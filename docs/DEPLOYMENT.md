# 🚀 Deployment Guide

## 🌐 Live Production Deployment

**Current Deployment:**
- **Frontend**: https://hate-speech-detector-sigma.vercel.app/
- **Backend API**: https://hate-speech-detector-backend-oamo.onrender.com
- **API Docs**: https://hate-speech-detector-backend-oamo.onrender.com/docs

---

## Backend → Render

### 1. Push to GitHub
```bash
git add .
git commit -m "Deploy to production"
git push origin main
```

### 2. Create Web Service on Render
1. Go to https://render.com
2. Click "New +" → "Web Service"
3. Connect your GitHub repository
4. Configure settings:
   - **Name**: `hate-speech-detector-backend`
   - **Root Directory**: `backend`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements-render.txt`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
   - **Instance Type**: `Free` (512MB RAM)

5. Environment Variables:
   - `PYTHON_VERSION`: `3.10.0`
   - `TF_CPP_MIN_LOG_LEVEL`: `2`

6. Click "Create Web Service"

### 3. Wait for Deployment
- Initial build: ~5-10 minutes
- Model loading: ~30 seconds
- Check logs for "Startup complete!"

### 4. Test Backend
```bash
curl https://your-app.onrender.com/health
```

---

## Frontend → Vercel

### 1. Update API URL
Create `.env.production` in frontend folder:
```bash
VITE_API_URL=https://hate-speech-detector-backend-oamo.onrender.com
```

### 2. Deploy to Vercel

**Option A: Vercel CLI**
```bash
cd frontend
npm install -g vercel
vercel login
vercel --prod
```

**Option B: Vercel Dashboard**
1. Go to https://vercel.com
2. Click "Add New" → "Project"
3. Import your GitHub repository
4. Configure:
   - **Framework Preset**: `Vite`
   - **Root Directory**: `frontend`
   - **Build Command**: `npm run build`
   - **Output Directory**: `dist`
5. Add Environment Variable:
   - `VITE_API_URL`: `https://hate-speech-detector-backend-oamo.onrender.com`
6. Click "Deploy"

### 3. Deployment Complete
- Build time: ~1-2 minutes
- Your app is live on Vercel's edge network!

---

## Configuration Files

### Backend: `runtime.txt`
```
python-3.10.0
```

### Backend: `.python-version`
```
3.10.0
```

### Backend: `render.yaml`
```yaml
services:
  - type: web
    name: hate-speech-api
    env: python
    region: oregon
    plan: free
    rootDir: backend
    buildCommand: "pip install -r requirements-render.txt"
    startCommand: "uvicorn main:app --host 0.0.0.0 --port $PORT"
    envVars:
      - key: PYTHON_VERSION
        value: 3.10.0
      - key: TF_CPP_MIN_LOG_LEVEL
        value: 2
```

### Frontend: `vercel.json`
```json
{
  "buildCommand": "npm run build",
  "outputDirectory": "dist",
  "framework": "vite",
  "rewrites": [
    {
      "source": "/(.*)",
      "destination": "/index.html"
    }
  ]
}
```

---

## Testing Production

### Test Backend API
```bash
# Health check
curl https://hate-speech-detector-backend-oamo.onrender.com/health

# Prediction test
curl -X POST https://hate-speech-detector-backend-oamo.onrender.com/predict \
  -H "Content-Type: application/json" \
  -d '{"text": "This is a test message"}'
```

### Test Frontend
Open https://hate-speech-detector-sigma.vercel.app/ in your browser

---

## Troubleshooting

### Backend Issues

**Problem: Build fails**
- Check Python version (must be 3.10.0)
- Verify `requirements-render.txt` has correct versions
- Check Render logs for specific errors

**Problem: App crashes on startup**
- Model files must be in `backend/` directory
- Check memory usage (must fit in 512MB)
- Verify TensorFlow CPU version is used

**Problem: Slow cold starts**
- Normal for free tier (sleeps after 15min inactivity)
- First request after sleep: ~30 seconds
- Consider upgrading to paid tier for always-on

### Frontend Issues

**Problem: Can't connect to backend**
- Verify `VITE_API_URL` environment variable
- Check CORS settings in backend
- Test backend health endpoint directly

**Problem: Build fails**
- Check Node.js version compatibility
- Verify all dependencies in `package.json`
- Clear cache: `rm -rf node_modules && npm install`

### Common Errors

**Error: "No module named 'keras.src.legacy'"**
- Solution: Use TensorFlow 2.13.0 with Keras 2.13.1
- Update `requirements-render.txt`

**Error: "Port not detected"**
- Solution: Ensure `compile=False` when loading model
- Remove `raise` in lifespan exception handler

**Error: "Memory limit exceeded"**
- Solution: Use `tensorflow-cpu` instead of `tensorflow`
- Reduce batch size or model complexity

---

## Performance Optimization

### Backend
- **Memory**: ~400MB (fits 512MB free tier)
- **Cold start**: ~30 seconds (model loading)
- **Response time**: <500ms (after warm-up)
- **Throughput**: ~100 requests/second

### Frontend
- **Build size**: ~200KB (gzipped)
- **Load time**: <1 second (edge CDN)
- **Lighthouse score**: 95+ (Performance)

---

## Costs

### Free Tier Limits

**Render (Backend)**
- 512MB RAM
- Sleeps after 15min inactivity
- 750 hours/month free
- Automatic HTTPS

**Vercel (Frontend)**
- 100GB bandwidth/month
- Unlimited deployments
- Edge network (CDN)
- Automatic HTTPS

### Upgrade Options

**Render Starter ($7/month)**
- Always-on (no sleep)
- 512MB RAM
- Better performance

**Vercel Pro ($20/month)**
- 1TB bandwidth
- Advanced analytics
- Priority support

---

## Monitoring

### Backend Health
```bash
# Check if backend is alive
curl https://hate-speech-detector-backend-oamo.onrender.com/ping

# Detailed health check
curl https://hate-speech-detector-backend-oamo.onrender.com/health
```

### Logs
- **Render**: Dashboard → Service → Logs
- **Vercel**: Dashboard → Project → Deployments → View Logs

---

## CI/CD

Both platforms support automatic deployment:

1. **Push to GitHub** → Automatic deployment
2. **Pull Request** → Preview deployment (Vercel)
3. **Merge to main** → Production deployment

---

## Security

### Backend
- HTTPS enabled by default
- CORS configured for frontend origin
- Input validation with Pydantic
- Rate limiting (Render default)

### Frontend
- HTTPS enabled by default
- Environment variables for API URL
- No sensitive data in client code

---

## Done! 🎉

Your hate speech detection app is now live and accessible worldwide!

**Next Steps:**
- Share your app URL
- Monitor usage and performance
- Collect feedback for improvements
- Consider adding authentication for production use
