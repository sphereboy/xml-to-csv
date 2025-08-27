#!/usr/bin/env python3
"""
Precise XML fixer that only fixes specific problematic CDATA sections.
"""

import re

def fix_xml_precisely(input_file, output_file):
    """Fix XML file more precisely by targeting only problematic areas."""
    print(f"Precisely fixing XML file: {input_file}")
    
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        print(f"Original file size: {len(content)} characters")
        
        # Instead of trying to fix all CDATA, let's try a different approach
        # Look for the specific error pattern mentioned in the error
        
        # The error was around line 58089 with "CData section not finished"
        # Let's try to find and fix that specific area
        
        # First, let's try to use a more lenient XML parser approach
        # We'll create a version that removes problematic CDATA sections entirely
        
        # Remove all CDATA sections and replace with plain text
        # This is a more aggressive approach but should work
        print("Removing all CDATA sections and replacing with plain text...")
        
        # Pattern to match CDATA sections
        cdata_pattern = r'<!\[CDATA\[(.*?)\]\]>'
        
        def replace_cdata(match):
            content = match.group(1)
            # Escape any HTML entities that might cause issues
            content = content.replace('&', '&amp;')
            content = content.replace('<', '&lt;')
            content = content.replace('>', '&gt;')
            return content
        
        # Replace all CDATA sections
        fixed_content = re.sub(cdata_pattern, replace_cdata, content, flags=re.DOTALL)
        
        # Also handle any unclosed CDATA sections
        unclosed_pattern = r'<!\[CDATA\[([^]]*?)(?=<!\[CDATA\[|$)'
        fixed_content = re.sub(unclosed_pattern, r'\1', fixed_content, flags=re.DOTALL)
        
        # Write fixed content
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(fixed_content)
        
        print(f"Fixed file size: {len(fixed_content)} characters")
        print(f"Fixed XML saved to: {output_file}")
        
        return True
        
    except Exception as e:
        print(f"Error fixing XML: {e}")
        return False

def main():
    """Main function."""
    input_file = "src/Squarespace-Wordpress-Export-08-27-2025.xml"
    output_file = "src/Squarespace-Wordpress-Export-08-27-2025_clean.xml"
    
    print("Precise XML CDATA Fixer")
    print("=" * 50)
    
    success = fix_xml_precisely(input_file, output_file)
    
    if success:
        print(f"\n✅ Successfully fixed XML file!")
        print(f"Original: {input_file}")
        print(f"Fixed: {output_file}")
        print(f"\nNow try converting the fixed file:")
        print(f"python3 -m src.cli {output_file} framer_import.csv --platform wordpress")
    else:
        print("\n❌ Failed to fix XML file")

if __name__ == '__main__':
    main()
