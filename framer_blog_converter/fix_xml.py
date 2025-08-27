#!/usr/bin/env python3
"""
Script to fix malformed CDATA sections in WordPress XML exports.
"""

import re
import sys

def fix_cdata_sections(input_file, output_file):
    """Fix malformed CDATA sections in XML file."""
    print(f"Fixing CDATA sections in {input_file}...")
    
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        print(f"File size: {len(content)} characters")
        
        # Find and fix common CDATA issues
        original_content = content
        
        # Fix unclosed CDATA sections
        # Look for CDATA that starts but doesn't end properly
        cdata_pattern = r'<!\[CDATA\[([^]]*?)(?=<!\[CDATA\[|$|]]>)'
        
        # Count problematic CDATA sections
        problematic_count = len(re.findall(cdata_pattern, content))
        print(f"Found {problematic_count} potentially problematic CDATA sections")
        
        # Fix common issues
        # 1. Replace unclosed CDATA with proper closing
        content = re.sub(r'<!\[CDATA\[([^]]*?)(?=<!\[CDATA\[|$)', r'<![CDATA[\1]]>', content)
        
        # 2. Fix CDATA that might have HTML tags breaking them
        content = re.sub(r'<!\[CDATA\[([^]]*?)<([^>]*?)>([^]]*?)(?=<!\[CDATA\[|$)', r'<![CDATA[\1<\2>\3]]>', content)
        
        # 3. Look for CDATA that ends abruptly and add proper closing
        content = re.sub(r'<!\[CDATA\[([^]]*?)(?=\s*$)', r'<![CDATA[\1]]>', content)
        
        # Check if we made changes
        if content != original_content:
            print("Fixed CDATA sections, writing to output file...")
            
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print(f"Fixed XML saved to {output_file}")
            return True
        else:
            print("No CDATA issues found or fixed")
            return False
            
    except Exception as e:
        print(f"Error fixing XML: {e}")
        return False

def main():
    """Main function."""
    input_file = "src/Squarespace-Wordpress-Export-08-27-2025.xml"
    output_file = "src/Squarespace-Wordpress-Export-08-27-2025_fixed.xml"
    
    print("XML CDATA Fixer for WordPress Exports")
    print("=" * 50)
    
    success = fix_cdata_sections(input_file, output_file)
    
    if success:
        print(f"\n✅ Successfully fixed XML file!")
        print(f"Original: {input_file}")
        print(f"Fixed: {output_file}")
        print(f"\nNow try converting the fixed file:")
        print(f"python3 -m src.cli {output_file} framer_import.csv --platform wordpress")
    else:
        print("\n❌ Failed to fix XML file")
        print("The XML may have other structural issues")

if __name__ == '__main__':
    main()
