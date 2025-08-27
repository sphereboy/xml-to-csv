"""
Content processing utilities for blog content conversion.
"""

import re
import html
import unicodedata
from typing import Optional, List, Dict, Any
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup, NavigableString, Tag


class ContentProcessor:
    """Processes and sanitizes blog content for Framer compatibility."""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.preserve_html = config.get('preserve_html', True)
        self.strip_html_tags = config.get('strip_html_tags', [])
        self.max_content_length = config.get('max_content_length')
        self.handle_cdata = config.get('handle_cdata', True)
        self.validate_urls = config.get('validate_urls', False)
        
        # HTML tags to always remove for safety
        self.unsafe_tags = {'script', 'style', 'iframe', 'object', 'embed', 'form', 'input'}
        
        # Tags to preserve but clean
        self.preserve_tags = {'p', 'div', 'span', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 
                             'strong', 'b', 'em', 'i', 'u', 'a', 'img', 'ul', 'ol', 'li',
                             'blockquote', 'code', 'pre', 'br', 'hr', 'table', 'tr', 'td', 'th'}
    
    def process_content(self, content: str, content_type: str = "content") -> str:
        """Process content based on type and configuration."""
        if not content:
            return ""
        
        # Handle CDATA sections
        if self.handle_cdata:
            content = self._extract_cdata(content)
        
        # Decode HTML entities
        content = html.unescape(content)
        
        # Process based on content type
        if content_type == "excerpt":
            return self._process_excerpt(content)
        elif content_type == "title":
            return self._process_title(content)
        else:
            return self._process_main_content(content)
    
    def _extract_cdata(self, content: str) -> str:
        """Extract content from CDATA sections."""
        cdata_pattern = r'<!\[CDATA\[(.*?)\]\]>'
        matches = re.findall(cdata_pattern, content, re.DOTALL)
        if matches:
            return matches[0]
        return content
    
    def _process_title(self, title: str) -> str:
        """Process and clean title content."""
        # Remove HTML tags
        title = self._strip_html_tags(title)
        # Normalize whitespace
        title = ' '.join(title.split())
        # Remove special characters that might cause issues
        title = re.sub(r'[^\w\s\-_.,!?()]', '', title)
        return title.strip()
    
    def _process_excerpt(self, excerpt: str) -> str:
        """Process excerpt content."""
        # Strip HTML for excerpt
        excerpt = self._strip_html_tags(excerpt)
        # Limit length
        if len(excerpt) > 300:
            excerpt = excerpt[:297] + "..."
        return excerpt.strip()
    
    def _process_main_content(self, content: str) -> str:
        """Process main content with HTML preservation options."""
        if not self.preserve_html:
            return self._strip_html_tags(content)
        
        # Parse HTML and clean it
        soup = BeautifulSoup(content, 'html.parser')
        
        # Remove unsafe tags
        for tag in soup.find_all(self.unsafe_tags):
            tag.decompose()
        
        # Clean and normalize HTML
        self._clean_html_tags(soup)
        
        # Handle images
        self._process_images(soup)
        
        # Handle links
        self._process_links(soup)
        
        # Convert back to string
        processed_content = str(soup)
        
        # Check content length
        if self.max_content_length and len(processed_content) > self.max_content_length:
            print(f"Warning: Content exceeds maximum length ({self.max_content_length} chars)")
        
        return processed_content
    
    def _strip_html_tags(self, content: str) -> str:
        """Strip HTML tags from content."""
        # Remove HTML tags
        content = re.sub(r'<[^>]+>', '', content)
        # Decode HTML entities
        content = html.unescape(content)
        # Normalize whitespace
        content = ' '.join(content.split())
        return content
    
    def _clean_html_tags(self, soup: BeautifulSoup):
        """Clean and normalize HTML tags."""
        for tag in soup.find_all():
            # Remove empty tags
            if tag.string is None and not tag.contents:
                tag.decompose()
                continue
            
            # Clean attributes
            if tag.attrs:
                # Keep only safe attributes
                safe_attrs = {}
                for attr, value in tag.attrs.items():
                    if self._is_safe_attribute(attr, value):
                        safe_attrs[attr] = value
                tag.attrs = safe_attrs
            
            # Normalize tag names
            if tag.name not in self.preserve_tags:
                # Convert to span if not in preserve list
                tag.name = 'span'
    
    def _is_safe_attribute(self, attr: str, value: str) -> bool:
        """Check if an HTML attribute is safe."""
        safe_attrs = {
            'href', 'src', 'alt', 'title', 'class', 'id', 'style',
            'width', 'height', 'target', 'rel'
        }
        
        if attr not in safe_attrs:
            return False
        
        # Check for dangerous values
        dangerous_patterns = [
            r'javascript:', r'vbscript:', r'data:', r'file:',
            r'on\w+\s*=', r'<script', r'<iframe'
        ]
        
        for pattern in dangerous_patterns:
            if re.search(pattern, str(value), re.IGNORECASE):
                return False
        
        return True
    
    def _process_images(self, soup: BeautifulSoup):
        """Process and clean image tags."""
        for img in soup.find_all('img'):
            # Ensure src attribute exists
            if not img.get('src'):
                img.decompose()
                continue
            
            # Clean src attribute
            src = img.get('src', '')
            if src.startswith('//'):
                src = 'https:' + src
            elif src.startswith('/'):
                # Handle relative URLs - this would need base URL from config
                pass
            
            # Remove unsafe attributes
            unsafe_attrs = ['onload', 'onerror', 'onclick']
            for attr in unsafe_attrs:
                img.attrs.pop(attr, None)
            
            # Ensure alt text exists
            if not img.get('alt'):
                img['alt'] = 'Image'
    
    def _process_links(self, soup: BeautifulSoup):
        """Process and clean link tags."""
        for link in soup.find_all('a'):
            href = link.get('href', '')
            
            # Clean href
            if href.startswith('//'):
                link['href'] = 'https:' + href
            elif href.startswith('/'):
                # Handle relative URLs
                pass
            
            # Add rel="noopener" for external links
            if href.startswith('http') and not href.startswith('http://localhost'):
                link['rel'] = 'noopener'
                link['target'] = '_blank'
    
    def generate_slug(self, title: str, max_length: int = 60) -> str:
        """Generate URL-friendly slug from title."""
        # Convert to lowercase
        slug = title.lower()
        
        # Remove HTML tags
        slug = self._strip_html_tags(slug)
        
        # Replace spaces and special characters with hyphens
        slug = re.sub(r'[^\w\s-]', '', slug)
        slug = re.sub(r'[-\s]+', '-', slug)
        
        # Remove leading/trailing hyphens
        slug = slug.strip('-')
        
        # Limit length
        if len(slug) > max_length:
            slug = slug[:max_length].rstrip('-')
        
        return slug
    
    def normalize_categories(self, categories: List[str]) -> str:
        """Normalize and format categories."""
        if not categories:
            return ""
        
        # Clean each category
        cleaned_categories = []
        for category in categories:
            if isinstance(category, str):
                # Remove HTML tags
                clean_cat = self._strip_html_tags(category)
                # Normalize
                clean_cat = clean_cat.strip().title()
                if clean_cat and clean_cat not in cleaned_categories:
                    cleaned_categories.append(clean_cat)
        
        return ", ".join(cleaned_categories)
    
    def normalize_tags(self, tags: List[str]) -> str:
        """Normalize and format tags."""
        if not tags:
            return ""
        
        # Clean each tag
        cleaned_tags = []
        for tag in tags:
            if isinstance(tag, str):
                # Remove HTML tags
                clean_tag = self._strip_html_tags(tag)
                # Normalize
                clean_tag = clean_tag.strip().lower()
                if clean_tag and clean_tag not in cleaned_tags:
                    cleaned_tags.append(clean_tag)
        
        return ", ".join(cleaned_tags)
    
    def process_author(self, author: str) -> str:
        """Process and clean author information."""
        if not author:
            return ""
        
        # Remove HTML tags
        author = self._strip_html_tags(author)
        # Normalize whitespace
        author = ' '.join(author.split())
        # Remove special characters
        author = re.sub(r'[^\w\s\-_.]', '', author)
        
        return author.strip()
    
    def process_status(self, status: str, status_mapping: Dict[str, str]) -> str:
        """Process and map status values."""
        if not status:
            return "Draft"
        
        # Clean status
        status = status.strip().lower()
        
        # Map to Framer status
        return status_mapping.get(status, "Draft")
    
    def validate_content_length(self, content: str, content_type: str = "content") -> Dict[str, Any]:
        """Validate content length and provide warnings."""
        result = {
            "valid": True,
            "warnings": [],
            "length": len(content)
        }
        
        if content_type == "title" and len(content) > 100:
            result["warnings"].append("Title is very long (over 100 characters)")
        
        elif content_type == "excerpt" and len(content) > 300:
            result["warnings"].append("Excerpt is very long (over 300 characters)")
        
        elif content_type == "content":
            if len(content) > 10000:
                result["warnings"].append("Content is very long (over 10,000 characters)")
            elif len(content) > 50000:
                result["warnings"].append("Content is extremely long (over 50,000 characters)")
                result["valid"] = False
        
        return result
