# 🚀 GET YOUR LIVE WEB LINK NOW (5 Minutes)

## Fastest Way to Deploy - No Technical Skills Required

### Method 1: Use GitHub Pages + Free Backend (EASIEST)

This method requires ZERO coding knowledge. Just click buttons!

#### Step 1: Deploy Frontend (2 minutes)

1. **Go to Cloudflare Pages Dashboard**
   ```
   https://dash.cloudflare.com/sign-up/pages
   ```

2. **Create Account** (if you don't have one)
   - Use your GitHub account to sign up (fastest)
   - It's 100% FREE

3. **Create New Project**
   - Click "Create a project"
   - Click "Connect to Git"
   - Select "GitHub"
   - Choose repository: `tekdela/company-ai-assistant`
   - Click "Begin setup"

4. **Build Configuration** (Copy-paste these values)
   ```
   Production branch: copilot/merge-ai-assistant-to-main
   Framework preset: Vite
   Build command: cd frontend && npm install && npm run build
   Build output directory: frontend/dist
   Root directory: (leave empty)
   ```

5. **Deploy!**
   - Click "Save and Deploy"
   - Wait 2-3 minutes
   - **YOUR LIVE LINK IS READY!** 🎉

   Example URL: `https://company-ai-assistant-7x9.pages.dev`

#### Step 2: Deploy Backend (3 minutes)

**Option A: Railway (Recommended - Easier)**

1. **Go to Railway**
   ```
   https://railway.app/new
   ```

2. **Sign in with GitHub**
   - Click "Login with GitHub"
   - Authorize Railway

3. **Create New Project**
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose `tekdela/company-ai-assistant`
   - Select branch: `copilot/merge-ai-assistant-to-main`

4. **Configure**
   - Railway detects Python automatically
   - Click "Deploy Now"
   - Wait 2 minutes

5. **Get Your URL**
   - Click on your deployed service
   - Copy the URL (something like: `https://web-production-xxxx.up.railway.app`)

6. **Update Settings**
   - Click "Variables"
   - Add these (click "New Variable" for each):
   ```
   BACKEND_PORT = 8000
   CORS_ORIGINS = https://company-ai-assistant-7x9.pages.dev
   ```
   (Replace with YOUR Cloudflare Pages URL from Step 1)

**Option B: Render (Alternative - Also Free)**

1. **Go to Render**
   ```
   https://render.com/
   ```

2. **Sign Up with GitHub**

3. **Create Web Service**
   - Click "New +" → "Web Service"
   - Connect GitHub repository: `tekdela/company-ai-assistant`
   - Branch: `copilot/merge-ai-assistant-to-main`

4. **Configure**
   ```
   Name: company-ai-assistant-api
   Region: (Choose closest to you)
   Branch: copilot/merge-ai-assistant-to-main
   Root Directory: backend
   Runtime: Python 3
   Build Command: pip install -r requirements.txt
   Start Command: uvicorn app.main:app --host 0.0.0.0 --port $PORT
   ```

5. **Environment Variables**
   - Scroll down to "Environment Variables"
   - Add:
   ```
   CORS_ORIGINS = https://company-ai-assistant-7x9.pages.dev
   ```
   (Replace with YOUR Cloudflare Pages URL)

6. **Create Web Service**
   - Click the button at the bottom
   - Wait 3-4 minutes
   - Copy your URL: `https://company-ai-assistant-api.onrender.com`

#### Step 3: Connect Frontend to Backend (30 seconds)

1. **Go Back to Cloudflare Pages**
   - Open https://dash.cloudflare.com/
   - Click on your "company-ai-assistant" project

2. **Add Environment Variable**
   - Click "Settings" → "Environment variables"
   - Click "Production" tab
   - Click "Add variable"
   ```
   Variable name: VITE_API_URL
   Value: https://[your-railway-or-render-url]
   ```
   (Use the URL you got from Railway or Render)

3. **Redeploy**
   - Go to "Deployments" tab
   - Click "Retry deployment" button on latest deployment

#### Step 4: TEST YOUR LIVE LINK! 🎉

**Your AI Assistant is now LIVE!**

Open your Cloudflare Pages URL in a browser:
```
https://company-ai-assistant-[your-id].pages.dev
```

You should see:
- ✅ Beautiful chat interface
- ✅ Can type messages
- ✅ Get AI responses

---

### Method 2: One-Click Automated Deploy (For Technical Users)

If you have Git and Node.js installed:

```bash
# 1. Clone the repository
git clone https://github.com/tekdela/company-ai-assistant.git
cd company-ai-assistant

# 2. Checkout the correct branch
git checkout copilot/merge-ai-assistant-to-main

# 3. Run automated deploy script
chmod +x deploy.sh
./deploy.sh
```

The script will:
- ✅ Check all prerequisites
- ✅ Deploy backend to Railway
- ✅ Deploy frontend to Cloudflare
- ✅ Configure everything automatically
- ✅ Give you your live links

---

## Your Live URLs

After completion, you'll have:

**Main Application (Frontend):**
```
https://company-ai-assistant-[random-id].pages.dev
```

**Backend API:**
```
https://[project-name].up.railway.app
or
https://company-ai-assistant-api.onrender.com
```

**API Documentation:**
```
https://[your-backend-url]/docs
```

**Health Check:**
```
https://[your-backend-url]/api/health
```

---

## Share These Links

✅ **User-Facing Link (Share with team):**
```
https://company-ai-assistant-[your-id].pages.dev
```

✅ **API Documentation (For developers):**
```
https://[your-backend]/docs
```

✅ **Health Status (For monitoring):**
```
https://[your-backend]/api/health
```

---

## Troubleshooting

### Frontend shows "Cannot connect to server"

1. Check backend is running:
   - Visit: `https://[your-backend-url]/api/health`
   - Should show: `{"status": "healthy"}`

2. Check environment variable:
   - Cloudflare Pages → Settings → Environment variables
   - Make sure `VITE_API_URL` is set correctly

3. Redeploy frontend:
   - Cloudflare Pages → Deployments → Retry deployment

### Backend shows "Application error"

1. Check logs:
   - Railway: Dashboard → Logs
   - Render: Dashboard → Logs tab

2. Check environment variables are set

3. Redeploy

---

## Free Tier Limits

**Will my deployment stay free?**

✅ **Cloudflare Pages:** Unlimited requests, free forever  
✅ **Railway:** 500 hours/month free (~$5/month after)  
✅ **Render:** 750 hours/month free  

**For most use cases, you'll stay within free limits!**

---

## Optional: Add Gemini AI (For Advanced Features)

1. **Get Free API Key**
   - Visit: https://makersuite.google.com/app/apikey
   - Click "Create API key"
   - Copy the key

2. **Add to Backend**
   - Railway/Render Dashboard
   - Environment Variables
   - Add: `GEMINI_API_KEY = [your-key]`
   - Service will auto-redeploy

---

## Success Checklist

- [ ] Signed up for Cloudflare (free)
- [ ] Signed up for Railway or Render (free)
- [ ] Deployed frontend to Cloudflare Pages
- [ ] Deployed backend to Railway/Render
- [ ] Updated CORS and API URL variables
- [ ] Tested live link - IT WORKS! 🎉

---

## Estimated Time

**Total Time to Live Link:** 5-7 minutes

- Cloudflare Pages setup: 2 minutes
- Railway/Render setup: 3 minutes
- Configuration: 1-2 minutes

---

## Support

**Still having issues?**

1. Check the detailed guide: `PRODUCTION_DEPLOYMENT.md`
2. Review deployment logs in your platform dashboard
3. Open a GitHub issue with error details
4. Check our documentation files

---

**Priority: URGENT** ⚡

Get your live link deployed NOW and share it with your team!

Your assistant is ready to help with:
- ✅ Vietnamese conversation
- ✅ Time queries
- ✅ Knowledge base search
- ✅ File uploads
- ✅ Translation

**Start typing and see the magic happen! 🚀**
