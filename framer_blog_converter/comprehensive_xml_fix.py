#!/usr/bin/env python3
"""
Comprehensive XML fixer that handles control characters, invalid XML, and structural issues.
"""

import re
import string

def fix_xml_comprehensively(input_file, output_file):
    """Fix XML file comprehensively by handling all common issues."""
    print(f"Comprehensively fixing XML file: {input_file}")
    
    try:
        with open(input_file, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        
        print(f"Original file size: {len(content)} characters")
        
        # Step 1: Remove or replace invalid XML characters
        print("Step 1: Cleaning invalid XML characters...")
        
        # Remove control characters (except tab, newline, carriage return)
        allowed_chars = set(string.printable) - set(string.whitespace) | {'\t', '\n', '\r'}
        cleaned_content = ''
        
        for char in content:
            if char in allowed_chars:
                cleaned_content += char
            else:
                # Replace invalid characters with space
                cleaned_content += ' '
        
        print(f"After character cleaning: {len(cleaned_content)} characters")
        
        # Step 2: Remove all CDATA sections and replace with plain text
        print("Step 2: Removing CDATA sections...")
        
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
        cleaned_content = re.sub(cdata_pattern, replace_cdata, cleaned_content, flags=re.DOTALL)
        
        # Also handle any unclosed CDATA sections
        unclosed_pattern = r'<!\[CDATA\[([^]]*?)(?=<!\[CDATA\[|$)'
        cleaned_content = re.sub(unclosed_pattern, r'\1', cleaned_content, flags=re.DOTALL)
        
        print(f"After CDATA removal: {len(cleaned_content)} characters")
        
        # Step 3: Fix common XML structural issues
        print("Step 3: Fixing XML structure...")
        
        # Remove any remaining CDATA markers
        cleaned_content = cleaned_content.replace('<![CDATA[', '')
        cleaned_content = cleaned_content.replace(']]>', '')
        
        # Fix common HTML entities
        cleaned_content = cleaned_content.replace('&', '&amp;')
        cleaned_content = cleaned_content.replace('<', '&lt;')
        cleaned_content = cleaned_content.replace('>', '&gt;')
        
        # Now restore the XML structure by replacing the escaped tags back
        cleaned_content = cleaned_content.replace('&lt;', '<')
        cleaned_content = cleaned_content.replace('&gt;', '>')
        
        # But keep &amp; as is for proper XML
        cleaned_content = cleaned_content.replace('&amp;amp;', '&amp;')
        
        print(f"After structure fixing: {len(cleaned_content)} characters")
        
        # Step 4: Validate basic XML structure
        print("Step 4: Validating XML structure...")
        
        # Ensure the file starts with XML declaration
        if not cleaned_content.startswith('<?xml'):
            cleaned_content = '<?xml version="1.0" encoding="UTF-8"?>\n' + cleaned_content
        
        # Write fixed content
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(cleaned_content)
        
        print(f"Final file size: {len(cleaned_content)} characters")
        print(f"Fixed XML saved to: {output_file}")
        
        return True
        
    except Exception as e:
        print(f"Error fixing XML: {e}")
        return False

def main():
    """Main function."""
    input_file = "src/Squarespace-Wordpress-Export-08-27-2025.xml"
    output_file = "src/Squarespace-Wordpress-Export-08-27-2025_final.xml"
    
    print("Comprehensive XML Fixer")
    print("=" * 50)
    
    success = fix_xml_comprehensively(input_file, output_file)
    
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
