# Framer Blog XML to CSV Converter

A robust, memory-efficient tool for converting blog XML exports to Framer-compatible CSV format. Designed specifically for seamless blog CMS import into Framer.

## Features

- **Memory-efficient processing** - Uses streaming XML parsing to handle large files
- **Multi-platform support** - WordPress, Ghost, Jekyll, and custom formats
- **Framer compatibility** - Outputs CSV in exact format expected by Framer Blog CMS
- **Content preservation** - Handles HTML, rich text, metadata, and media references
- **Auto-detection** - Automatically detects blog platform from XML structure
- **Progress tracking** - Shows conversion progress for large files
- **Validation** - Comprehensive output validation and error checking
- **Flexible configuration** - Customizable content processing options

## Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Install from source

```bash
# Clone the repository
git clone <repository-url>
cd framer_blog_converter

# Install dependencies
pip install -r requirements.txt

# Install the package
pip install -e .
```

### Install dependencies only

```bash
pip install lxml tqdm python-dateutil beautifulsoup4 click pydantic
```

## Quick Start

### Basic Usage

```bash
# Convert WordPress XML export
python -m framer_blog_converter.cli wordpress_export.xml framer_blog.csv --platform wordpress

# Auto-detect platform
python -m framer_blog_converter.cli blog_export.xml framer_blog.csv --auto-detect

# Preview conversion
python -m framer_blog_converter.cli blog_export.xml --preview 10

# Get file statistics
python -m framer_blog_converter.cli blog_export.xml --stats
```

### Python API

```python
from framer_blog_converter import FramerBlogConverter

# Initialize converter
converter = FramerBlogConverter()

# Load platform template
converter.load_platform_template('wordpress')

# Configure content processing
converter.set_content_processing(
    preserve_html=True,
    generate_slugs=True,
    max_content_length=50000
)

# Convert file
success = converter.convert('input.xml', 'output.csv')
```

## Supported Platforms

### WordPress
- **Format**: WordPress XML export (Tools > Export)
- **Features**: Full content, excerpts, categories, tags, author info
- **Special handling**: CDATA sections, namespaced elements, status mapping

### Ghost
- **Format**: Ghost JSON export (converted to XML)
- **Features**: HTML content, excerpts, tags, author info
- **Special handling**: ISO date formats, status mapping

### Jekyll
- **Format**: Jekyll front matter and markdown
- **Features**: Markdown content, categories, tags, author info
- **Special handling**: YAML front matter parsing

### Custom
- **Format**: Any XML structure
- **Features**: Configurable field mapping
- **Special handling**: Custom templates and field extraction

## Output Format

The converter generates CSV files with the following columns, exactly matching Framer's requirements:

| Column | Description | Required |
|--------|-------------|----------|
| Title | Blog post title | Yes |
| Slug | URL-friendly version of title | Yes |
| Content | Main blog content (HTML preserved) | Yes |
| Excerpt | Short description/summary | Yes |
| Author | Post author name | Yes |
| Published Date | Publication date (YYYY-MM-DD) | Yes |
| Featured Image | URL to main image | No |
| Categories | Comma-separated category list | No |
| Tags | Comma-separated tag list | No |
| Status | Published/Draft status | Yes |
| SEO Title | Custom title for SEO | No |
| SEO Description | Meta description | No |

## Configuration

### Content Processing Options

```python
converter.set_content_processing(
    preserve_html=True,           # Keep HTML formatting
    strip_html_tags=[],           # Tags to remove
    max_content_length=50000,     # Max content length
    generate_slugs=True,          # Auto-generate slugs
    slug_max_length=60,           # Max slug length
    handle_cdata=True,            # Process CDATA sections
    validate_urls=False,          # Validate image URLs
    output_encoding='utf-8'       # Output encoding
)
```

### Custom Platform Templates

Create a JSON configuration file:

```json
{
  "name": "Custom Blog",
  "description": "Custom blog platform",
  "item_tag": "post",
  "field_mappings": {
    "title": "title",
    "content": "body",
    "author": "writer",
    "date": "publish_date"
  },
  "date_formats": ["%Y-%m-%d", "%Y-%m-%d %H:%M:%S"],
  "status_mapping": {
    "live": "Published",
    "draft": "Draft"
  }
}
```

Load custom template:

```python
converter.load_platform_template('custom')
```

## Command Line Options

### Basic Commands

```bash
# List available platforms
python -m framer_blog_converter.cli --list-platforms

# Show help
python -m framer_blog_converter.cli --help
```

### Conversion Options

```bash
# Platform specification
--platform, -p {wordpress,ghost,jekyll,custom}

# Auto-detection
--auto-detect, -a

# Preview mode
--preview N

# File statistics
--stats, -s

# Validation
--validate, -V
```

### Content Processing Options

```bash
# HTML handling
--preserve-html          # Keep HTML formatting
--strip-html            # Remove all HTML

# Content limits
--max-content-length N  # Maximum content length

# Slug generation
--generate-slugs        # Auto-generate slugs
--no-slugs             # Don't generate slugs

# Encoding
--encoding, -e ENCODING # Output encoding
```

### Configuration

```bash
# Custom config file
--config, -c FILE

# Verbose output
--verbose, -v
```

## Examples

### WordPress Export

```bash
# Convert WordPress export
python -m framer_blog_converter.cli \
  wordpress_export.xml \
  framer_import.csv \
  --platform wordpress \
  --validate

# Preview first 5 posts
python -m framer_blog_converter.cli \
  wordpress_export.xml \
  --preview 5 \
  --platform wordpress
```

### Ghost Export

```bash
# Convert Ghost export with auto-detection
python -m framer_blog_converter.cli \
  ghost_export.xml \
  framer_import.csv \
  --auto-detect \
  --preserve-html
```

### Custom Format

```bash
# Convert with custom configuration
python -m framer_blog_converter.cli \
  custom_blog.xml \
  framer_import.csv \
  --config custom_mapping.json \
  --validate
```

## Error Handling

The converter provides comprehensive error handling:

- **XML parsing errors** - Detailed error messages for malformed XML
- **Missing fields** - Warnings for missing optional fields
- **Content validation** - Length checks and content warnings
- **Platform detection** - Fallback options for unknown formats
- **File I/O errors** - Graceful handling of file access issues

## Performance

### Memory Usage

- **Streaming parser** - Processes XML without loading entire file into memory
- **Element cleanup** - Automatically frees memory after processing each post
- **Configurable limits** - Set maximum content length to prevent memory issues

### Processing Speed

- **Typical performance**: 0.1 seconds per MB + 0.05 seconds per post
- **Large files**: Handles files with 1000+ posts efficiently
- **Progress tracking** - Real-time progress updates for long operations

## Troubleshooting

### Common Issues

1. **Platform not detected**
   - Use `--platform` to specify manually
   - Check XML structure with `--stats`

2. **Memory errors**
   - Reduce `--max-content-length`
   - Check available system memory

3. **Encoding issues**
   - Specify `--encoding` parameter
   - Check XML file encoding declaration

4. **Missing content**
   - Verify field mappings in platform template
   - Check XML structure with preview mode

### Debug Mode

```bash
# Enable verbose output
python -m framer_blog_converter.cli \
  input.xml \
  output.csv \
  --verbose \
  --platform wordpress
```

## Development

### Project Structure

```
framer_blog_converter/
├── src/
│   ├── __init__.py           # Package initialization
│   ├── blog_converter.py     # Core conversion logic
│   ├── framer_formatter.py   # CSV formatting
│   ├── content_processor.py  # Content processing
│   ├── cli.py               # Command line interface
│   ├── config.py            # Configuration management
│   └── utils.py             # Utility functions
├── templates/                # Platform templates
├── tests/                   # Test suite
├── requirements.txt         # Dependencies
└── README.md               # This file
```

### Running Tests

```bash
# Install test dependencies
pip install pytest

# Run tests
pytest tests/
```

### Adding New Platforms

1. Create platform template in `templates/`
2. Add platform mapping in `config.py`
3. Update platform detection logic
4. Add test cases

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For issues and questions:

1. Check the troubleshooting section
2. Review existing issues
3. Create a new issue with detailed information
4. Include sample XML and error messages

## Changelog

### Version 1.0.0
- Initial release
- WordPress, Ghost, and Jekyll support
- Streaming XML parser
- Framer-compatible CSV output
- Command line interface
- Python API
