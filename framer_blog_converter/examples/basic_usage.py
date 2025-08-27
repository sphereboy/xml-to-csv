#!/usr/bin/env python3
"""
Basic usage example for the Framer Blog XML to CSV converter.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from blog_converter import FramerBlogConverter

def main():
    """Demonstrate basic usage of the converter."""
    print("Framer Blog XML to CSV Converter - Basic Usage Example")
    print("=" * 60)
    
    # Initialize converter
    converter = FramerBlogConverter()
    
    # List available platforms
    print("\nAvailable platforms:")
    platforms = converter.list_available_platforms()
    for platform in platforms:
        print(f"  - {platform}")
    
    # Load WordPress platform template
    print("\nLoading WordPress platform template...")
    success = converter.load_platform_template('wordpress')
    if success:
        print("✓ WordPress template loaded successfully")
    else:
        print("✗ Failed to load WordPress template")
        return
    
    # Configure content processing
    print("\nConfiguring content processing...")
    converter.set_content_processing(
        preserve_html=True,
        generate_slugs=True,
        max_content_length=100000
    )
    print("✓ Content processing configured")
    
    # Sample XML file path (adjust as needed)
    input_file = "tests/sample_data/sample_wordpress.xml"
    output_file = "sample_output.csv"
    
    print(f"\nConverting {input_file} to {output_file}...")
    
    # Perform conversion
    success = converter.convert(input_file, output_file)
    
    if success:
        print(f"\n✓ Conversion completed successfully!")
        print(f"Output file: {output_file}")
        
        # Show preview
        print("\nPreview of converted data:")
        preview = converter.preview(input_file, 2)
        print(preview)
    else:
        print("\n✗ Conversion failed!")

if __name__ == '__main__':
    main()
