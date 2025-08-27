#!/usr/bin/env python3
"""
Robust XML parser that can handle malformed CDATA sections.
"""

import re
import os

def fix_xml_cdata(input_file, output_file):
    """Fix malformed CDATA sections in XML file."""
    print(f"Fixing XML file: {input_file}")
    
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        print(f"Original file size: {len(content)} characters")
        
        # Fix common CDATA issues
        fixed_content = content
        
        # Pattern 1: Find CDATA sections that start but don't end properly
        # Look for <![CDATA[ followed by content but no ]]>
        cdata_pattern = r'<!\[CDATA\[([^]]*?)(?=<!\[CDATA\[|$|]]>)'
        matches = re.findall(cdata_pattern, content, re.DOTALL)
        
        if matches:
            print(f"Found {len(matches)} potentially problematic CDATA sections")
            
            # Fix by adding proper closing tags
            for match in matches:
                # Escape special characters in the match
                escaped_match = re.escape(match)
                # Replace the problematic CDATA with properly closed one
                pattern = f'<!\\[CDATA\\[{escaped_match}(?=<!\\[CDATA\\[|$|]]>)'
                replacement = f'<![CDATA[{match}]]>'
                fixed_content = re.sub(pattern, replacement, fixed_content)
        
        # Pattern 2: Look for CDATA that might be broken by HTML tags
        # This is more complex and requires careful handling
        lines = content.split('\n')
        fixed_lines = []
        in_cdata = False
        cdata_buffer = []
        
        for line in lines:
            if '<![CDATA[' in line:
                in_cdata = True
                cdata_buffer = [line]
            elif in_cdata:
                cdata_buffer.append(line)
                if ']]>' in line:
                    # CDATA section is properly closed
                    fixed_lines.extend(cdata_buffer)
                    in_cdata = False
                    cdata_buffer = []
                elif line.strip() == '' or line.strip().startswith('</'):
                    # End of content, close CDATA
                    cdata_buffer.append(']]>')
                    fixed_lines.extend(cdata_buffer)
                    in_cdata = False
                    cdata_buffer = []
            else:
                fixed_lines.append(line)
        
        # If we still have unclosed CDATA at the end
        if in_cdata and cdata_buffer:
            cdata_buffer.append(']]>')
            fixed_lines.extend(cdata_buffer)
        
        # Join lines back together
        final_content = '\n'.join(fixed_lines)
        
        # Write fixed content
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(final_content)
        
        print(f"Fixed file size: {len(final_content)} characters")
        print(f"Fixed XML saved to: {output_file}")
        
        return True
        
    except Exception as e:
        print(f"Error fixing XML: {e}")
        return False

def main():
    """Main function."""
    input_file = "src/Squarespace-Wordpress-Export-08-27-2025.xml"
    output_file = "src/Squarespace-Wordpress-Export-08-27-2025_fixed.xml"
    
    print("Robust XML CDATA Fixer")
    print("=" * 50)
    
    success = fix_xml_cdata(input_file, output_file)
    
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
