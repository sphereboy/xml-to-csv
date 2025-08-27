#!/usr/bin/env python3
"""
Setup script for Framer Blog XML to CSV Converter
"""

from setuptools import setup, find_packages
import os

# Read the README file
def read_readme():
    readme_path = os.path.join(os.path.dirname(__file__), 'README.md')
    if os.path.exists(readme_path):
        with open(readme_path, 'r', encoding='utf-8') as f:
            return f.read()
    return "Framer Blog XML to CSV Converter"

# Read requirements
def read_requirements():
    req_path = os.path.join(os.path.dirname(__file__), 'requirements.txt')
    if os.path.exists(req_path):
        with open(req_path, 'r', encoding='utf-8') as f:
            return [line.strip() for line in f if line.strip() and not line.startswith('#')]
    return []

setup(
    name="framer-blog-converter",
    version="1.0.0",
    description="Convert blog XML exports to Framer-compatible CSV format",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    author="Your Name",
    author_email="your.email@example.com",
    url="https://github.com/yourusername/framer-blog-converter",
    packages=find_packages(),
    include_package_data=True,
    package_data={
        'framer_blog_converter': [
            'templates/*.json',
            'tests/sample_data/*.xml'
        ]
    },
    install_requires=read_requirements(),
    extras_require={
        'dev': [
            'pytest>=6.0',
            'pytest-cov>=2.0',
            'black>=21.0',
            'flake8>=3.8',
            'mypy>=0.800'
        ]
    },
    entry_points={
        'console_scripts': [
            'framer-blog-converter=framer_blog_converter.src.cli:main',
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Text Processing :: Markup :: XML",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Internet :: WWW/HTTP :: Site Management",
    ],
    python_requires=">=3.8",
    keywords="framer, blog, xml, csv, converter, wordpress, ghost, jekyll",
    project_urls={
        "Bug Reports": "https://github.com/yourusername/framer-blog-converter/issues",
        "Source": "https://github.com/yourusername/framer-blog-converter",
        "Documentation": "https://github.com/yourusername/framer-blog-converter#readme",
    },
)
