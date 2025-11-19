# 🚀 Production Deployment Guide - Get Your Live Web Link

## URGENT: Deploy AI Assistant to Production

This guide will help you deploy your AI Assistant to get a **live web link** that works immediately.

**Target URLs:**
- **Main App (Frontend):** `https://company-ai-assistant-[your-name].pages.dev`
- **Backend API:** Will be deployed on Railway/Render (free tier)

---

## Quick Deploy (15 Minutes Total)

### Option 1: Cloudflare Pages + Railway (RECOMMENDED)

This is the fastest way to get your live link with minimal setup.

#### Step 1: Deploy Frontend to Cloudflare Pages (5 minutes)

1. **Login to Cloudflare**
   - Go to https://dash.cloudflare.com/
   - Sign up for free account if needed
   - Go to "Workers & Pages" section

2. **Connect GitHub Repository**
   - Click "Create Application" → "Pages" → "Connect to Git"
   - Select your GitHub account and repository `tekdela/company-ai-assistant`
   - Click "Begin setup"

3. **Configure Build Settings**
   ```
   Framework preset: Vite
   Build command: cd frontend && npm install && npm run build
   Build output directory: frontend/dist
   Root directory: (leave empty)
   ```

4. **Environment Variables** (Optional for frontend-only)
   ```
   VITE_API_URL = https://your-backend-url.railway.app
   ```
   *(Can set this later when backend is deployed)*

5. **Deploy**
   - Click "Save and Deploy"
   - Wait 2-3 minutes for build
   - **Your live link is ready!** `https://company-ai-assistant-xxx.pages.dev`

#### Step 2: Deploy Backend to Railway (10 minutes)

1. **Sign Up for Railway**
   - Go to https://railway.app/
   - Click "Login" → Sign in with GitHub
   - Free tier gives you 500 hours/month

2. **Create New Project**
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose `tekdela/company-ai-assistant`

3. **Configure Service**
   - Railway will auto-detect the Dockerfile
   - Click "Add variables" and set:
   ```
   GEMINI_API_KEY = (your Gemini API key - optional for now)
   BACKEND_PORT = 8000
   CORS_ORIGINS = https://company-ai-assistant-xxx.pages.dev
   ```

4. **Set Root Directory**
   - Go to Settings
   - Set "Root Directory" to `backend`
   - Set "Start Command" to `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

5. **Deploy**
   - Railway will automatically deploy
   - Get your live URL: `https://[random-name].up.railway.app`

6. **Update Frontend**
   - Go back to Cloudflare Pages
   - Settings → Environment variables
   - Add: `VITE_API_URL = https://[your-railway-url].up.railway.app`
   - Redeploy

---

### Option 2: Vercel (Alternative - Both Frontend & Backend)

#### Deploy Everything to Vercel

1. **Install Vercel CLI**
   ```bash
   npm install -g vercel
   ```

2. **Login**
   ```bash
   vercel login
   ```

3. **Deploy Frontend**
   ```bash
   cd frontend
   vercel --prod
   ```
   Follow prompts, select default settings

4. **Deploy Backend**
   ```bash
   cd ../backend
   vercel --prod
   ```
   
5. **Set Environment Variables**
   - Go to Vercel Dashboard
   - Select your backend project
   - Settings → Environment Variables
   - Add `GEMINI_API_KEY`, `CORS_ORIGINS`

---

### Option 3: Render (Free Alternative to Railway)

1. **Sign Up at Render**
   - Go to https://render.com/
   - Sign up with GitHub

2. **Create Web Service**
   - New → Web Service
   - Connect GitHub repo
   - Configure:
   ```
   Name: company-ai-assistant-api
   Root Directory: backend
   Environment: Python
   Build Command: pip install -r requirements.txt
   Start Command: uvicorn app.main:app --host 0.0.0.0 --port $PORT
   ```

3. **Environment Variables**
   ```
   GEMINI_API_KEY = (optional)
   CORS_ORIGINS = https://company-ai-assistant-xxx.pages.dev
   ```

4. **Deploy**
   - Click "Create Web Service"
   - Get URL: `https://company-ai-assistant-api.onrender.com`

---

## Post-Deployment Configuration

### Update Frontend to Use Backend

1. **Cloudflare Pages Dashboard**
   - Go to your deployed Pages project
   - Settings → Environment variables
   - Production tab
   - Add:
   ```
   VITE_API_URL = https://[your-backend-url]
   ```

2. **Redeploy**
   - Go to Deployments
   - Click "Retry deployment" or push a new commit

### Get Gemini API Key (Optional - For AI Features)

1. **Google AI Studio**
   - Go to https://makersuite.google.com/app/apikey
   - Click "Create API key"
   - Copy the key

2. **Add to Backend**
   - Railway/Render/Vercel Dashboard
   - Environment Variables
   - Add: `GEMINI_API_KEY = [your-key]`
   - Redeploy backend

---

## Testing Your Deployment

### 1. Test Frontend
Visit your Cloudflare Pages URL:
```
https://company-ai-assistant-xxx.pages.dev
```

You should see:
- ✅ Chat interface loads
- ✅ Can type messages
- ✅ UI is responsive

### 2. Test Backend
Visit your Railway/Render URL + `/api/health`:
```
https://your-backend.railway.app/api/health
```

Should return:
```json
{
  "status": "healthy",
  "timestamp": "...",
  "services": {...}
}
```

### 3. Test Full Integration
- Open frontend URL
- Type a message: "Xin chào"
- Should get AI response

---

## Troubleshooting

### Frontend shows "Can't connect to backend"
1. Check `VITE_API_URL` is set in Cloudflare Pages
2. Check backend is running (visit `/api/health`)
3. Check CORS settings in backend include frontend URL

### Backend won't start
1. Check `BACKEND_PORT` is set correctly
2. Railway: Should use `$PORT` variable
3. Check logs in deployment platform

### "Module not found" errors
1. Check `requirements.txt` has all dependencies
2. Ensure build command runs `pip install -r requirements.txt`

---

## Success Checklist

After following this guide, you should have:

- [ ] ✅ Frontend live at `https://company-ai-assistant-xxx.pages.dev`
- [ ] ✅ Backend live at `https://xxx.railway.app` or similar
- [ ] ✅ Frontend can connect to backend
- [ ] ✅ Chat interface working
- [ ] ✅ Can send and receive messages
- [ ] ✅ (Optional) Gemini AI responding

---

## URLs to Share

After deployment, your live links are:

**Main Application:**
```
https://company-ai-assistant-[your-id].pages.dev
```

**API Documentation:**
```
https://[your-backend].railway.app/docs
```

**API Health Check:**
```
https://[your-backend].railway.app/api/health
```

---

## Cost Summary

**FREE TIER LIMITS:**
- Cloudflare Pages: Unlimited (free forever)
- Railway: 500 hours/month free ($5/month after)
- Render: 750 hours/month free
- Google Gemini: 60 requests/minute free

**Estimated Total:** $0-5/month

---

## Next Steps

1. [ ] Set up custom domain (optional)
2. [ ] Configure Gemini API key for AI features
3. [ ] Upload CSV knowledge base through UI
4. [ ] Share live link with your team!

---

## Support

If you encounter issues:
1. Check deployment logs in platform dashboard
2. Review this guide
3. Check documentation in this repo
4. Open GitHub issue for help

---

**Estimated Time to Live Link:** 15-20 minutes

**Priority:** URGENT - Complete immediately for user access
