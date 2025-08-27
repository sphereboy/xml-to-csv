"""
Framer-specific CSV formatting for blog content import.
"""

import csv
import io
from typing import Dict, List, Any, Optional
from datetime import datetime
from dateutil import parser as date_parser


class FramerFormatter:
    """Formats blog data into Framer-compatible CSV format."""
    
    # Framer Blog CMS required columns
    REQUIRED_COLUMNS = [
        "Title",
        "Slug", 
        "Content",
        "Excerpt",
        "Author",
        "Published Date",
        "Featured Image",
        "Categories",
        "Tags",
        "Status",
        "SEO Title",
        "SEO Description"
    ]
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.output_encoding = config.get('output_encoding', 'utf-8')
        self.generate_slugs = config.get('generate_slugs', True)
        self.slug_max_length = config.get('slug_max_length', 60)
        
    def format_blog_post(self, post_data: Dict[str, Any], content_processor) -> Dict[str, str]:
        """Format a single blog post for Framer CSV output."""
        formatted_post = {}
        
        # Title
        formatted_post["Title"] = self._format_title(post_data.get('title', ''))
        
        # Slug
        slug = post_data.get('slug', '')
        if not slug and self.generate_slugs:
            slug = content_processor.generate_slug(
                formatted_post["Title"], 
                self.slug_max_length
            )
        formatted_post["Slug"] = slug
        
        # Content
        formatted_post["Content"] = content_processor.process_content(
            post_data.get('content', ''), 
            'content'
        )
        
        # Excerpt
        excerpt = post_data.get('excerpt', '')
        if not excerpt and formatted_post["Content"]:
            # Generate excerpt from content if not provided
            excerpt = self._generate_excerpt(formatted_post["Content"])
        formatted_post["Excerpt"] = content_processor.process_content(excerpt, 'excerpt')
        
        # Author
        formatted_post["Author"] = content_processor.process_author(
            post_data.get('author', '')
        )
        
        # Published Date
        formatted_post["Published Date"] = self._format_date(
            post_data.get('date', ''),
            post_data.get('date_formats', [])
        )
        
        # Featured Image
        formatted_post["Featured Image"] = self._format_image_url(
            post_data.get('featured_image', '')
        )
        
        # Categories
        categories = post_data.get('categories', [])
        if isinstance(categories, str):
            categories = [categories]
        formatted_post["Categories"] = content_processor.normalize_categories(categories)
        
        # Tags
        tags = post_data.get('tags', [])
        if isinstance(tags, str):
            tags = [tags]
        formatted_post["Tags"] = content_processor.normalize_tags(tags)
        
        # Status
        status = post_data.get('status', '')
        status_mapping = post_data.get('status_mapping', {})
        formatted_post["Status"] = content_processor.process_status(status, status_mapping)
        
        # SEO Title
        seo_title = post_data.get('seo_title', '')
        if not seo_title:
            seo_title = formatted_post["Title"]
        formatted_post["SEO Title"] = content_processor.process_content(seo_title, 'title')
        
        # SEO Description
        seo_description = post_data.get('seo_description', '')
        if not seo_description:
            seo_description = formatted_post["Excerpt"]
        formatted_post["SEO Description"] = content_processor.process_content(
            seo_description, 'excerpt'
        )
        
        return formatted_post
    
    def _format_title(self, title: str) -> str:
        """Format and clean title."""
        if not title:
            return "Untitled Post"
        
        # Remove HTML tags
        title = title.replace('<', '&lt;').replace('>', '&gt;')
        # Normalize whitespace
        title = ' '.join(title.split())
        return title.strip()
    
    def _generate_excerpt(self, content: str, max_length: int = 300) -> str:
        """Generate excerpt from content if not provided."""
        # Strip HTML tags for excerpt
        import re
        clean_content = re.sub(r'<[^>]+>', '', content)
        
        # Take first few sentences
        sentences = clean_content.split('.')
        excerpt = ""
        
        for sentence in sentences:
            if len(excerpt + sentence + '.') <= max_length:
                excerpt += sentence + '.'
            else:
                break
        
        if not excerpt:
            excerpt = clean_content[:max_length-3] + "..."
        
        return excerpt.strip()
    
    def _format_date(self, date_str: str, date_formats: List[str] = None) -> str:
        """Format date to Framer-compatible format (YYYY-MM-DD)."""
        if not date_str:
            return datetime.now().strftime("%Y-%m-%d")
        
        # Try to parse the date
        try:
            # First try dateutil parser
            parsed_date = date_parser.parse(date_str)
            return parsed_date.strftime("%Y-%m-%d")
        except:
            pass
        
        # Try specific formats if provided
        if date_formats:
            for fmt in date_formats:
                try:
                    parsed_date = datetime.strptime(date_str, fmt)
                    return parsed_date.strftime("%Y-%m-%d")
                except:
                    continue
        
        # Fallback to current date
        print(f"Warning: Could not parse date '{date_str}', using current date")
        return datetime.now().strftime("%Y-%m-%d")
    
    def _format_image_url(self, image_url: str) -> str:
        """Format and validate image URL."""
        if not image_url:
            return ""
        
        # Clean URL
        image_url = image_url.strip()
        
        # Handle relative URLs
        if image_url.startswith('//'):
            image_url = 'https:' + image_url
        elif image_url.startswith('/'):
            # This would need base URL from config
            pass
        
        return image_url
    
    def write_csv(self, posts: List[Dict[str, str]], output_file: str) -> None:
        """Write formatted posts to CSV file."""
        with open(output_file, 'w', newline='', encoding=self.output_encoding) as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=self.REQUIRED_COLUMNS)
            
            # Write header
            writer.writeheader()
            
            # Write posts
            for post in posts:
                writer.writerow(post)
    
    def write_csv_to_string(self, posts: List[Dict[str, str]]) -> str:
        """Write formatted posts to string and return."""
        output = io.StringIO()
        writer = csv.DictWriter(output, fieldnames=self.REQUIRED_COLUMNS)
        
        # Write header
        writer.writeheader()
        
        # Write posts
        for post in posts:
            writer.writerow(post)
        
        return output.getvalue()
    
    def validate_csv_data(self, posts: List[Dict[str, str]]) -> Dict[str, Any]:
        """Validate CSV data for Framer compatibility."""
        validation_result = {
            "valid": True,
            "errors": [],
            "warnings": [],
            "stats": {
                "total_posts": len(posts),
                "published_posts": 0,
                "draft_posts": 0,
                "posts_with_images": 0,
                "posts_with_categories": 0,
                "posts_with_tags": 0
            }
        }
        
        if not posts:
            validation_result["errors"].append("No posts to validate")
            validation_result["valid"] = False
            return validation_result
        
        # Check each post
        for i, post in enumerate(posts):
            post_num = i + 1
            
            # Check required fields
            for field in self.REQUIRED_COLUMNS:
                if field not in post:
                    validation_result["errors"].append(
                        f"Post {post_num}: Missing required field '{field}'"
                    )
                    validation_result["valid"] = False
            
            # Check content length
            content = post.get("Content", "")
            if len(content) > 100000:
                validation_result["warnings"].append(
                    f"Post {post_num}: Content is very long ({len(content)} characters)"
                )
            
            # Check title length
            title = post.get("Title", "")
            if len(title) > 200:
                validation_result["warnings"].append(
                    f"Post {post_num}: Title is very long ({len(title)} characters)"
                )
            
            # Check excerpt length
            excerpt = post.get("Excerpt", "")
            if len(excerpt) > 500:
                validation_result["warnings"].append(
                    f"Post {post_num}: Excerpt is very long ({len(excerpt)} characters)"
                )
            
            # Update stats
            if post.get("Status") == "Published":
                validation_result["stats"]["published_posts"] += 1
            else:
                validation_result["stats"]["draft_posts"] += 1
            
            if post.get("Featured Image"):
                validation_result["stats"]["posts_with_images"] += 1
            
            if post.get("Categories"):
                validation_result["stats"]["posts_with_categories"] += 1
            
            if post.get("Tags"):
                validation_result["stats"]["posts_with_tags"] += 1
        
        return validation_result
    
    def get_csv_preview(self, posts: List[Dict[str, str]], max_posts: int = 5) -> str:
        """Get a preview of the CSV output."""
        if not posts:
            return "No posts to preview"
        
        preview_posts = posts[:max_posts]
        preview_csv = self.write_csv_to_string(preview_posts)
        
        # Add summary
        summary = f"Preview of first {len(preview_posts)} posts:\n"
        summary += f"Total posts: {len(posts)}\n"
        summary += f"CSV columns: {', '.join(self.REQUIRED_COLUMNS)}\n\n"
        
        return summary + preview_csv
