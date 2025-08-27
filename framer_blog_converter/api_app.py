"""
API-only Flask application for the Framer Blog XML to CSV converter.
This is designed to be deployed separately from the frontend.
"""

import os
import tempfile
import uuid
from pathlib import Path
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from werkzeug.utils import secure_filename
import json

# Import the converter
try:
    from src.blog_converter import FramerBlogConverter
    from src.config import DEFAULT_PLATFORMS
except ImportError:
    # Fallback for when running as module
    from .blog_converter import FramerBlogConverter
    from .config import DEFAULT_PLATFORMS

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend communication

# Configuration
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB max file size
app.config['UPLOAD_FOLDER'] = tempfile.gettempdir()

# Ensure upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({'status': 'healthy', 'message': 'API is running'})

@app.route('/api/platforms', methods=['GET'])
def get_platforms():
    """Get available platform templates."""
    platforms = []
    for name, mapping in DEFAULT_PLATFORMS.items():
        platforms.append({
            'name': name,
            'display_name': mapping.name,
            'description': mapping.description
        })
    return jsonify(platforms)

@app.route('/api/convert', methods=['POST'])
def convert_file():
    """Handle file upload and conversion."""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file uploaded'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        # Validate file type
        if not file.filename.lower().endswith('.xml'):
            return jsonify({'error': 'Only XML files are supported'}), 400
        
        # Get conversion options
        platform = request.form.get('platform', 'wordpress')
        preserve_html = request.form.get('preserve_html', 'false').lower() == 'true'
        strip_html = request.form.get('strip_html', 'false').lower() == 'true'
        
        # Generate unique filename
        file_id = str(uuid.uuid4())
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], f"{file_id}_{filename}")
        
        # Save uploaded file
        file.save(file_path)
        
        try:
            # Initialize converter
            converter = FramerBlogConverter()
            
            # Load platform template
            if not converter.load_platform_template(platform):
                return jsonify({'error': f'Platform {platform} not supported'}), 400
            
            # Configure content processing
            converter.set_content_processing(
                preserve_html=preserve_html,
                strip_html=strip_html
            )
            
            # Convert the file
            output_filename = f"{file_id}_{filename.replace('.xml', '.csv')}"
            output_path = os.path.join(app.config['UPLOAD_FOLDER'], output_filename)
            
            success = converter.convert_file(file_path, output_path)
            
            if not success:
                return jsonify({'error': 'Conversion failed'}), 500
            
            # Return success response with file info
            return jsonify({
                'success': True,
                'message': 'File converted successfully',
                'download_url': f'/api/download/{file_id}',
                'file_id': file_id,
                'original_filename': filename,
                'output_filename': output_filename
            })
            
        finally:
            # Clean up uploaded file
            if os.path.exists(file_path):
                os.remove(file_path)
                
    except Exception as e:
        return jsonify({'error': f'Conversion failed: {str(e)}'}), 500

@app.route('/api/download/<file_id>', methods=['GET'])
def download_file(file_id):
    """Download converted CSV file."""
    try:
        # Find the file with this ID
        for filename in os.listdir(app.config['UPLOAD_FOLDER']):
            if filename.startswith(file_id) and filename.endswith('.csv'):
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                
                # Send file and then delete it
                response = send_file(
                    file_path,
                    as_attachment=True,
                    download_name=filename.replace(f"{file_id}_", "")
                )
                
                # Schedule file deletion after response
                @response.call_on_close
                def cleanup():
                    try:
                        if os.path.exists(file_path):
                            os.remove(file_path)
                    except:
                        pass
                
                return response
        
        return jsonify({'error': 'File not found'}), 404
        
    except Exception as e:
        return jsonify({'error': f'Download failed: {str(e)}'}), 500

@app.route('/api/analyze', methods=['POST'])
def analyze_file():
    """Analyze uploaded XML file."""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file uploaded'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        # Generate unique filename
        file_id = str(uuid.uuid4())
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], f"{file_id}_{filename}")
        
        # Save uploaded file
        file.save(file_path)
        
        try:
            # Initialize converter for analysis
            converter = FramerBlogConverter()
            
            # Get file statistics
            stats = converter.get_file_statistics(file_path)
            
            # Detect platform
            detected_platform = converter.detect_platform(file_path)
            
            # Get preview data
            preview_data = converter.preview_posts(file_path, limit=5)
            
            return jsonify({
                'file_size': os.path.getsize(file_path),
                'file_size_mb': round(os.path.getsize(file_path) / (1024 * 1024), 2),
                'stats': stats,
                'detected_platform': detected_platform,
                'supported': detected_platform in DEFAULT_PLATFORMS,
                'preview': preview_data
            })
            
        finally:
            # Clean up uploaded file
            if os.path.exists(file_path):
                os.remove(file_path)
                
    except Exception as e:
        return jsonify({'error': f'Analysis failed: {str(e)}'}), 500

if __name__ == '__main__':
    # Get port from environment variable for production deployment
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') != 'production'
    
    app.run(debug=debug, host='0.0.0.0', port=port)
