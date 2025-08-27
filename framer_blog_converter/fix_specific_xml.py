#!/usr/bin/env python3
"""
Script to fix the specific malformed CDATA section in the XML file.
"""

def fix_specific_xml_issue(input_file, output_file):
    """Fix the specific XML issue around line 58089."""
    print(f"Fixing specific XML issue in {input_file}...")
    
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        print(f"File has {len(lines)} lines")
        
        # Look for the problematic area around line 58089
        problematic_line = None
        for i, line in enumerate(lines, 1):
            if i >= 58080 and i <= 58100:  # Check around the problematic line
                if 'CData section not finished' in line or 'CDATA' in line:
                    print(f"Line {i}: {line.strip()}")
                    problematic_line = i
                    break
        
        if not problematic_line:
            print("Could not locate the specific problematic line")
            return False
        
        # Look for unclosed CDATA sections
        fixed_content = ""
        in_cdata = False
        cdata_buffer = ""
        
        for i, line in enumerate(lines, 1):
            if '<![CDATA[' in line:
                in_cdata = True
                cdata_buffer = line
            elif in_cdata:
                cdata_buffer += line
                if ']]>' in line:
                    # CDATA section is properly closed
                    fixed_content += cdata_buffer
                    in_cdata = False
                    cdata_buffer = ""
                elif i == len(lines):  # End of file
                    # Close any unclosed CDATA at end of file
                    if not cdata_buffer.endswith(']]>'):
                        cdata_buffer += ']]>'
                    fixed_content += cdata_buffer
            else:
                fixed_content += line
        
        # Write the fixed content
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(fixed_content)
        
        print(f"Fixed XML saved to {output_file}")
        return True
        
    except Exception as e:
        print(f"Error fixing XML: {e}")
        return False

def main():
    """Main function."""
    input_file = "src/Squarespace-Wordpress-Export-08-27-2025.xml"
    output_file = "src/Squarespace-Wordpress-Export-08-27-2025_fixed.xml"
    
    print("Specific XML Issue Fixer")
    print("=" * 50)
    
    success = fix_specific_xml_issue(input_file, output_file)
    
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
