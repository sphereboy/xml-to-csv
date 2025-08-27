"""
Configuration and mapping definitions for different blog platforms.
"""

import json
import os
from pathlib import Path
from typing import Dict, Any, Optional
from pydantic import BaseModel, Field


class PlatformMapping(BaseModel):
    """Configuration for a specific blog platform."""
    name: str
    description: str
    item_tag: str  # XML tag that contains each blog post
    field_mappings: Dict[str, str]  # XML path -> CSV column mapping
    date_formats: list[str] = Field(default_factory=list)
    status_mapping: Dict[str, str] = Field(default_factory=dict)
    content_field: str = "content"
    excerpt_field: Optional[str] = None
    author_field: Optional[str] = None
    date_field: Optional[str] = None
    image_field: Optional[str] = None
    category_field: Optional[str] = None
    tag_field: Optional[str] = None


class ConverterConfig(BaseModel):
    """Main configuration for the converter."""
    output_encoding: str = "utf-8"
    preserve_html: bool = True
    strip_html_tags: list[str] = Field(default_factory=list)
    max_content_length: Optional[int] = None
    generate_slugs: bool = True
    slug_max_length: int = 60
    handle_cdata: bool = True
    validate_urls: bool = False
    download_images: bool = False
    image_download_path: Optional[str] = None


class ConfigManager:
    """Manages configuration and platform mappings."""
    
    def __init__(self, templates_dir: Optional[str] = None):
        self.templates_dir = Path(templates_dir) if templates_dir else Path(__file__).parent.parent / "templates"
        self.platforms: Dict[str, PlatformMapping] = {}
        self.config = ConverterConfig()
        self._load_platform_templates()
    
    def _load_platform_templates(self):
        """Load all platform template files."""
        if not self.templates_dir.exists():
            return
        
        for template_file in self.templates_dir.glob("*.json"):
            try:
                with open(template_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    platform_name = template_file.stem
                    self.platforms[platform_name] = PlatformMapping(**data)
            except Exception as e:
                print(f"Warning: Could not load template {template_file}: {e}")
    
    def get_platform_mapping(self, platform_name: str) -> Optional[PlatformMapping]:
        """Get platform mapping by name."""
        return self.platforms.get(platform_name.lower())
    
    def list_platforms(self) -> list[str]:
        """List all available platforms."""
        return list(self.platforms.keys())
    
    def add_custom_mapping(self, name: str, mapping: PlatformMapping):
        """Add a custom platform mapping."""
        self.platforms[name.lower()] = mapping
    
    def save_custom_mapping(self, name: str, mapping: PlatformMapping):
        """Save a custom mapping to a JSON file."""
        custom_dir = self.templates_dir / "custom"
        custom_dir.mkdir(exist_ok=True)
        
        file_path = custom_dir / f"{name}.json"
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(mapping.dict(), f, indent=2, ensure_ascii=False)
        
        self.platforms[name.lower()] = mapping


# Default platform mappings
DEFAULT_PLATFORMS = {
    "wordpress": PlatformMapping(
        name="WordPress",
        description="WordPress XML export format",
        item_tag="item",
        field_mappings={
            "title": "title",
            "content": "{http://purl.org/rss/1.0/modules/content/}encoded",
            "excerpt": "{http://wordpress.org/export/1.2/excerpt/}encoded",
            "author": "{http://purl.org/dc/elements/1.1/}creator",
            "date": "pubDate",
            "status": "{http://wordpress.org/export/1.2/}status",
            "categories": "category",
            "tags": "post_tag",
            "featured_image": "{http://wordpress.org/export/1.2/}attachment_url",
            "slug": "{http://wordpress.org/export/1.2/}post_name",
            "seo_title": "yoast_wpseo_title",
            "seo_description": "yoast_wpseo_metadesc"
        },
        date_formats=["%a, %d %b %Y %H:%M:%S %z", "%Y-%m-%d %H:%M:%S"],
        status_mapping={
            "publish": "Published",
            "draft": "Draft",
            "private": "Draft",
            "pending": "Draft"
        },
        content_field="{http://purl.org/rss/1.0/modules/content/}encoded",
        excerpt_field="{http://wordpress.org/export/1.2/excerpt/}encoded",
        author_field="{http://purl.org/dc/elements/1.1/}creator",
        date_field="pubDate",
        image_field="{http://wordpress.org/export/1.2/}attachment_url",
        category_field="category",
        tag_field="post_tag"
    ),
    
    "ghost": PlatformMapping(
        name="Ghost",
        description="Ghost JSON export format (converted to XML)",
        item_tag="post",
        field_mappings={
            "title": "title",
            "content": "html",
            "excerpt": "excerpt",
            "author": "author",
            "date": "published_at",
            "status": "status",
            "tags": "tags",
            "slug": "slug",
            "featured_image": "feature_image"
        },
        date_formats=["%Y-%m-%dT%H:%M:%S.%fZ", "%Y-%m-%d %H:%M:%S"],
        status_mapping={
            "published": "Published",
            "draft": "Draft"
        },
        content_field="html",
        excerpt_field="excerpt",
        author_field="author",
        date_field="published_at",
        image_field="feature_image",
        tag_field="tags"
    ),
    
    "jekyll": PlatformMapping(
        name="Jekyll",
        description="Jekyll front matter and markdown",
        item_tag="post",
        field_mappings={
            "title": "title",
            "content": "content",
            "excerpt": "excerpt",
            "author": "author",
            "date": "date",
            "categories": "categories",
            "tags": "tags",
            "slug": "slug",
            "featured_image": "image"
        },
        date_formats=["%Y-%m-%d", "%Y-%m-%d %H:%M:%S"],
        status_mapping={
            "published": "Published",
            "draft": "Draft"
        },
        content_field="content",
        excerpt_field="excerpt",
        author_field="author",
        date_field="date",
        image_field="image",
        category_field="categories",
        tag_field="tags"
    )
}
