# 🚀 Deployment Guide - Company AI Assistant

This guide will help you deploy the AI Assistant to production and create a live web link.

## ⚠️ Important Prerequisites

Before starting deployment, you need to:

### 1. Merge Pull Requests to Main Branch

**You must merge the following PRs manually (in this order):**

1. **First**: Merge PR #2 (Gemini AI + Cloudflare integration)
   - Go to: https://github.com/tekdela/company-ai-assistant/pull/2
   - Click "Ready for review" to convert from draft
   - Click "Merge pull request"
   
2. **Second**: Merge PR #1 (Basic AI assistant system)
   - Go to: https://github.com/tekdela/company-ai-assistant/pull/1
   - Click "Ready for review" to convert from draft
   - Click "Merge pull request"

> **Note**: These merges will add all the necessary code (backend, frontend, infrastructure) to the main branch.

### 2. Get Required API Keys and Credentials

You'll need:

- **Google Gemini API Key**
  - Get it from: https://makersuite.google.com/app/apikey
  - Free tier available
  
- **Cloudflare Account** (for frontend deployment)
  - Sign up at: https://dash.cloudflare.com/sign-up
  - Free tier available
  - Get API Token from: https://dash.cloudflare.com/profile/api-tokens
  
- **Railway/Render Account** (for backend deployment)
  - Railway: https://railway.app (recommended)
  - Render: https://render.com
  - Both have free tiers

---

## 🎯 Deployment Strategy

We'll use this approach:
- **Frontend**: Deploy to Cloudflare Pages (free CDN + hosting)
- **Backend**: Deploy to Railway (free tier, easy setup)
- **Result**: Live web link at `https://company-ai-assistant-<your-username>.pages.dev`

---

## Step 1: Deploy Backend to Railway

### 1.1 Create Railway Project

```bash
# 1. Install Railway CLI
npm install -g @railway/cli

# 2. Login to Railway
railway login

# 3. Navigate to backend directory (after merging PRs)
cd backend

# 4. Initialize Railway project
railway init
```

### 1.2 Set Environment Variables

In Railway dashboard:

1. Go to your project
2. Click on "Variables" tab
3. Add these variables:

```
GEMINI_API_KEY=your_gemini_api_key_here
BACKEND_HOST=0.0.0.0
BACKEND_PORT=8000
CORS_ORIGINS=https://company-ai-assistant-tekdela.pages.dev
ENVIRONMENT=production
```

### 1.3 Deploy

```bash
# Deploy to Railway
railway up
```

Your backend will be available at: `https://your-app-name.up.railway.app`

**Note the URL** - you'll need it for frontend configuration.

---

## Step 2: Deploy Frontend to Cloudflare Pages

### 2.1 Install Wrangler CLI

```bash
npm install -g wrangler
```

### 2.2 Login to Cloudflare

```bash
wrangler login
```

### 2.3 Build Frontend

First, update the API URL in the frontend code to point to your Railway backend:

```bash
cd frontend

# Edit vite.config.ts and update the proxy target:
# Change: target: 'http://localhost:8000'
# To: target: 'https://your-app-name.up.railway.app'

# Or set environment variable before build
export VITE_API_URL=https://your-app-name.up.railway.app

# Build the frontend
npm install
npm run build
```

### 2.4 Deploy to Cloudflare Pages

```bash
wrangler pages publish dist --project-name=company-ai-assistant
```

Your frontend will be available at: `https://company-ai-assistant-<random>.pages.dev`

You can customize the subdomain in Cloudflare dashboard.

---

## Step 3: Update CORS Configuration

After getting your Cloudflare Pages URL:

1. Go to Railway dashboard
2. Update the `CORS_ORIGINS` environment variable:
   ```
   CORS_ORIGINS=https://your-actual-pages-url.pages.dev
   ```
3. Redeploy the backend

---

## Step 4: Test Your Deployment

Visit your Cloudflare Pages URL:
```
https://company-ai-assistant-<your-subdomain>.pages.dev
```

You should see:
- ✅ Chat interface loads
- ✅ Can send messages
- ✅ File upload works
- ✅ All features working

---

## 🔧 Alternative: Docker Deployment (VPS/Cloud Server)

If you prefer to deploy on your own VPS:

### 1. SSH into your server

```bash
ssh user@your-server.com
```

### 2. Clone and deploy

```bash
# Clone repo (after merging PRs)
git clone https://github.com/tekdela/company-ai-assistant.git
cd company-ai-assistant

# Copy environment file
cp backend/.env.example backend/.env

# Edit with your keys
nano backend/.env

# Deploy with Docker Compose
docker-compose -f docker-compose.prod.yml up -d
```

### 3. Setup Nginx reverse proxy

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:3000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location /api {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

---

## 🎯 Expected Final URLs

After successful deployment:

- **Frontend**: `https://company-ai-assistant-tekdela.pages.dev`
- **Backend**: `https://company-ai-assistant-api.up.railway.app`
- **API Docs**: `https://company-ai-assistant-api.up.railway.app/docs`

---

## ✅ Verification Checklist

- [ ] PRs #1 and #2 merged to main branch
- [ ] Backend deployed to Railway
- [ ] Frontend built successfully
- [ ] Frontend deployed to Cloudflare Pages
- [ ] CORS configured correctly
- [ ] Chat interface loads without errors
- [ ] Can send and receive messages
- [ ] File upload works
- [ ] All features tested

---

## 🆘 Troubleshooting

### Frontend shows "Connection Error"
- Check CORS_ORIGINS in Railway matches your Pages URL
- Check backend is running: `curl https://your-backend.up.railway.app/api/health`

### Chat doesn't respond
- Verify GEMINI_API_KEY is set in Railway
- Check backend logs in Railway dashboard

### Build fails
- Ensure all dependencies are installed: `npm install`
- Clear cache: `rm -rf node_modules dist && npm install`

---

## 📞 Support

If you need help:
1. Check Railway/Cloudflare logs
2. Review the error messages
3. Open an issue on GitHub
4. Check the main README.md for more details

---

**Timeline**: Allow 30-60 minutes for complete deployment from start to finish.

**Cost**: Using free tiers, this deployment costs **$0/month**.
