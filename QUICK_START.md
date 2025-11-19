# ⚡ Quick Start - Deploy AI Assistant in 15 Minutes

This guide gets you from zero to a live AI Assistant web link in 15 minutes.

## 🎯 What You'll Get

A live, working AI Assistant at:
- **Frontend**: `https://company-ai-assistant-<you>.pages.dev`
- **Backend API**: `https://<your-app>.up.railway.app`

## 📋 Requirements (Get These First)

1. ✅ GitHub account (you have this)
2. ✅ Google Gemini API key → [Get it here](https://makersuite.google.com/app/apikey) (2 minutes)
3. ✅ Railway account → [Sign up](https://railway.app) (2 minutes, use GitHub login)
4. ✅ Cloudflare account → [Sign up](https://dash.cloudflare.com/sign-up) (2 minutes)
5. ✅ Node.js installed → Check with `node --version`

## 🚀 Step-by-Step (15 minutes total)

### Step 1: Merge PRs (2 minutes)

**Important: Do this first!**

1. Go to PR #2: https://github.com/tekdela/company-ai-assistant/pull/2
   - Click "Ready for review"
   - Click "Merge pull request"
   - Click "Confirm merge"

2. Go to PR #1: https://github.com/tekdela/company-ai-assistant/pull/1
   - Click "Ready for review"
   - Click "Merge pull request"
   - Click "Confirm merge"

Now all code is in the main branch!

### Step 2: Deploy Backend (5 minutes)

```bash
# 1. Clone the repo
git clone https://github.com/tekdela/company-ai-assistant.git
cd company-ai-assistant

# 2. Install Railway CLI
npm install -g @railway/cli

# 3. Login to Railway
railway login
# This opens a browser - click "Authorize"

# 4. Go to backend directory
cd backend

# 5. Create a new Railway project
railway init
# Select "Create new project"
# Give it a name like "company-ai-assistant"

# 6. Add environment variables
railway variables set GEMINI_API_KEY=your_actual_gemini_key_here
railway variables set BACKEND_HOST=0.0.0.0
railway variables set BACKEND_PORT=8000
railway variables set ENVIRONMENT=production

# 7. Deploy!
railway up
```

After deployment, Railway will show you a URL like:
`https://company-ai-assistant-production.up.railway.app`

**Copy this URL** - you'll need it!

### Step 3: Deploy Frontend (5 minutes)

```bash
# 1. Go to frontend directory
cd ../frontend

# 2. Install Wrangler CLI (if not installed)
npm install -g wrangler

# 3. Login to Cloudflare
wrangler login
# This opens a browser - click "Allow"

# 4. Update API URL in vite.config.ts
# Edit the file and replace the proxy target with your Railway URL
# Or just set an environment variable:
export VITE_API_URL=https://your-railway-url.up.railway.app

# 5. Install dependencies and build
npm install
npm run build

# 6. Deploy to Cloudflare Pages
wrangler pages publish dist --project-name=company-ai-assistant
```

You'll get a URL like:
`https://company-ai-assistant-abc.pages.dev`

### Step 4: Update CORS (1 minute)

Now that you have your Cloudflare Pages URL:

```bash
# Update CORS in Railway to allow your frontend
railway variables set CORS_ORIGINS=https://your-actual-pages-url.pages.dev
```

Railway will automatically redeploy.

### Step 5: Test It! (2 minutes)

1. Open your Cloudflare Pages URL in a browser
2. Try sending a message: "Xin chào!"
3. Upload a CSV file
4. Ask about the data

✅ If everything works, you're done!

---

## 🎉 You're Live!

Your AI Assistant is now:
- ✅ Accessible from anywhere via web link
- ✅ Running on production-grade infrastructure
- ✅ Backed by Google Gemini AI
- ✅ Distributed globally via Cloudflare CDN
- ✅ Completely free (using free tiers)

**Share your link**: `https://company-ai-assistant-<you>.pages.dev`

---

## 🔧 Optional: Custom Domain

Want a custom domain like `ai.yourcompany.com`?

### In Cloudflare:
1. Go to Pages → Your project → Custom domains
2. Click "Set up a custom domain"
3. Enter your domain (must be on Cloudflare DNS)
4. Follow the DNS setup instructions

---

## ❓ Troubleshooting

### "Connection failed" error
- Check Railway backend is running: Open `https://your-backend.up.railway.app/api/health`
- Verify CORS_ORIGINS matches your Pages URL exactly

### Backend not deploying
- Check Railway logs in the dashboard
- Verify GEMINI_API_KEY is set correctly

### Frontend build fails
```bash
cd frontend
rm -rf node_modules dist
npm install
npm run build
```

### Need to update backend code?
```bash
cd backend
# Make your changes
railway up
```

### Need to update frontend?
```bash
cd frontend
npm run build
wrangler pages publish dist
```

---

## 📊 What's Next?

Now that you're live:

1. **Monitor usage**: Check Railway dashboard for API usage
2. **Add features**: Customize the prompts, add more intents
3. **Scale up**: Upgrade Railway/Cloudflare plans as needed
4. **Secure it**: Add authentication if needed
5. **Share it**: Give the link to your team!

---

## 💰 Costs

Using free tiers:
- Railway: Free 500 hours/month (enough for 24/7)
- Cloudflare Pages: Unlimited free
- Gemini API: Free tier (60 requests/minute)

**Total: $0/month** for moderate usage!

When you need to scale:
- Railway Pro: $5/month
- Cloudflare Pages Pro: Free forever
- Gemini API: Pay as you go

---

## 🆘 Still Stuck?

1. Check the detailed DEPLOYMENT_GUIDE.md
2. Review Railway logs: `railway logs`
3. Check Cloudflare Pages deployment logs
4. Open an issue on GitHub with error details

---

**Happy deploying! 🚀**
