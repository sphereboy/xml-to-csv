"""
Utility functions for the Framer Blog XML to CSV converter.
"""

import os
import re
import hashlib
from typing import List, Dict, Any, Optional
from pathlib import Path
from urllib.parse import urlparse, urljoin


def sanitize_filename(filename: str) -> str:
    """Sanitize filename for safe file operations."""
    # Remove or replace unsafe characters
    filename = re.sub(r'[<>:"/\\|?*]', '_', filename)
    # Remove leading/trailing spaces and dots
    filename = filename.strip(' .')
    # Limit length
    if len(filename) > 200:
        filename = filename[:200]
    return filename


def generate_file_hash(file_path: str, algorithm: str = 'md5') -> str:
    """Generate hash for a file."""
    hash_func = hashlib.new(algorithm)
    
    with open(file_path, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_func.update(chunk)
    
    return hash_func.hexdigest()


def validate_xml_file(file_path: str) -> Dict[str, Any]:
    """Validate XML file structure and content."""
    result = {
        "valid": True,
        "errors": [],
        "warnings": [],
        "file_size": 0,
        "encoding": None,
        "root_element": None
    }
    
    try:
        # Check file exists and is readable
        if not os.path.exists(file_path):
            result["valid"] = False
            result["errors"].append("File does not exist")
            return result
        
        # Get file size
        result["file_size"] = os.path.getsize(file_path)
        
        if result["file_size"] == 0:
            result["valid"] = False
            result["errors"].append("File is empty")
            return result
        
        # Try to parse XML
        from lxml import etree
        
        with open(file_path, 'rb') as f:
            # Read first few bytes to detect encoding
            header = f.read(100)
            f.seek(0)
            
            # Try to detect encoding
            if header.startswith(b'<?xml'):
                encoding_match = re.search(rb'encoding=["\']([^"\']+)["\']', header)
                if encoding_match:
                    result["encoding"] = encoding_match.group(1).decode('ascii')
            
            # Parse XML
            try:
                tree = etree.parse(f)
                root = tree.getroot()
                result["root_element"] = root.tag
                
                # Check for common blog-related elements
                blog_elements = ['item', 'post', 'entry', 'article']
                found_elements = []
                
                for elem in blog_elements:
                    if root.find(f'.//{elem}') is not None:
                        found_elements.append(elem)
                
                if not found_elements:
                    result["warnings"].append("No common blog post elements found")
                else:
                    result["warnings"].append(f"Found blog elements: {', '.join(found_elements)}")
                
            except etree.XMLSyntaxError as e:
                result["valid"] = False
                result["errors"].append(f"XML syntax error: {e}")
        
    except Exception as e:
        result["valid"] = False
        result["errors"].append(f"File validation error: {e}")
    
    return result


def detect_encoding(file_path: str) -> Optional[str]:
    """Detect file encoding."""
    try:
        import chardet
        
        with open(file_path, 'rb') as f:
            raw_data = f.read(10000)  # Read first 10KB
            result = chardet.detect(raw_data)
            return result['encoding'] if result['confidence'] > 0.7 else None
    
    except ImportError:
        # Fallback to basic detection
        try:
            with open(file_path, 'rb') as f:
                header = f.read(100)
                if header.startswith(b'<?xml'):
                    encoding_match = re.search(rb'encoding=["\']([^"\']+)["\']', header)
                    if encoding_match:
                        return encoding_match.group(1).decode('ascii')
        except:
            pass
        
        return None


def normalize_url(url: str, base_url: Optional[str] = None) -> str:
    """Normalize and clean URL."""
    if not url:
        return ""
    
    url = url.strip()
    
    # Handle protocol-relative URLs
    if url.startswith('//'):
        url = 'https:' + url
    
    # Handle relative URLs
    elif url.startswith('/') and base_url:
        url = urljoin(base_url, url)
    
    # Ensure protocol
    elif not url.startswith(('http://', 'https://')):
        if base_url:
            url = urljoin(base_url, url)
        else:
            url = 'https://' + url
    
    return url


def extract_domain(url: str) -> Optional[str]:
    """Extract domain from URL."""
    try:
        parsed = urlparse(url)
        return parsed.netloc
    except:
        return None


def is_valid_url(url: str) -> bool:
    """Check if URL is valid."""
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except:
        return False


def clean_html_content(html_content: str, preserve_tags: List[str] = None) -> str:
    """Clean HTML content while preserving specified tags."""
    if not html_content:
        return ""
    
    if preserve_tags is None:
        preserve_tags = ['p', 'br', 'strong', 'em', 'b', 'i', 'u', 'a', 'img']
    
    # Remove script and style tags
    html_content = re.sub(r'<script[^>]*>.*?</script>', '', html_content, flags=re.DOTALL | re.IGNORECASE)
    html_content = re.sub(r'<style[^>]*>.*?</style>', '', html_content, flags=re.DOTALL | re.IGNORECASE)
    
    # Remove unsafe tags
    unsafe_tags = ['iframe', 'object', 'embed', 'form', 'input', 'button']
    for tag in unsafe_tags:
        html_content = re.sub(f'<{tag}[^>]*>.*?</{tag}>', '', html_content, flags=re.DOTALL | re.IGNORECASE)
        html_content = re.sub(f'<{tag}[^>]*/?>', '', html_content, flags=re.IGNORECASE)
    
    # Clean attributes (remove event handlers, etc.)
    html_content = re.sub(r'\s+on\w+\s*=\s*["\'][^"\']*["\']', '', html_content, flags=re.IGNORECASE)
    html_content = re.sub(r'\s+javascript\s*:', '', html_content, flags=re.IGNORECASE)
    
    return html_content.strip()


def truncate_text(text: str, max_length: int, suffix: str = "...") -> str:
    """Truncate text to specified length."""
    if len(text) <= max_length:
        return text
    
    # Try to break at word boundary
    truncated = text[:max_length - len(suffix)]
    last_space = truncated.rfind(' ')
    
    if last_space > max_length * 0.8:  # If we can break at a reasonable word boundary
        truncated = truncated[:last_space]
    
    return truncated + suffix


def normalize_whitespace(text: str) -> str:
    """Normalize whitespace in text."""
    if not text:
        return ""
    
    # Replace multiple spaces with single space
    text = re.sub(r'\s+', ' ', text)
    # Remove leading/trailing whitespace
    text = text.strip()
    
    return text


def extract_meta_tags(html_content: str) -> Dict[str, str]:
    """Extract meta tags from HTML content."""
    meta_tags = {}
    
    if not html_content:
        return meta_tags
    
    # Find meta tags
    meta_pattern = r'<meta\s+([^>]+)>'
    meta_matches = re.findall(meta_pattern, html_content, re.IGNORECASE)
    
    for match in meta_matches:
        # Extract name/content or property/content
        name_match = re.search(r'name\s*=\s*["\']([^"\']+)["\']', match, re.IGNORECASE)
        property_match = re.search(r'property\s*=\s*["\']([^"\']+)["\']', match, re.IGNORECASE)
        content_match = re.search(r'content\s*=\s*["\']([^"\']+)["\']', match, re.IGNORECASE)
        
        if content_match:
            content = content_match.group(1)
            
            if name_match:
                name = name_match.group(1).lower()
                meta_tags[name] = content
            elif property_match:
                property_name = property_match.group(1).lower()
                meta_tags[property_name] = content
    
    return meta_tags


def create_backup(file_path: str, backup_dir: str = None) -> Optional[str]:
    """Create a backup of the file."""
    try:
        if not backup_dir:
            backup_dir = os.path.dirname(file_path)
        
        backup_dir = Path(backup_dir)
        backup_dir.mkdir(exist_ok=True)
        
        filename = Path(file_path).name
        timestamp = int(os.path.getmtime(file_path))
        backup_name = f"{filename}.backup.{timestamp}"
        backup_path = backup_dir / backup_name
        
        import shutil
        shutil.copy2(file_path, backup_path)
        
        return str(backup_path)
    
    except Exception as e:
        print(f"Warning: Could not create backup: {e}")
        return None


def format_file_size(size_bytes: int) -> str:
    """Format file size in human-readable format."""
    if size_bytes == 0:
        return "0 B"
    
    size_names = ["B", "KB", "MB", "GB", "TB"]
    i = 0
    while size_bytes >= 1024 and i < len(size_names) - 1:
        size_bytes /= 1024.0
        i += 1
    
    return f"{size_bytes:.1f} {size_names[i]}"


def estimate_processing_time(file_size_mb: float, posts_count: int) -> str:
    """Estimate processing time based on file size and post count."""
    # Rough estimates based on typical performance
    time_per_mb = 0.1  # seconds per MB
    time_per_post = 0.05  # seconds per post
    
    total_time = (file_size_mb * time_per_mb) + (posts_count * time_per_post)
    
    if total_time < 60:
        return f"{total_time:.1f} seconds"
    elif total_time < 3600:
        return f"{total_time/60:.1f} minutes"
    else:
        return f"{total_time/3600:.1f} hours"
