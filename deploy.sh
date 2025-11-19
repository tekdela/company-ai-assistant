#!/bin/bash

# 🚀 Automated Deployment Script for Company AI Assistant
# This script helps automate the deployment to Railway + Cloudflare

set -e  # Exit on error

echo "🚀 Company AI Assistant - Automated Deployment Script"
echo "========================================================"
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored messages
print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_info() {
    echo -e "ℹ️  $1"
}

# Check if running from correct directory
if [ ! -d "backend" ] || [ ! -d "frontend" ]; then
    print_error "This script must be run from the repository root directory"
    exit 1
fi

# Check prerequisites
print_info "Checking prerequisites..."

# Check Node.js
if ! command -v node &> /dev/null; then
    print_error "Node.js is not installed. Please install it from https://nodejs.org"
    exit 1
fi
print_success "Node.js is installed: $(node --version)"

# Check npm
if ! command -v npm &> /dev/null; then
    print_error "npm is not installed"
    exit 1
fi
print_success "npm is installed: $(npm --version)"

echo ""
echo "📋 Step 1: Backend Deployment to Railway"
echo "=========================================="
print_warning "Make sure you have:"
print_warning "  1. Merged PR #2 and PR #1 to main branch"
print_warning "  2. A Railway account (https://railway.app)"
print_warning "  3. Your Google Gemini API Key"
echo ""

read -p "Do you have Railway CLI installed? (y/n) " -n 1 -r
echo ""
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    print_info "Installing Railway CLI..."
    npm install -g @railway/cli
    print_success "Railway CLI installed"
fi

print_info "Please login to Railway in the browser that just opened..."
railway login

read -p "Enter your Google Gemini API Key: " GEMINI_API_KEY

if [ -z "$GEMINI_API_KEY" ]; then
    print_error "Gemini API Key is required"
    exit 1
fi

print_info "Navigating to backend directory..."
cd backend

print_info "Initializing Railway project..."
railway init

print_info "Setting environment variables..."
railway variables set GEMINI_API_KEY="$GEMINI_API_KEY"
railway variables set BACKEND_HOST=0.0.0.0
railway variables set BACKEND_PORT=8000
railway variables set ENVIRONMENT=production

print_info "Deploying backend to Railway..."
railway up

print_success "Backend deployed successfully!"

# Get Railway URL
print_info "Getting your Railway backend URL..."
BACKEND_URL=$(railway domain 2>/dev/null || echo "")

if [ -z "$BACKEND_URL" ]; then
    print_warning "Could not automatically get Railway URL"
    print_info "Please get it from Railway dashboard and enter it here:"
    read -p "Enter your Railway backend URL (e.g., https://app-name.up.railway.app): " BACKEND_URL
fi

print_success "Backend URL: $BACKEND_URL"

cd ..

echo ""
echo "📋 Step 2: Frontend Deployment to Cloudflare Pages"
echo "=================================================="
print_warning "Make sure you have a Cloudflare account (https://dash.cloudflare.com)"
echo ""

read -p "Do you have Wrangler CLI installed? (y/n) " -n 1 -r
echo ""
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    print_info "Installing Wrangler CLI..."
    npm install -g wrangler
    print_success "Wrangler CLI installed"
fi

print_info "Please login to Cloudflare in the browser that just opened..."
wrangler login

print_info "Navigating to frontend directory..."
cd frontend

print_info "Installing frontend dependencies..."
npm install

print_info "Building frontend with backend URL: $BACKEND_URL"
export VITE_API_URL="$BACKEND_URL"
npm run build

print_info "Deploying to Cloudflare Pages..."
wrangler pages publish dist --project-name=company-ai-assistant

print_success "Frontend deployed successfully!"

cd ..

echo ""
echo "📋 Step 3: Updating CORS Configuration"
echo "======================================="
print_info "Cloudflare should have given you a Pages URL"
read -p "Enter your Cloudflare Pages URL (e.g., https://company-ai-assistant-abc.pages.dev): " PAGES_URL

if [ -z "$PAGES_URL" ]; then
    print_warning "No Pages URL provided. You'll need to update CORS manually later."
else
    print_info "Updating CORS in Railway..."
    cd backend
    railway variables set CORS_ORIGINS="$PAGES_URL"
    print_success "CORS updated! Railway will redeploy automatically."
    cd ..
fi

echo ""
echo "🎉 Deployment Complete!"
echo "======================="
print_success "Your AI Assistant is now live!"
echo ""
echo "📍 Your URLs:"
echo "   Frontend: $PAGES_URL"
echo "   Backend:  $BACKEND_URL"
echo "   API Docs: $BACKEND_URL/docs"
echo ""
print_info "Next steps:"
echo "   1. Open $PAGES_URL in your browser"
echo "   2. Test the chat functionality"
echo "   3. Upload a CSV file"
echo "   4. Share the link with your team!"
echo ""
print_warning "If you encounter any issues:"
echo "   - Check Railway logs: railway logs"
echo "   - Check Cloudflare Pages deployment logs"
echo "   - Review the DEPLOYMENT_GUIDE.md"
echo ""
echo "Thank you for using Company AI Assistant! 🚀"
