# Netlify Deployment Guide for Framer Blog Converter

## Overview

This guide explains how to deploy your Framer Blog XML to CSV Converter using a **split architecture**:

- **Frontend**: React/Next.js app deployed on Netlify (static hosting)
- **Backend**: Python Flask API deployed on a separate platform

## Why This Approach?

**Traditional Flask apps** (what you had before):

- Need a Python server running
- Cannot be deployed on Netlify
- Require platforms like Render, Railway, Heroku

**Split Architecture** (what we're doing now):

- Frontend runs on Netlify (familiar to you)
- Backend runs separately on a Python platform
- Frontend communicates with backend via API calls
- Best of both worlds!

## Project Structure

```
framer_blog_converter/
├── frontend/                 # React/Next.js frontend
│   ├── pages/
│   ├── package.json
│   └── next.config.js
├── api_app.py               # Python Flask API
├── web_app.py               # Original full Flask app
└── src/                     # Core converter logic
```

## Step 1: Deploy the Python Backend

### Option A: Render (Recommended - Free)

1. **Go to [render.com](https://render.com)**
2. **Sign up and connect your GitHub repository**
3. **Create a new Web Service**
4. **Select your repository**
5. **Configure the service:**
   - **Name**: `framer-blog-api`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python api_app.py`
6. **Deploy!**

### Option B: Railway

1. **Go to [railway.app](https://railway.app)**
2. **Connect your GitHub repository**
3. **Deploy the `api_app.py`**

### Option C: Heroku

1. **Install Heroku CLI**
2. **Run:**
   ```bash
   heroku create framer-blog-api
   git push heroku main
   ```

## Step 2: Update Frontend API URLs

Once your backend is deployed, you'll get a URL like:

- Render: `https://framer-blog-api.onrender.com`
- Railway: `https://your-app.railway.app`
- Heroku: `https://framer-blog-api.herokuapp.com`

**Update the frontend to use this URL:**

1. **Edit `frontend/pages/index.tsx`**
2. **Replace the API calls with your backend URL:**

```typescript
// Change this:
const response = await fetch('/api/convert', {

// To this:
const response = await fetch('https://your-backend-url.com/api/convert', {
```

3. **Update the Netlify redirects in `netlify.toml`:**

```toml
[[redirects]]
  from = "/api/*"
  to = "https://your-backend-url.com/api/:splat"
  status = 200
  force = true
```

## Step 3: Deploy Frontend to Netlify

1. **Go to [netlify.com](https://netlify.com)**
2. **Sign up and connect your GitHub repository**
3. **Configure the build:**
   - **Build command**: `cd frontend && npm install && npm run build`
   - **Publish directory**: `frontend/out`
4. **Deploy!**

## Step 4: Test the Complete System

1. **Frontend**: Your Netlify URL (e.g., `https://your-app.netlify.app`)
2. **Backend**: Your Python API URL (e.g., `https://framer-blog-api.onrender.com`)
3. **Test file conversion** by uploading an XML file

## Environment Variables

### Backend (Python API)

Set these in your backend platform:

- `FLASK_ENV`: `production`
- `SECRET_KEY`: A secure random string
- `PORT`: Usually set automatically

### Frontend (Netlify)

Set these in Netlify:

- `NEXT_PUBLIC_API_URL`: Your backend API URL

## Troubleshooting

### Common Issues:

1. **CORS Errors**: Make sure `flask-cors` is installed and CORS is enabled
2. **API Not Found**: Check that your backend URL is correct
3. **File Upload Fails**: Ensure your backend has sufficient storage
4. **Build Fails**: Check that all dependencies are in `requirements.txt`

### Debug Steps:

1. **Test backend directly**: Visit `https://your-backend-url.com/api/health`
2. **Check browser console** for frontend errors
3. **Check backend logs** in your deployment platform
4. **Verify API endpoints** are working

## Benefits of This Approach

✅ **Familiar workflow**: Deploy frontend on Netlify like your React apps  
✅ **Scalability**: Frontend and backend can scale independently  
✅ **Cost-effective**: Use free tiers for both frontend and backend  
✅ **Flexibility**: Easy to switch backend platforms if needed  
✅ **Performance**: Static frontend loads fast, API handles heavy processing

## Alternative: Single Platform Deployment

If you prefer to keep everything together, you can still deploy the full Flask app on platforms like:

- **Render** (recommended)
- **Railway**
- **Heroku**
- **DigitalOcean App Platform**

But you won't be able to use Netlify for the frontend.

## Next Steps

1. **Deploy your Python backend** on Render/Railway/Heroku
2. **Update the frontend API URLs** with your backend URL
3. **Deploy the frontend** on Netlify
4. **Test the complete system**
5. **Share your working converter!**

This approach gives you the best of both worlds - the familiar Netlify deployment for your frontend and a robust Python backend for your conversion logic!
