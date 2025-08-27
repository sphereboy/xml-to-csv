#!/usr/bin/env python3
"""
Simple launcher for the Framer Blog XML to CSV Converter web application.
"""

import sys
import os

# Add the src directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from web_app import WebConverter

def main():
    """Launch the web application."""
    print("🚀 Starting Framer Blog XML to CSV Converter...")
    print("📱 Web interface will be available at: http://localhost:5001")
    print("🔄 Press Ctrl+C to stop the server")
    print()
    
    try:
        converter = WebConverter()
        converter.run(debug=True, host='0.0.0.0', port=5001)
    except KeyboardInterrupt:
        print("\n👋 Server stopped. Goodbye!")
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
