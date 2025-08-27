# 🌐 Framer Blog XML to CSV Converter - Web Interface

A modern, user-friendly web application that allows users to convert their blog XML exports to Framer-compatible CSV format through a beautiful browser interface.

## ✨ Features

- **Drag & Drop Interface**: Simply drag and drop your XML file to get started
- **Multiple Platform Support**: WordPress, Ghost, Jekyll, and Squarespace
- **Real-time Analysis**: Get instant feedback on your file format and content
- **Progress Tracking**: Visual progress bar during conversion
- **Smart Platform Detection**: Automatically detects your blog platform
- **Content Processing Options**: Choose how to handle HTML content
- **Instant Download**: Get your converted CSV file immediately
- **Responsive Design**: Works perfectly on desktop and mobile devices

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

### Installation

1. **Clone or download the project**:
   ```bash
   cd framer_blog_converter
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the web application**:
   ```bash
   python run_web.py
   ```

4. **Open your browser** and go to:
   ```
   http://localhost:5000
   ```

## 🎯 How to Use

### Step 1: Upload Your File
- Drag and drop your XML file onto the upload zone, or click "Choose File"
- Supported formats: XML files up to 50MB
- The app will automatically analyze your file and detect the platform

### Step 2: Configure Options
- **Platform**: Select your blog platform (WordPress, Ghost, Jekyll, or Squarespace)
- **Content Processing**: Choose how to handle HTML content
  - Preserve HTML: Keep formatting intact
  - Strip HTML: Remove all HTML tags for clean text

### Step 3: Convert
- Click "Convert to CSV" to start the conversion process
- Watch the progress bar as your file is processed
- Get instant feedback on the conversion results

### Step 4: Download
- Once conversion is complete, click "Download CSV"
- Your Framer-ready CSV file will be saved to your computer
- Use "New Conversion" to process another file

## 🔧 Supported Platforms

| Platform | Description | Auto-Detection |
|----------|-------------|----------------|
| **WordPress** | Standard WordPress XML exports | ✅ Yes |
| **Ghost** | Ghost blog exports | ✅ Yes |
| **Jekyll** | Jekyll static site exports | ✅ Yes |
| **Squarespace** | Squarespace WordPress-compatible exports | ✅ Yes |

## 📱 Browser Compatibility

- ✅ Chrome 80+
- ✅ Firefox 75+
- ✅ Safari 13+
- ✅ Edge 80+
- ✅ Mobile browsers (iOS Safari, Chrome Mobile)

## 🛠️ Technical Details

### Architecture
- **Backend**: Flask web framework
- **Frontend**: Modern HTML5 with Tailwind CSS
- **File Handling**: Secure file uploads with size validation
- **Session Management**: Flask sessions for user state
- **Error Handling**: Comprehensive error reporting and user feedback

### Security Features
- File type validation (XML only)
- File size limits (50MB max)
- Secure filename handling
- Temporary file cleanup
- Session-based file management

### Performance
- Asynchronous file processing
- Progress tracking with real-time updates
- Efficient memory usage
- Automatic cleanup of temporary files

## 🚨 Troubleshooting

### Common Issues

**"File upload failed"**
- Check file size (must be under 50MB)
- Ensure file is in XML format
- Check internet connection

**"Conversion failed"**
- Verify XML file is not corrupted
- Try selecting a different platform
- Check if the XML structure is supported

**"Platform not detected"**
- Try manual platform selection
- Check XML file format
- Some custom exports may need manual configuration

### Getting Help

1. **Check the file format**: Ensure your XML file is a standard blog export
2. **Try different platforms**: Some exports work better with specific platform settings
3. **File size**: Large files may take longer to process
4. **Browser issues**: Try refreshing the page or using a different browser

## 🔄 Development

### Running in Development Mode
```bash
python run_web.py
```

### Running in Production
```bash
export SECRET_KEY="your-secret-key-here"
export FLASK_ENV=production
python run_web.py
```

### Customizing the Interface
- Templates are located in `templates/`
- CSS uses Tailwind CSS framework
- JavaScript is vanilla ES6+ (no frameworks)

## 📊 File Size Guidelines

| File Size | Processing Time | Recommendation |
|-----------|----------------|----------------|
| < 1MB | < 10 seconds | ✅ Excellent |
| 1-10MB | 10-60 seconds | ✅ Good |
| 10-25MB | 1-5 minutes | ⚠️ Be patient |
| 25-50MB | 5-15 minutes | ⚠️ Large file, may take time |
| > 50MB | Not supported | ❌ File too large |

## 🌟 Pro Tips

1. **Best Results**: Use the platform that matches your export source
2. **Content Quality**: Choose HTML preservation for rich content, stripping for clean text
3. **File Preparation**: Ensure your XML export is complete and not corrupted
4. **Multiple Files**: Process files one at a time for best results
5. **Backup**: Always keep your original XML files as backup

## 🤝 Contributing

Want to improve the web interface? Here are some areas that could use enhancement:

- Additional platform support
- Batch file processing
- Advanced content filtering options
- Export format customization
- User account management
- Conversion history

## 📄 License

This project is open source and available under the same license as the main converter.

## 🆘 Support

If you encounter issues:

1. Check the troubleshooting section above
2. Verify your file format and size
3. Try different platform settings
4. Check browser compatibility
5. Report bugs with file samples (if possible)

---

**Happy Converting! 🎉**

Transform your blog exports into Framer-ready content with ease.
