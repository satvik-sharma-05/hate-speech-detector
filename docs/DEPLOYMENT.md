# 🚀 Deployment Guide

## Backend → Render

1. **Push to GitHub**
   ```bash
   git add .
   git commit -m "Deploy"
   git push
   ```

2. **Create Web Service on Render**
   - Go to https://render.com
   - Click "New +" → "Web Service"
   - Connect your GitHub repo
   - Settings:
     - **Root Directory**: `backend`
     - **Build Command**: `pip install -r requirements-render.txt`
     - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
   - Click "Create Web Service"

3. **Copy Backend URL**
   - Example: `https://your-app.onrender.com`

## Frontend → Vercel

1. **Update API URL**
   ```javascript
   // frontend/src/App.jsx
   const API_URL = 'https://your-app.onrender.com'  // Your Render URL
   ```

2. **Deploy to Vercel**
   ```bash
   cd frontend
   npm install -g vercel
   vercel login
   vercel --prod
   ```
   
   Or use Vercel Dashboard:
   - Go to https://vercel.com
   - Click "Import Project"
   - Connect GitHub repo
   - **Root Directory**: `frontend`
   - Click "Deploy"

## Test Production

```bash
cd tests
python test_api.py https://your-app.onrender.com
```

## Environment Variables

### Backend (Render)
- `PYTHON_VERSION`: 3.12.0 (auto-detected)

### Frontend (Vercel)
- `VITE_API_URL`: Your Render backend URL

## Troubleshooting

**Backend not starting?**
- Check logs on Render dashboard
- Verify `requirements-render.txt` is correct
- Ensure model files are in `backend/` folder

**Frontend can't connect?**
- Verify API URL in `App.jsx`
- Check CORS settings in backend
- Test backend health: `https://your-app.onrender.com/health`

## Costs

- **Render**: Free tier (512MB RAM, sleeps after 15min inactivity)
- **Vercel**: Free tier (100GB bandwidth/month)

## Done! 🎉

Your app is live and ready to use!
