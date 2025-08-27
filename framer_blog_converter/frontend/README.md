# Framer Blog Converter Frontend

This is the React/Next.js frontend for the Framer Blog XML to CSV Converter. It provides a user-friendly interface for uploading XML files and converting them to CSV format.

## Features

- 🎨 Modern, responsive UI built with React and Next.js
- 📁 Drag-and-drop file upload
- 🔄 Real-time conversion progress
- 📊 File analysis and preview
- 📱 Mobile-friendly design
- 🌐 Platform selection (WordPress, Ghost, Jekyll)

## Quick Start

### Prerequisites

- Node.js 18+ installed
- npm or yarn package manager

### Installation

1. **Navigate to the frontend directory:**
   ```bash
   cd framer_blog_converter/frontend
   ```

2. **Run the setup script:**
   ```bash
   ./setup.sh
   ```

   This will:
   - Check Node.js version
   - Install dependencies
   - Build the project
   - Provide next steps

### Manual Setup

If you prefer to set up manually:

1. **Install dependencies:**
   ```bash
   npm install
   ```

2. **Build the project:**
   ```bash
   npm run build
   ```

3. **Start development server:**
   ```bash
   npm run dev
   ```

## Project Structure

```
frontend/
├── pages/           # Next.js pages
│   └── index.tsx   # Main converter page
├── package.json     # Dependencies and scripts
├── next.config.js   # Next.js configuration
├── setup.sh         # Setup script
└── README.md        # This file
```

## Development

### Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run start` - Start production server
- `npm run lint` - Run linting

### Development Server

The development server runs on `http://localhost:3000` by default.

## Deployment

### Netlify Deployment

This frontend is configured for Netlify deployment:

1. **Connect your GitHub repository to Netlify**
2. **Build settings:**
   - Build command: `cd framer_blog_converter/frontend && npm install && npm run build`
   - Publish directory: `framer_blog_converter/frontend/out`
3. **Deploy!**

### Configuration

The `netlify.toml` file contains the deployment configuration and redirects API calls to your Python backend.

## Backend Integration

This frontend communicates with a Python Flask API backend. You need to:

1. **Deploy the backend** (`api_app.py`) to a Python platform (Render, Railway, Heroku)
2. **Update API URLs** in the frontend code with your backend URL
3. **Configure CORS** on your backend to allow frontend requests

## Customization

### Styling

The UI uses Tailwind CSS classes. You can customize the appearance by modifying the CSS classes in the React components.

### Adding New Platforms

To add support for new platforms:

1. **Update the platforms array** in `pages/index.tsx`
2. **Ensure your backend supports** the new platform
3. **Test the integration**

### API Endpoints

The frontend expects these API endpoints from your backend:

- `POST /api/convert` - Convert XML to CSV
- `GET /api/platforms` - Get available platforms
- `POST /api/analyze` - Analyze XML file
- `GET /api/download/:id` - Download converted file

## Troubleshooting

### Common Issues

1. **Build fails**: Check Node.js version and dependencies
2. **API calls fail**: Verify backend URL and CORS configuration
3. **Styling issues**: Ensure Tailwind CSS is properly configured

### Debug Steps

1. **Check browser console** for JavaScript errors
2. **Verify API endpoints** are accessible
3. **Check build output** for compilation errors
4. **Test backend directly** to isolate issues

## Support

If you encounter issues:

1. **Check the main project README** for backend setup
2. **Review the deployment guide** in `NETLIFY_DEPLOYMENT.md`
3. **Check browser console** for error messages
4. **Verify backend is running** and accessible

## License

This frontend is part of the Framer Blog XML to CSV Converter project.
