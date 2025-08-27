# Deployment Guide for Framer Blog XML to CSV Converter

## Overview
This Flask web application converts XML blog exports to CSV format for various platforms. It's designed to be deployed on cloud platforms that support Python web applications.

## Deployment Options

### Option 1: Render (Recommended - Free Tier)
Render is excellent for Flask apps and offers a generous free tier.

**Steps:**
1. Go to [render.com](https://render.com) and sign up
2. Connect your GitHub repository
3. Create a new Web Service
4. Select your repository
5. Render will automatically detect the `render.yaml` configuration
6. Deploy!

**Features:**
- Free tier available
- Automatic deployments from Git
- SSL certificates included
- Custom domains supported

### Option 2: Railway
Railway is another great option with a free tier.

**Steps:**
1. Go to [railway.app](https://railway.app) and sign up
2. Connect your GitHub repository
3. Create a new project
4. Deploy your Flask app

### Option 3: Heroku
Heroku has a free tier but requires a credit card.

**Steps:**
1. Install Heroku CLI
2. Run: `heroku create your-app-name`
3. Run: `git push heroku main`
4. Your app will be deployed

### Option 4: DigitalOcean App Platform
More professional but costs money.

## Environment Variables

Set these environment variables in your deployment platform:

- `FLASK_ENV`: Set to `production` for production deployments
- `SECRET_KEY`: A secure random string for Flask sessions
- `PORT`: The port your app should listen on (usually set automatically)

## File Structure for Deployment

```
framer_blog_converter/
├── web_app.py              # Main Flask application
├── requirements.txt         # Python dependencies
├── templates/              # HTML templates
├── src/                    # Core converter logic
└── tests/                  # Test files
```

## Important Notes

1. **Large Files**: The large XML files (4-5MB) have been removed from Git tracking to prevent deployment issues
2. **Temporary Files**: The app creates temporary files during conversion - ensure your deployment platform has sufficient storage
3. **File Uploads**: Maximum file size is set to 50MB
4. **Security**: Change the default secret key in production

## Troubleshooting

### Common Issues:

1. **Port Binding**: Ensure your app listens on `0.0.0.0` and uses the `PORT` environment variable
2. **Dependencies**: All required packages are in `requirements.txt`
3. **File Permissions**: Ensure the app can create temporary files
4. **Memory**: Large XML files require sufficient memory for processing

### Debug Mode:
- Set `FLASK_ENV=development` to enable debug mode
- Set `FLASK_ENV=production` to disable debug mode

## Local Development

To run locally:
```bash
cd framer_blog_converter
python web_app.py
```

The app will be available at `http://localhost:5000`

## Production Considerations

1. **Security**: Change the default secret key
2. **Logging**: Implement proper logging for production
3. **Monitoring**: Set up health checks and monitoring
4. **Backup**: Implement backup strategies for user data
5. **Rate Limiting**: Consider implementing rate limiting for file uploads
