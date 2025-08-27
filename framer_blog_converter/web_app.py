"""
Web application for the Framer Blog XML to CSV converter.
Provides a user-friendly interface for file uploads and conversions.
"""

import os
import tempfile
import uuid
from pathlib import Path
from typing import Dict, Any, Optional
from flask import Flask, render_template, request, jsonify, send_file, session, flash, redirect
from werkzeug.utils import secure_filename
import json

# Use absolute imports for direct execution
try:
    from src.blog_converter import FramerBlogConverter
    from src.config import DEFAULT_PLATFORMS
except ImportError:
    # Fallback for when running as module
    from .blog_converter import FramerBlogConverter
    from .config import DEFAULT_PLATFORMS


class WebConverter:
    """Web interface wrapper for the blog converter."""
    
    def __init__(self):
        self.app = Flask(__name__)
        self.app.secret_key = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
        self.app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB max file size
        self.app.config['UPLOAD_FOLDER'] = tempfile.gettempdir()
        
        # Ensure upload folder exists
        os.makedirs(self.app.config['UPLOAD_FOLDER'], exist_ok=True)
        
        self.setup_routes()
        self.converter = None
    
    def setup_routes(self):
        """Setup Flask routes."""
        
        @self.app.route('/')
        def index():
            """Main page with file upload form."""
            platforms = list(DEFAULT_PLATFORMS.keys())
            return render_template('index.html', platforms=platforms)
        
        @self.app.route('/upload', methods=['POST'])
        def upload_file():
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
                
                # Generate unique filename
                file_id = str(uuid.uuid4())
                filename = secure_filename(file.filename)
                file_path = os.path.join(self.app.config['UPLOAD_FOLDER'], f"{file_id}_{filename}")
                
                # Save uploaded file
                file.save(file_path)
                
                # Get conversion options
                platform = request.form.get('platform', 'wordpress')
                preserve_html = request.form.get('preserve_html', 'false').lower() == 'true'
                strip_html = request.form.get('strip_html', 'false').lower() == 'true'
                
                # Initialize converter
                self.converter = FramerBlogConverter()
                
                # Load platform template
                if not self.converter.load_platform_template(platform):
                    return jsonify({'error': f'Platform {platform} not supported'}), 400
                
                # Configure content processing
                self.converter.set_content_processing(
                    preserve_html=preserve_html,
                    strip_html=strip_html
                )
                
                # Store file info in session
                session['file_path'] = file_path
                session['file_id'] = file_id
                session['original_filename'] = filename
                session['platform'] = platform
                
                # Analyze file and get preview
                analysis = self.analyze_file(file_path)
                
                return jsonify({
                    'success': True,
                    'file_id': file_id,
                    'analysis': analysis,
                    'message': 'File uploaded successfully'
                })
                
            except Exception as e:
                return jsonify({'error': f'Upload failed: {str(e)}'}), 500
        
        @self.app.route('/convert', methods=['POST'])
        def convert_file():
            """Convert the uploaded file to CSV."""
            try:
                file_path = session.get('file_path')
                if not file_path or not os.path.exists(file_path):
                    return jsonify({'error': 'No file found. Please upload a file first.'}), 400
                
                if not self.converter:
                    return jsonify({'error': 'Converter not initialized. Please upload a file first.'}), 400
                
                # Generate output filename
                original_name = session.get('original_filename', 'export')
                base_name = Path(original_name).stem
                output_filename = f"{base_name}_framer.csv"
                output_path = os.path.join(self.app.config['UPLOAD_FOLDER'], f"{session['file_id']}_{output_filename}")
                
                # Perform conversion
                success = self.converter.convert(file_path, output_path)
                
                if not success:
                    return jsonify({'error': 'Conversion failed. Please check your file format.'}), 500
                
                # Store output path in session
                session['output_path'] = output_path
                session['output_filename'] = output_filename
                
                # Get conversion summary
                summary = self.get_conversion_summary(output_path)
                
                return jsonify({
                    'success': True,
                    'output_filename': output_filename,
                    'summary': summary,
                    'message': 'Conversion completed successfully'
                })
                
            except Exception as e:
                return jsonify({'error': f'Conversion failed: {str(e)}'}), 500
        
        @self.app.route('/download')
        def download_file():
            """Download the converted CSV file."""
            output_path = session.get('output_path')
            if not output_path or not os.path.exists(output_path):
                flash('No converted file found. Please convert a file first.', 'error')
                return redirect('/')
            
            return send_file(
                output_path,
                as_attachment=True,
                download_name=session.get('output_filename', 'converted.csv'),
                mimetype='text/csv'
            )
        
        @self.app.route('/preview')
        def preview_file():
            """Get a preview of the uploaded XML file."""
            file_path = session.get('file_path')
            if not file_path or not os.path.exists(file_path):
                return jsonify({'error': 'No file found'}), 400
            
            try:
                preview = self.get_file_preview(file_path)
                return jsonify({'success': True, 'preview': preview})
            except Exception as e:
                return jsonify({'error': f'Preview failed: {str(e)}'}), 500
        
        @self.app.route('/cleanup', methods=['POST'])
        def cleanup_files():
            """Clean up temporary files."""
            try:
                file_path = session.get('file_path')
                output_path = session.get('output_path')
                
                # Remove temporary files
                if file_path and os.path.exists(file_path):
                    os.remove(file_path)
                
                if output_path and os.path.exists(output_path):
                    os.remove(output_path)
                
                # Clear session
                session.clear()
                
                return jsonify({'success': True, 'message': 'Files cleaned up successfully'})
            except Exception as e:
                return jsonify({'error': f'Cleanup failed: {str(e)}'}), 500
        
        @self.app.route('/api/platforms')
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
    
    def analyze_file(self, file_path: str) -> Dict[str, Any]:
        """Analyze the uploaded XML file."""
        try:
            if not self.converter:
                return {'error': 'Converter not initialized'}
            
            # Get file statistics
            stats = self.converter.get_file_statistics(file_path)
            
            # Detect platform
            detected_platform = self.converter.detect_platform(file_path)
            
            return {
                'file_size': os.path.getsize(file_path),
                'file_size_mb': round(os.path.getsize(file_path) / (1024 * 1024), 2),
                'stats': stats,
                'detected_platform': detected_platform,
                'supported': detected_platform in DEFAULT_PLATFORMS
            }
        except Exception as e:
            return {'error': f'Analysis failed: {str(e)}'}
    
    def get_file_preview(self, file_path: str) -> Dict[str, Any]:
        """Get a preview of the XML file content."""
        try:
            if not self.converter:
                return {'error': 'Converter not initialized'}
            
            # Get preview data
            preview_data = self.converter.preview_posts(file_path, limit=5)
            
            return {
                'posts': preview_data,
                'total_posts': len(preview_data)
            }
        except Exception as e:
            return {'error': f'Preview failed: {str(e)}'}
    
    def get_conversion_summary(self, output_path: str) -> Dict[str, Any]:
        """Get summary of the conversion results."""
        try:
            if not os.path.exists(output_path):
                return {'error': 'Output file not found'}
            
            # Count lines in CSV (excluding header)
            with open(output_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            total_posts = len(lines) - 1 if len(lines) > 1 else 0  # Subtract header
            
            return {
                'total_posts': total_posts,
                'output_size': os.path.getsize(output_path),
                'output_size_mb': round(os.path.getsize(output_path) / (1024 * 1024), 2)
            }
        except Exception as e:
            return {'error': f'Summary failed: {str(e)}'}
    
    def run(self, debug: bool = True, host: str = '0.0.0.0', port: int = 5000):
        """Run the Flask application."""
        self.app.run(debug=debug, host=host, port=port)


def create_app():
    """Factory function to create the Flask app."""
    converter = WebConverter()
    return converter.app


if __name__ == '__main__':
    converter = WebConverter()
    converter.run(debug=True)
