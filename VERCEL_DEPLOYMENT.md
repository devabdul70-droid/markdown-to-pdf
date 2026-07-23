# Vercel Deployment Guide

## Overview

This guide explains how to deploy the Markdown to PDF Converter to Vercel.

⚠️ **Important**: FastAPI with PDF generation (WeasyPrint) has limitations on Vercel's serverless platform:
- Vercel functions have a **max execution time of 60 seconds** (pro) or 10 seconds (hobby)
- PDF generation can exceed this for large documents
- Recommended for **small to medium documents only**

## Prerequisites

1. **Vercel Account**: https://vercel.com
2. **GitHub Account**: Repository already connected
3. **Node.js + npm**: Installed locally (for Vercel CLI)

## Deployment Methods

### Method 1: Using Vercel CLI (Recommended)

#### Step 1: Install Vercel CLI
```bash
npm install -g vercel
# or
npm i -g vercel@latest
```

#### Step 2: Login to Vercel
```bash
vercel login
```
Follow the prompts to authenticate with your GitHub account.

#### Step 3: Deploy
```bash
cd "d:\abdul wahab\OTHER STUDY PROJECTS\markdown-to-pdf"
vercel
```

When prompted:
- **Which scope do you want to deploy to?** - Select your account
- **Found project settings** - Confirm or update settings
- **Production** or **Preview** - Choose deployment environment

#### Step 4: Set Environment Variables
```bash
vercel env add DEBUG
vercel env add MAX_FILE_SIZE
vercel env add ALLOWED_ORIGINS
vercel env add DEFAULT_PAGE_SIZE
```

Or via Vercel Dashboard:
1. Go to Project Settings → Environment Variables
2. Add required variables (see Configuration section below)

#### Step 5: Re-deploy with Environment Variables
```bash
vercel --prod
```

### Method 2: GitHub Integration (Automatic)

1. Push your code to GitHub:
```bash
git add .
git commit -m "Add Vercel configuration"
git push origin master
```

2. Go to https://vercel.com/new
3. Select "Continue with GitHub"
4. Select the **markdown-to-pdf** repository
5. Framework: **Python**
6. Python Version: **3.11**
7. Build Command: Leave default or use: `pip install -r requirements.txt`
8. Output Directory: Leave empty
9. Click "Deploy"

10. After deployment, add environment variables in Project Settings

### Method 3: Docker on Vercel (Limited)

Note: Vercel has limited Docker support. Use Methods 1-2 instead.

## Configuration

### Environment Variables

Set these in Vercel Dashboard (Project Settings → Environment Variables):

```
DEBUG=false
MAX_FILE_SIZE=5242880
MAX_MARKDOWN_LENGTH=500000
ALLOWED_ORIGINS=https://yourdomain.com
DEFAULT_PAGE_SIZE=A4
DEFAULT_MARGIN=2cm
DEFAULT_FONT_SIZE=12
```

For multiple origins:
```
ALLOWED_ORIGINS=https://yourdomain.com,https://www.yourdomain.com,http://localhost:3000
```

### Build Settings

**Framework Preset**: `Python`

**Python Version**: `3.11` or higher

**Build Command**:
```bash
pip install -r requirements.txt
```

**Install Command** (if needed):
```bash
pip install --upgrade pip setuptools wheel && pip install -r requirements.txt
```

**Output Directory**: Leave empty (or `.`)

## Troubleshooting

### Error: "uv lock" Command Failed

**Problem**: Vercel tries to use `uv` package manager but project isn't configured for it.

**Solution**: 
- ✅ We've added `pyproject.toml` to the repo
- ✅ The `vercel.json` specifies using `pip` instead of `uv`
- ✅ Commit and push the changes:

```bash
git add pyproject.toml vercel.json api/ .vercelignore
git commit -m "Add Vercel configuration"
git push origin master
```

Then redeploy:
```bash
vercel --prod
```

### Error: "WeasyPrint Dependencies Not Found"

**Problem**: System dependencies for WeasyPrint are missing.

**Solution**: Vercel's Python runtime doesn't include all system dependencies needed by WeasyPrint.

**Options**:
1. **Use Docker Deployment** - Deploy as a Docker container instead
2. **Use Traditional Hosting** - Deploy to AWS Lambda, Railway, Render, etc.
3. **Use Serverless Alternative** - Use a pre-built PDF API service

### Error: "Function Timeout (> 60 seconds)"

**Problem**: PDF generation takes too long.

**Solutions**:
1. **Accept limitations**: Vercel functions timeout at 60s (pro) or 10s (hobby)
2. **Optimize**: Split large documents, use simpler themes
3. **Alternative hosting**: Use Docker on Render, Railway, or AWS

### Error: "No module named 'weasyprint'"

**Problem**: Dependencies not installed during build.

**Solution**: Ensure `requirements.txt` is in root directory and is committed to git:
```bash
# Verify file exists and is tracked
git ls-files | grep requirements.txt

# If not tracked, add it
git add requirements.txt
git commit -m "Ensure requirements.txt is tracked"
git push
```

## Post-Deployment

### Verify Deployment

```bash
# Get deployment URL
vercel ls

# Or check Vercel Dashboard
# https://vercel.com/dashboard
```

### Test Endpoints

```bash
# Replace YOUR_DEPLOYMENT_URL with your actual URL
DOMAIN="your-deployment-url.vercel.app"

# Health check
curl https://$DOMAIN/health

# List themes
curl https://$DOMAIN/themes

# Convert text (simple test)
curl -X POST https://$DOMAIN/convert/text \
  -H "Content-Type: application/json" \
  -d '{
    "markdown": "# Test\n\nHello World",
    "theme": "default"
  }' \
  --output test.pdf
```

### View Logs

```bash
# Real-time logs
vercel logs --tail

# Or via Dashboard:
# Project → Deployments → Select deployment → Logs tab
```

### Monitor Performance

Vercel Dashboard provides:
- Request metrics
- Error rates
- Response times
- Bandwidth usage

## Limitations on Vercel

| Aspect | Limit | Notes |
|--------|-------|-------|
| **Execution Time** | 10s (hobby), 60s (pro) | PDF generation may timeout |
| **Memory** | 3GB max per request | Should be sufficient |
| **Disk Space** | 512MB per deployment | Themes/templates fit easily |
| **Concurrent Requests** | Scales automatically | May be throttled |
| **Request Payload** | 4.5MB max | File uploads limited |
| **Response Size** | 4.5MB max | Large PDFs may fail |

## Performance Tips

### For Vercel Serverless

1. **Use Simple Themes**: Complex CSS = slower rendering
2. **Limit Markdown Size**: Keep < 100KB for best performance
3. **Avoid Large Images**: Images in markdown slow rendering
4. **Use Default Settings**: Skip custom overrides when possible
5. **Monitor Execution Time**: Use Vercel Analytics

### Optimize PDF Generation

```bash
# In your client code, avoid:
# - Very large markdown documents (>200KB)
# - Complex CSS with many gradients
# - High-resolution embedded images
# - Custom fonts requiring downloads

# Best practices:
# - Use pre-defined themes
# - Keep markdown < 50KB
# - Use simple formatting
```

## Better Alternatives for This Project

Vercel may not be ideal for a PDF generation service. Consider:

### 1. **Railway.app** ⭐ Recommended
- Unlimited execution time
- Docker support native
- Simple deployment from GitHub
- Good free tier
- https://railway.app

### 2. **Render.com**
- Free tier with time limits
- Docker support
- Environment variables easy to set
- https://render.com

### 3. **Fly.io**
- Docker deployment
- Global distribution
- Good for long-running tasks
- https://fly.io

### 4. **AWS Lambda + Docker**
- Supports longer execution times
- Scalable
- Requires more setup
- https://aws.amazon.com/lambda

### 5. **DigitalOcean App Platform**
- Docker containers
- Generous free tier
- Simple GitHub integration
- https://www.digitalocean.com/products/app-platform

## Recommended Deployment Path

For best results:

1. **Development**: Local machine with `uvicorn`
2. **Testing**: Docker locally with `docker-compose`
3. **Production**: 
   - Small scale: **Railway.app** or **Render.com**
   - Large scale: **AWS ECS** or **Kubernetes**
   - Simple: **DigitalOcean App Platform**

## Support

For Vercel-specific issues:
- https://vercel.com/docs
- https://vercel.com/support

For application issues:
- Check `/logs` directory
- Review error responses
- Check Vercel analytics

---

## Quick Deployment Checklist

- [ ] Committed `pyproject.toml`, `vercel.json`, `api/index.py`, `.vercelignore`
- [ ] Pushed to GitHub
- [ ] Created Vercel project
- [ ] Set environment variables
- [ ] Deployed successfully
- [ ] Tested health endpoint
- [ ] Tested conversion endpoint
- [ ] Monitored initial performance
- [ ] Set up error alerts (optional)

Good luck with your deployment! 🚀
