"""
Core blog converter class for XML to CSV conversion.
"""

import os
import sys
from typing import Dict, List, Any, Optional, Generator, Iterator
from pathlib import Path
from lxml import etree
from tqdm import tqdm

from .config import ConfigManager, PlatformMapping, DEFAULT_PLATFORMS
from .content_processor import ContentProcessor
from .framer_formatter import FramerFormatter


class FramerBlogConverter:
    """Main converter class for blog XML to CSV conversion."""
    
    def __init__(self, config_file: Optional[str] = None):
        self.config_manager = ConfigManager()
        self.content_processor = None
        self.framer_formatter = None
        self.current_platform = None
        self.current_mapping = None
        
        # Load default platforms
        for name, mapping in DEFAULT_PLATFORMS.items():
            self.config_manager.add_custom_mapping(name, mapping)
        
        # Initialize processors
        self._initialize_processors()
        
        # Load custom config if provided
        if config_file:
            self.load_config(config_file)
    
    def _initialize_processors(self):
        """Initialize content processor and formatter with default config."""
        config = self.config_manager.config.dict()
        self.content_processor = ContentProcessor(config)
        self.framer_formatter = FramerFormatter(config)
    
    def load_config(self, config_file: str):
        """Load configuration from file."""
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                import json
                config_data = json.load(f)
                
                # Update config
                for key, value in config_data.items():
                    if hasattr(self.config_manager.config, key):
                        setattr(self.config_manager.config, key, value)
                
                # Reinitialize processors
                self._initialize_processors()
                
                print(f"Configuration loaded from {config_file}")
        except Exception as e:
            print(f"Warning: Could not load config file {config_file}: {e}")
    
    def load_platform_template(self, platform_name: str) -> bool:
        """Load a specific platform template."""
        mapping = self.config_manager.get_platform_mapping(platform_name)
        if mapping:
            self.current_platform = platform_name
            self.current_mapping = mapping
            print(f"Loaded platform template: {mapping.name}")
            return True
        else:
            print(f"Platform template '{platform_name}' not found")
            return False
    
    def list_available_platforms(self) -> List[str]:
        """List all available platform templates."""
        return self.config_manager.list_platforms()
    
    def set_content_processing(self, **kwargs):
        """Configure content processing options."""
        for key, value in kwargs.items():
            if hasattr(self.config_manager.config, key):
                setattr(self.config_manager.config, key, value)
        
        # Reinitialize processors
        self._initialize_processors()
    
    def convert(self, input_file: str, output_file: str, platform: Optional[str] = None) -> bool:
        """Convert XML file to CSV format."""
        if not os.path.exists(input_file):
            print(f"Error: Input file '{input_file}' not found")
            return False
        
        # Load platform if specified
        if platform and not self.load_platform_template(platform):
            return False
        
        if not self.current_mapping:
            print("Error: No platform template loaded. Use load_platform_template() first.")
            return False
        
        try:
            print(f"Converting {input_file} to {output_file}")
            print(f"Platform: {self.current_mapping.name}")
            
            # Parse XML and convert
            posts = list(self._parse_xml_stream(input_file))
            
            if not posts:
                print("No posts found in XML file")
                return False
            
            print(f"Found {len(posts)} posts")
            
            # Format posts for Framer
            formatted_posts = []
            for post in tqdm(posts, desc="Formatting posts"):
                formatted_post = self.framer_formatter.format_blog_post(
                    post, 
                    self.content_processor
                )
                formatted_posts.append(formatted_post)
            
            # Validate output
            validation = self.framer_formatter.validate_csv_data(formatted_posts)
            if not validation["valid"]:
                print("Validation errors found:")
                for error in validation["errors"]:
                    print(f"  - {error}")
                return False
            
            if validation["warnings"]:
                print("Validation warnings:")
                for warning in validation["warnings"]:
                    print(f"  - {warning}")
            
            # Write CSV
            self.framer_formatter.write_csv(formatted_posts, output_file)
            
            # Print statistics
            stats = validation["stats"]
            print(f"\nConversion completed successfully!")
            print(f"Total posts: {stats['total_posts']}")
            print(f"Published: {stats['published_posts']}")
            print(f"Drafts: {stats['draft_posts']}")
            print(f"With images: {stats['posts_with_images']}")
            print(f"With categories: {stats['posts_with_categories']}")
            print(f"With tags: {stats['posts_with_tags']}")
            
            return True
            
        except Exception as e:
            print(f"Error during conversion: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def preview(self, input_file: str, max_posts: int = 10, platform: Optional[str] = None) -> str:
        """Preview conversion without writing to file."""
        if not os.path.exists(input_file):
            return f"Error: Input file '{input_file}' not found"
        
        # Load platform if specified
        if platform and not self.load_platform_template(platform):
            return f"Error: Platform template '{platform}' not found"
        
        if not self.current_mapping:
            return "Error: No platform template loaded. Use load_platform_template() first."
        
        try:
            # Parse XML and convert limited posts
            posts = []
            for i, post in enumerate(self._parse_xml_stream(input_file)):
                if i >= max_posts:
                    break
                posts.append(post)
            
            if not posts:
                return "No posts found in XML file"
            
            # Format posts for preview
            formatted_posts = []
            for post in posts:
                formatted_post = self.framer_formatter.format_blog_post(
                    post, 
                    self.content_processor
                )
                formatted_posts.append(formatted_post)
            
            # Get preview
            preview = self.framer_formatter.get_csv_preview(formatted_posts, len(formatted_posts))
            
            return preview
            
        except Exception as e:
            return f"Error during preview: {e}"
    
    def _parse_xml_stream(self, input_file: str) -> Generator[Dict[str, Any], None, None]:
        """Parse XML file using streaming approach for memory efficiency."""
        try:
            # Use iterparse for memory-efficient parsing
            context = etree.iterparse(input_file, events=('end',), tag=self.current_mapping.item_tag)
            
            for event, elem in context:
                if elem.tag == self.current_mapping.item_tag:
                    post_data = self._extract_post_data(elem)
                    if post_data:
                        yield post_data
                    
                    # Clear element to free memory
                    elem.clear()
                    if elem.getprevious() is not None:
                        del elem.getparent()[0]
            
            del context
            
        except etree.XMLSyntaxError as e:
            print(f"XML parsing error: {e}")
            raise
        except Exception as e:
            print(f"Error parsing XML: {e}")
            raise
    
    def _extract_post_data(self, elem: etree._Element) -> Optional[Dict[str, Any]]:
        """Extract blog post data from XML element."""
        try:
            post_data = {}
            
            # Extract basic fields
            for field_name, xml_path in self.current_mapping.field_mappings.items():
                value = self._extract_field_value(elem, xml_path)
                if value is not None:
                    post_data[field_name] = value
            
            # Extract categories and tags (they might be multiple elements)
            if self.current_mapping.category_field:
                categories = self._extract_multiple_values(elem, self.current_mapping.category_field)
                if categories:
                    post_data['categories'] = categories
            
            if self.current_mapping.tag_field:
                tags = self._extract_multiple_values(elem, self.current_mapping.tag_field)
                if tags:
                    post_data['tags'] = tags
            
            # Add platform-specific data
            post_data['date_formats'] = self.current_mapping.date_formats
            post_data['status_mapping'] = self.current_mapping.status_mapping
            
            # Check if we have essential data
            if not post_data.get('title') and not post_data.get('content'):
                return None
            
            return post_data
            
        except Exception as e:
            print(f"Error extracting post data: {e}")
            return None
    
    def _extract_field_value(self, elem: etree._Element, xml_path: str) -> Optional[str]:
        """Extract value from XML element using path."""
        try:
            if xml_path.startswith('{') and '}' in xml_path:
                # Handle full namespace URLs like {http://...}tag
                end_brace = xml_path.find('}')
                namespace = xml_path[1:end_brace]
                tag = xml_path[end_brace + 1:]
                
                # Try direct find with namespace
                child = elem.find(f'.//{{{namespace}}}{tag}')
                if child is not None and child.text:
                    return child.text.strip()
                elif child is not None:
                    return ""
            elif ':' in xml_path:
                # Handle shorthand namespaces like content:encoded
                namespace, tag = xml_path.split(':', 1)
                # Try to find element with namespace
                for child in elem.iter():
                    if child.tag.endswith(f'{{{tag}}}'):
                        if child.text and child.text.strip():
                            return child.text.strip()
                        return ""
            else:
                # Simple tag name
                child = elem.find(xml_path)
                if child is not None and child.text:
                    return child.text.strip()
            
            return None
            
        except Exception as e:
            print(f"Error extracting field {xml_path}: {e}")
            return None
    
    def _extract_multiple_values(self, elem: etree._Element, tag_name: str) -> List[str]:
        """Extract multiple values for tags/categories."""
        try:
            values = []
            if ':' in tag_name:
                namespace, tag = tag_name.split(':', 1)
                # Find elements with namespace
                for child in elem.iter():
                    if child.tag.endswith(f'{{{tag}}}'):
                        if child.text and child.text.strip():
                            values.append(child.text.strip())
            else:
                # Simple tag name
                for child in elem.findall(tag_name):
                    if child.text and child.text.strip():
                        values.append(child.text.strip())
            
            return values
            
        except Exception as e:
            print(f"Error extracting multiple values for {tag_name}: {e}")
            return []
    
    def detect_platform(self, input_file: str) -> Optional[str]:
        """Attempt to auto-detect the platform from XML structure."""
        try:
            context = etree.iterparse(input_file, events=('start',))
            
            for event, elem in context:
                if elem.tag == 'rss':
                    return 'wordpress'
                elif elem.tag == 'ghost':
                    return 'ghost'
                elif elem.tag == 'jekyll':
                    return 'jekyll'
                elif elem.tag == 'blog':
                    return 'custom'
                break
            
            del context
            
            # Check for common patterns
            with open(input_file, 'r', encoding='utf-8') as f:
                content = f.read(1000)  # Read first 1000 chars
                if 'wp:post_type' in content:
                    return 'wordpress'
                elif 'ghost' in content.lower():
                    return 'ghost'
                elif 'jekyll' in content.lower():
                    return 'jekyll'
            
            return None
            
        except Exception as e:
            print(f"Error detecting platform: {e}")
            return None
    
    def get_conversion_stats(self, input_file: str) -> Dict[str, Any]:
        """Get statistics about the XML file without full conversion."""
        if not os.path.exists(input_file):
            return {"error": "File not found"}
        
        try:
            stats = {
                "total_posts": 0,
                "platform_detected": None,
                "file_size_mb": round(os.path.getsize(input_file) / (1024 * 1024), 2),
                "estimated_processing_time": "Unknown"
            }
            
            # Detect platform
            platform = self.detect_platform(input_file)
            stats["platform_detected"] = platform
            
            # Count posts
            if platform:
                self.load_platform_template(platform)
                if self.current_mapping:
                    context = etree.iterparse(input_file, events=('end',), tag=self.current_mapping.item_tag)
                    stats["total_posts"] = sum(1 for event, elem in context)
                    del context
                    
                    # Estimate processing time
                    if stats["total_posts"] > 0:
                        time_per_post = 0.1  # seconds
                        total_time = stats["total_posts"] * time_per_post
                        if total_time < 60:
                            stats["estimated_processing_time"] = f"{total_time:.1f} seconds"
                        else:
                            stats["estimated_processing_time"] = f"{total_time/60:.1f} minutes"
            
            return stats
            
        except Exception as e:
            return {"error": str(e)}
    
    def get_file_statistics(self, input_file: str) -> Dict[str, Any]:
        """Get file statistics - alias for get_conversion_stats for web compatibility."""
        return self.get_conversion_stats(input_file)
    
    def preview_posts(self, input_file: str, limit: int = 5) -> List[Dict[str, Any]]:
        """Preview the first N posts from the XML file without full conversion."""
        if not os.path.exists(input_file):
            return []
        
        if not self.current_mapping:
            # Try to auto-detect platform
            platform = self.detect_platform(input_file)
            if platform:
                self.load_platform_template(platform)
            else:
                return []
        
        if not self.current_mapping:
            return []
        
        try:
            preview_posts = []
            context = etree.iterparse(input_file, events=('end',), tag=self.current_mapping.item_tag)
            
            for event, elem in context:
                if len(preview_posts) >= limit:
                    break
                
                post_data = {}
                
                # Extract basic fields
                for field_name, xml_path in self.current_mapping.fields.items():
                    if xml_path:
                        value = self._extract_field(elem, xml_path)
                        if value:
                            post_data[field_name] = value
                
                # Extract tags/categories if available
                if hasattr(self.current_mapping, 'tags_field') and self.current_mapping.tags_field:
                    tags = self._extract_multiple_values(elem, self.current_mapping.tags_field)
                    if tags:
                        post_data['tags'] = tags
                
                if hasattr(self.current_mapping, 'categories_field') and self.current_mapping.categories_field:
                    categories = self._extract_multiple_values(elem, self.current_mapping.categories_field)
                    if categories:
                        post_data['categories'] = categories
                
                if post_data:
                    preview_posts.append(post_data)
                
                # Clean up element to free memory
                elem.clear()
            
            del context
            return preview_posts
            
        except Exception as e:
            print(f"Error previewing posts: {e}")
            return []
