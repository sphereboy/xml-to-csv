#!/usr/bin/env python3
"""
Simplified API for testing and debugging.
"""

import os
import tempfile
import uuid
from pathlib import Path
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from werkzeug.utils import secure_filename
import json
import traceback

app = Flask(__name__)
CORS(app)

# Configuration
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB max file size
app.config['UPLOAD_FOLDER'] = tempfile.gettempdir()

# Ensure upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({
        'status': 'healthy', 
        'message': 'API is running',
        'upload_folder': app.config['UPLOAD_FOLDER'],
        'python_version': os.sys.version
    })

@app.route('/api/platforms', methods=['GET'])
def get_platforms():
    """Get available platform templates."""
    try:
        # Try to import the converter
        from src.blog_converter import FramerBlogConverter
        from src.config import DEFAULT_PLATFORMS
        
        platforms = []
        for name, mapping in DEFAULT_PLATFORMS.items():
            platforms.append({
                'name': name,
                'display_name': mapping.name,
                'description': mapping.description
            })
        return jsonify(platforms)
    except Exception as e:
        return jsonify({
            'error': f'Failed to load platforms: {str(e)}',
            'traceback': traceback.format_exc()
        }), 500

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
        
        # Generate unique filename
        file_id = str(uuid.uuid4())
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], f"{file_id}_{filename}")
        
        # Save uploaded file
        file.save(file_path)
        
        try:
            # Try to import and use the converter
            from src.blog_converter import FramerBlogConverter
            
            # Initialize converter
            converter = FramerBlogConverter()
            
            # Load platform template
            if not converter.load_platform_template(platform):
                return jsonify({'error': f'Platform {platform} not supported'}), 400
            
            # Convert the file using the correct method name
            output_filename = f"{file_id}_{filename.replace('.xml', '.csv')}"
            output_path = os.path.join(app.config['UPLOAD_FOLDER'], output_filename)
            
            success = converter.convert(file_path, output_path, platform)
            
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
            
        except Exception as e:
            return jsonify({
                'error': f'Conversion failed: {str(e)}',
                'traceback': traceback.format_exc()
            }), 500
            
        finally:
            # Clean up uploaded file
            if os.path.exists(file_path):
                os.remove(file_path)
                
    except Exception as e:
        return jsonify({
            'error': f'Request failed: {str(e)}',
            'traceback': traceback.format_exc()
        }), 500

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
        return jsonify({
            'error': f'Download failed: {str(e)}',
            'traceback': traceback.format_exc()
        }), 500

if __name__ == '__main__':
    # Get port from environment variable for production deployment
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') != 'production'
    
    print(f"Starting API server on port {port}")
    print(f"Debug mode: {debug}")
    print(f"Upload folder: {app.config['UPLOAD_FOLDER']}")
    
    app.run(debug=debug, host='0.0.0.0', port=port)
