# 🔐 GitHub Secrets Configuration

This guide shows you how to set up GitHub Secrets for automated deployments.

## Why GitHub Secrets?

GitHub Secrets allow you to:
- 🔒 Store sensitive credentials securely
- 🤖 Enable automated CI/CD deployments
- 🚀 Deploy automatically when you push to main branch
- 🔄 No manual deployment needed

## Required Secrets

You need to configure these secrets in your GitHub repository:

### 1. CLOUDFLARE_API_TOKEN
- **What**: Your Cloudflare API token for deploying to Pages
- **How to get**:
  1. Login to Cloudflare: https://dash.cloudflare.com
  2. Go to: My Profile → API Tokens
  3. Click "Create Token"
  4. Use template: "Edit Cloudflare Workers"
  5. Copy the token

### 2. CLOUDFLARE_ACCOUNT_ID
- **What**: Your Cloudflare account ID
- **How to get**:
  1. Login to Cloudflare Dashboard
  2. Select any domain/site
  3. Look on the right sidebar under "Account ID"
  4. Copy the ID

### 3. BACKEND_URL
- **What**: URL of your deployed backend (Railway)
- **Example**: `https://company-ai-assistant-production.up.railway.app`
- **How to get**:
  1. Deploy backend to Railway first
  2. Copy the URL from Railway dashboard
  3. Add it as a GitHub secret

## How to Add Secrets to GitHub

### Step 1: Go to Repository Settings
1. Open your GitHub repository
2. Click "Settings" tab
3. In the left sidebar, click "Secrets and variables"
4. Click "Actions"

### Step 2: Add Each Secret
For each secret:
1. Click "New repository secret"
2. Enter the name (e.g., `CLOUDFLARE_API_TOKEN`)
3. Paste the value
4. Click "Add secret"

Repeat for all three secrets.

## Automated Deployment Workflow

Once secrets are configured, the GitHub Action will:

1. **Trigger**: Automatically when you push to `main` branch
2. **Build**: Build the frontend with your backend URL
3. **Deploy**: Deploy to Cloudflare Pages
4. **Result**: Your site updates automatically!

## Testing the Workflow

### Method 1: Push to Main Branch
```bash
# Make a small change
echo "# Test" >> test.txt

# Commit and push
git add test.txt
git commit -m "Test deployment"
git push origin main
```

### Method 2: Manual Trigger
1. Go to "Actions" tab in GitHub
2. Select "Deploy to Cloudflare Pages"
3. Click "Run workflow"
4. Select branch: `main`
5. Click "Run workflow"

## Viewing Deployment Status

1. Go to "Actions" tab in your repository
2. Click on the latest workflow run
3. Watch the deployment progress
4. Check for any errors

## Troubleshooting

### "Secret not found" Error
- Make sure secret names match exactly (case-sensitive)
- Re-add the secrets if needed

### Deployment Fails
1. Check the workflow logs in Actions tab
2. Verify all secrets are correct
3. Ensure backend URL is accessible
4. Check Cloudflare API token has correct permissions

### Backend URL Not Working
- Verify Railway deployment is successful
- Check the URL is publicly accessible
- Update the BACKEND_URL secret if it changed

## Alternative: Manual Deployment

If you prefer not to use GitHub Actions:

1. Don't configure secrets
2. Use the `deploy.sh` script for manual deployment
3. Or follow QUICK_START.md for step-by-step manual process

## Security Best Practices

- ✅ Never commit secrets to code
- ✅ Use GitHub Secrets for all sensitive data
- ✅ Rotate API tokens periodically
- ✅ Use minimal permissions for API tokens
- ✅ Review who has access to repository secrets

## Summary

Required GitHub Secrets:
```
Name                    | Description
------------------------|------------------------------------------
CLOUDFLARE_API_TOKEN   | Cloudflare API token for deployments
CLOUDFLARE_ACCOUNT_ID  | Your Cloudflare account ID
BACKEND_URL            | Railway backend URL
```

Once configured:
- ✅ Automatic deployments on every push to main
- ✅ No manual deployment needed
- ✅ Secure credential management
- ✅ Continuous deployment ready

---

Need help? Check:
- [GitHub Secrets Documentation](https://docs.github.com/en/actions/security-guides/encrypted-secrets)
- [Cloudflare API Tokens](https://developers.cloudflare.com/fundamentals/api/get-started/create-token/)
- DEPLOYMENT_GUIDE.md for more details
