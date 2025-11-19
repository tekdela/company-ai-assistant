# 🚀 Company AI Assistant - Ready for Production Deployment

Trợ lý AI nội bộ hỗ trợ công việc cho công ty - Powered by Google Gemini AI

## ⚡ Quick Links

- **[Quick Start Guide](./QUICK_START.md)** - Deploy in 15 minutes
- **[Detailed Deployment Guide](./DEPLOYMENT_GUIDE.md)** - Step-by-step instructions
- **[PR #1: Basic System](https://github.com/tekdela/company-ai-assistant/pull/1)** - Core functionality
- **[PR #2: Gemini + Cloudflare](https://github.com/tekdela/company-ai-assistant/pull/2)** - AI enhancement

## 📊 Current Status

- ✅ **Backend**: FastAPI + Google Gemini AI (PR #1 + PR #2)
- ✅ **Frontend**: React + TypeScript + Vite (PR #1 + PR #2)
- ✅ **Infrastructure**: Docker + Cloudflare Workers/Pages (PR #2)
- ✅ **CI/CD**: GitHub Actions configured
- ⏳ **Deployment**: Ready to deploy (see guides above)

## 🎯 What This AI Assistant Does

- 💬 **Natural Vietnamese Conversation** - Powered by Google Gemini Pro
- 📚 **Knowledge Base** - Upload CSV files for instant Q&A
- ⏰ **Time Queries** - Multi-timezone support
- 🔄 **Translation** - Vietnamese ↔ English
- 🤖 **Smart Intent Detection** - Understands what you need
- 📊 **Session History** - Maintains conversation context

## 🚀 Deployment Options

### Option 1: Railway + Cloudflare (Recommended, Free)

**Best for**: Quick deployment, zero configuration

- **Backend**: Railway (free 500 hours/month)
- **Frontend**: Cloudflare Pages (free unlimited)
- **Result**: `https://company-ai-assistant-<you>.pages.dev`
- **Time**: 15 minutes
- **Cost**: $0/month

[👉 Follow Quick Start Guide](./QUICK_START.md)

### Option 2: Docker Compose (VPS/Cloud Server)

**Best for**: Full control, own infrastructure

- **Requirements**: VPS with Docker installed
- **Result**: Your own domain
- **Time**: 30 minutes
- **Cost**: VPS cost ($5-10/month)

[👉 Follow Deployment Guide](./DEPLOYMENT_GUIDE.md#alternative-docker-deployment-vpscloud-server)

## 📋 Pre-Deployment Checklist

Before deploying, you **must**:

### 1. Merge Pull Requests to Main Branch

**This is critical!** The code is currently in separate PRs:

- [ ] Merge [PR #2](https://github.com/tekdela/company-ai-assistant/pull/2) first (Gemini + Cloudflare)
- [ ] Then merge [PR #1](https://github.com/tekdela/company-ai-assistant/pull/1) (Basic system)

**How to merge**:
1. Go to each PR link above
2. Click "Ready for review" (converts from draft)
3. Click "Merge pull request"
4. Click "Confirm merge"

### 2. Get Required Credentials

- [ ] **Google Gemini API Key** → [Get it here](https://makersuite.google.com/app/apikey)
- [ ] **Railway Account** → [Sign up](https://railway.app)
- [ ] **Cloudflare Account** → [Sign up](https://dash.cloudflare.com/sign-up)

## 🎯 Expected Result

After deployment, you'll have:

- ✅ **Live Web Link**: `https://company-ai-assistant-<your-username>.pages.dev`
- ✅ **Working AI Chat**: Powered by Google Gemini
- ✅ **Global CDN**: Fast access worldwide via Cloudflare
- ✅ **API Endpoint**: `https://<your-app>.up.railway.app`
- ✅ **Auto HTTPS**: Secure by default
- ✅ **Zero Downtime**: 99.9% uptime

## 🏗️ Architecture

```
┌──────────────────┐
│     Users        │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│  Cloudflare CDN  │  ← Global distribution
│   (Pages/Edge)   │  ← DDoS protection
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│  Frontend (React)│
│    TypeScript    │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│ Backend (FastAPI)│  ← Deployed on Railway
│  Gemini AI API   │  ← Google Gemini Pro
│  Knowledge Base  │  ← CSV processing
└──────────────────┘
```

## 📚 Documentation

- **[README.md](./README.md)** - This file, overview
- **[QUICK_START.md](./QUICK_START.md)** - 15-minute deployment guide
- **[DEPLOYMENT_GUIDE.md](./DEPLOYMENT_GUIDE.md)** - Detailed deployment instructions
- **PR #1 README** - Basic system documentation
- **PR #2 README** - Gemini AI integration docs

## 🔧 Tech Stack

### Backend
- **Framework**: FastAPI 0.104.1
- **AI**: Google Gemini Pro
- **Data**: Pandas (CSV processing)
- **Server**: Uvicorn (async ASGI)
- **Language**: Python 3.11+

### Frontend
- **Framework**: React 18
- **Language**: TypeScript 5.2
- **Build**: Vite 5.0
- **HTTP**: Axios
- **Styling**: Custom CSS

### Infrastructure
- **Containerization**: Docker + Docker Compose
- **CDN**: Cloudflare Pages
- **Edge**: Cloudflare Workers
- **CI/CD**: GitHub Actions
- **Hosting**: Railway (backend), Cloudflare (frontend)

## 💰 Costs

### Free Tier (Recommended for starting)
- Railway: 500 hours/month free
- Cloudflare Pages: Unlimited free
- Gemini API: 60 requests/minute free
- **Total**: $0/month

## 🆘 Support

Having trouble? Check these resources:

1. **[Quick Start Guide](./QUICK_START.md)** - Common issues
2. **[Deployment Guide](./DEPLOYMENT_GUIDE.md)** - Troubleshooting section
3. **GitHub Issues** - Open a new issue with details

**Deploy now and get your live web link in 15 minutes!** 🚀

---

Made with ❤️ using Google Gemini AI and Cloudflare
