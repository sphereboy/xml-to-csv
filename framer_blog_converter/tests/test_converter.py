"""
Basic tests for the Framer Blog XML to CSV converter.
"""

import os
import tempfile
import unittest
from pathlib import Path

# Add src to path for imports
import sys
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from blog_converter import FramerBlogConverter
from config import ConfigManager, PlatformMapping


class TestFramerBlogConverter(unittest.TestCase):
    """Test cases for the main converter class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.converter = FramerBlogConverter()
        self.sample_xml = Path(__file__).parent / 'sample_data' / 'sample_wordpress.xml'
    
    def test_platform_detection(self):
        """Test platform auto-detection."""
        if self.sample_xml.exists():
            platform = self.converter.detect_platform(str(self.sample_xml))
            self.assertEqual(platform, 'wordpress')
    
    def test_platform_loading(self):
        """Test platform template loading."""
        success = self.converter.load_platform_template('wordpress')
        self.assertTrue(success)
        self.assertIsNotNone(self.converter.current_mapping)
        self.assertEqual(self.converter.current_mapping.name, 'WordPress')
    
    def test_available_platforms(self):
        """Test listing available platforms."""
        platforms = self.converter.list_available_platforms()
        self.assertIn('wordpress', platforms)
        self.assertIn('ghost', platforms)
        self.assertIn('jekyll', platforms)
    
    def test_content_processing_config(self):
        """Test content processing configuration."""
        self.converter.set_content_processing(
            preserve_html=False,
            max_content_length=1000
        )
        
        config = self.converter.config_manager.config
        self.assertFalse(config.preserve_html)
        self.assertEqual(config.max_content_length, 1000)
    
    def test_file_stats(self):
        """Test file statistics generation."""
        if self.sample_xml.exists():
            stats = self.converter.get_conversion_stats(str(self.sample_xml))
            self.assertNotIn('error', stats)
            self.assertEqual(stats['platform_detected'], 'wordpress')
            self.assertGreater(stats['total_posts'], 0)


class TestConfigManager(unittest.TestCase):
    """Test cases for configuration management."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.config_manager = ConfigManager()
    
    def test_default_platforms(self):
        """Test default platform loading."""
        platforms = self.config_manager.list_platforms()
        self.assertIn('wordpress', platforms)
        self.assertIn('ghost', platforms)
        self.assertIn('jekyll', platforms)
    
    def test_platform_mapping(self):
        """Test platform mapping retrieval."""
        mapping = self.config_manager.get_platform_mapping('wordpress')
        self.assertIsNotNone(mapping)
        self.assertEqual(mapping.name, 'WordPress')
        self.assertEqual(mapping.item_tag, 'item')
    
    def test_custom_mapping(self):
        """Test custom platform mapping."""
        custom_mapping = PlatformMapping(
            name="Custom Blog",
            description="Test custom blog",
            item_tag="post",
            field_mappings={"title": "title", "content": "body"}
        )
        
        self.config_manager.add_custom_mapping('custom', custom_mapping)
        retrieved = self.config_manager.get_platform_mapping('custom')
        self.assertEqual(retrieved.name, 'Custom Blog')


class TestContentProcessing(unittest.TestCase):
    """Test cases for content processing."""
    
    def setUp(self):
        """Set up test fixtures."""
        from content_processor import ContentProcessor
        self.processor = ContentProcessor({
            'preserve_html': True,
            'handle_cdata': True
        })
    
    def test_cdata_extraction(self):
        """Test CDATA section extraction."""
        content = '<![CDATA[<p>Test content</p>]]>'
        processed = self.processor.process_content(content, 'content')
        self.assertIn('<p>Test content</p>', processed)
    
    def test_html_preservation(self):
        """Test HTML preservation."""
        content = '<p>Test <strong>bold</strong> content</p>'
        processed = self.processor.process_content(content, 'content')
        self.assertIn('<p>', processed)
        self.assertIn('<strong>', processed)
    
    def test_slug_generation(self):
        """Test URL slug generation."""
        title = "Test Blog Post Title!"
        slug = self.processor.generate_slug(title)
        self.assertEqual(slug, 'test-blog-post-title')
    
    def test_content_validation(self):
        """Test content length validation."""
        short_content = "Short content"
        long_content = "Long content " * 1000
        
        short_validation = self.processor.validate_content_length(short_content, 'content')
        long_validation = self.processor.validate_content_length(long_content, 'content')
        
        self.assertTrue(short_validation['valid'])
        self.assertFalse(long_validation['valid'])


if __name__ == '__main__':
    unittest.main()
