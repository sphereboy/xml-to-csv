#!/usr/bin/env python3
"""
Demo script for the Framer Blog XML to CSV Converter web application.
This script demonstrates how to use the web interface programmatically.
"""

import requests
import time
import os
import sys

# Add the src directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def demo_web_converter():
    """Demonstrate the web converter functionality."""
    
    # Base URL for the web application
    base_url = "http://localhost:5000"
    
    print("🚀 Framer Blog XML to CSV Converter - Web Demo")
    print("=" * 60)
    
    # Check if the web server is running
    try:
        response = requests.get(base_url, timeout=5)
        if response.status_code == 200:
            print("✅ Web server is running!")
        else:
            print(f"⚠️  Web server responded with status: {response.status_code}")
    except requests.exceptions.ConnectionError:
        print("❌ Web server is not running!")
        print("Please start the web server first:")
        print("  python run_web.py")
        return
    except Exception as e:
        print(f"❌ Error connecting to web server: {e}")
        return
    
    print("\n📋 Available endpoints:")
    print(f"  • Main page: {base_url}/")
    print(f"  • Upload: {base_url}/upload")
    print(f"  • Convert: {base_url}/convert")
    print(f"  • Download: {base_url}/download")
    print(f"  • Preview: {base_url}/preview")
    print(f"  • Platforms API: {base_url}/api/platforms")
    
    # Get available platforms
    try:
        response = requests.get(f"{base_url}/api/platforms")
        if response.status_code == 200:
            platforms = response.json()
            print(f"\n🔧 Supported platforms ({len(platforms)}):")
            for platform in platforms:
                print(f"  • {platform['name']}: {platform['display_name']}")
                if platform.get('description'):
                    print(f"    {platform['description']}")
        else:
            print(f"⚠️  Could not fetch platforms: {response.status_code}")
    except Exception as e:
        print(f"❌ Error fetching platforms: {e}")
    
    print("\n💡 To use the web interface:")
    print("1. Open your browser and go to: http://localhost:5000")
    print("2. Drag and drop your XML file or click 'Choose File'")
    print("3. Select your blog platform")
    print("4. Choose content processing options")
    print("5. Click 'Convert to CSV'")
    print("6. Download your converted file")
    
    print("\n🔧 For developers:")
    print("• The web app uses Flask for the backend")
    print("• Frontend is built with Tailwind CSS and vanilla JavaScript")
    print("• File uploads are limited to 50MB")
    print("• Temporary files are automatically cleaned up")
    print("• Session-based file management for security")

def test_api_endpoints():
    """Test the API endpoints to ensure they're working."""
    
    base_url = "http://localhost:5000"
    
    print("\n🧪 Testing API endpoints...")
    
    # Test platforms endpoint
    try:
        response = requests.get(f"{base_url}/api/platforms")
        if response.status_code == 200:
            print("✅ Platforms API: Working")
        else:
            print(f"❌ Platforms API: Failed ({response.status_code})")
    except Exception as e:
        print(f"❌ Platforms API: Error - {e}")
    
    # Test main page
    try:
        response = requests.get(base_url)
        if response.status_code == 200:
            print("✅ Main page: Working")
        else:
            print(f"❌ Main page: Failed ({response.status_code})")
    except Exception as e:
        print(f"❌ Main page: Error - {e}")

if __name__ == "__main__":
    print("Starting web converter demo...")
    demo_web_converter()
    test_api_endpoints()
    
    print("\n🎉 Demo complete!")
    print("\nTo start the web server, run:")
    print("  python run_web.py")
    print("\nThen open http://localhost:5000 in your browser.")
