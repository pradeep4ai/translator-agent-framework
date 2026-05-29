# Deployment Guide: Translator Agent Framework

Complete step-by-step guide for deploying the Translator Agent Framework to GitHub and Vercel.

---

## 📋 Table of Contents

1. [Initial Setup](#initial-setup)
2. [GitHub Repository Setup](#github-repository-setup)
3. [GitHub Actions CI/CD Pipeline](#github-actions-cicd-pipeline)
4. [Vercel Frontend Deployment](#vercel-frontend-deployment)
5. [Environment Variables & Secrets](#environment-variables--secrets)
6. [Live URLs](#live-urls)
7. [Troubleshooting](#troubleshooting)

---

## Initial Setup

### Step 1: Initialize Git Repository Locally

```bash
cd C:/Users/deepa/workspace/PRADEEP-WORK/POC-DEMO/CLAUDE-AGENTS/GITHUB-PUBLISHED/translator-agent-framework
git init
git config user.email "your-email@example.com"
git config user.name "Your Name"
```

### Step 2: Create `.gitignore` File

The `.gitignore` file was created to exclude:
- Python: `__pycache__/`, `*.pyc`, `venv/`, `.env`
- Node.js: `node_modules/`, `.npm`
- IDE: `.vscode/`, `.idea/`, `*.swp`
- OS: `.DS_Store`, `Thumbs.db`

### Step 3: Create Initial Commit

```bash
git add .
git commit -m "Initial commit: Polyglot translator agent framework with FastAPI backend and React frontend"
```

**Result:** 58 files committed including:
- Python backend (FastAPI)
- React frontend (Vite + TypeScript)
- Agent framework
- Configuration and documentation

---

## GitHub Repository Setup

### Step 1: Create Repository on GitHub

1. Go to https://github.com/new
2. Enter **Repository name:** `translator-agent-framework`
3. Choose **Public** or **Private** visibility
4. **DO NOT** initialize with README, .gitignore, or license (we already have them)
5. Click **"Create repository"**

### Step 2: Add Remote and Push to GitHub

```bash
git remote add origin https://github.com/pradeep4ai/translator-agent-framework.git
git branch -M main
git push -u origin main
```

**Result:** Repository is now live at:
👉 https://github.com/pradeep4ai/translator-agent-framework

**Commits pushed:** 58 files on main branch

---

## GitHub Actions CI/CD Pipeline

### Step 1: CI/CD Workflow Configuration

A GitHub Actions workflow was created at `.github/workflows/deploy.yml` with three jobs:

#### **Job 1: Test** ✅
- Runs on: `ubuntu-latest`
- Python versions: 3.10, 3.11, 3.12 (matrix)
- Steps:
  - Clone repository
  - Set up Python
  - Install dependencies from `requirements.txt`
  - Run tests: `pytest tests/ -v --tb=short`

#### **Job 2: Build** 📦
- Runs after: Test job passes
- Only on: Push to main branch
- Steps:
  - Set up Python 3.11
  - Install dependencies
  - Set up Node.js 18
  - Build backend (FastAPI validation)
  - Install frontend dependencies: `cd frontend && npm ci`
  - Build frontend: `cd frontend && npm run build`
  - Run linting: `npm run lint`

#### **Job 3: Deploy to Vercel** 🚀
- Runs after: Build job passes
- Steps:
  - Install Vercel CLI
  - Deploy frontend using credentials
  - Post deployment status

### Step 2: View Workflow Status

Go to: https://github.com/pradeep4ai/translator-agent-framework/actions

**Status indicators:**
- 🟢 Green = Passed
- 🔴 Red = Failed
- 🟡 Yellow = Running

---

## Vercel Frontend Deployment

### Step 1: Create Vercel Account

1. Go to https://vercel.com/signup
2. Sign up with GitHub account (`pradeep4ai`)
3. Authorize Vercel to access your GitHub repositories

### Step 2: Import Repository

1. Go to https://vercel.com/dashboard
2. Click **"+ Add New"** → **"Project"**
3. Click **"Import Git Repository"**
4. Search for `translator-agent-framework` and select it
5. Click **"Import"**

### Step 3: Configure Project Settings

- **Framework Preset:** Vite
- **Root Directory:** `frontend` (⚠️ Important!)
- **Build Command:** `npm install && npm run build`
- **Output Directory:** `dist`
- Click **"Deploy"**

**Result:** Project is deployed to Vercel

### Step 4: Get Project IDs

From your project URL: `https://vercel.com/deep-s-projects15/translator-agent-framework`

- **Org ID:** `deep-s-projects15`
- **Project ID:** `translator-agent-framework`

---

## Environment Variables & Secrets

### Step 1: Generate Vercel Token

1. Go to https://vercel.com/account/tokens
2. Click **"Create Token"**
3. Name: `github-actions`
4. Copy the token (save securely)

### Step 2: Add GitHub Secrets

1. Go to: https://github.com/pradeep4ai/translator-agent-framework/settings/secrets/actions
2. Click **"New repository secret"** and add all three:

| Name | Value |
|------|-------|
| `VERCEL_TOKEN` | Your Vercel token from step 1 |
| `VERCEL_ORG_ID` | `deep-s-projects15` |
| `VERCEL_PROJECT_ID` | `translator-agent-framework` |

### Step 3: Verify Configuration Files

**vercel.json:**
```json
{
  "buildCommand": "cd frontend && npm install && npm run build",
  "installCommand": "cd frontend && npm install",
  "outputDirectory": "frontend/dist",
  "framework": "vite",
  "regions": ["iad1"]
}
```

This ensures npm packages are installed before building.

---

## Live URLs

### ✅ Frontend (Vercel)
👉 **https://translator-agent-framework.vercel.app**

- React + Vite frontend
- Hosted on Vercel
- Auto-deploys on every push to main
- Live status: ✅ Ready

### GitHub Repository
👉 **https://github.com/pradeep4ai/translator-agent-framework**

- Source code
- CI/CD pipelines
- Deployment configurations

### GitHub Actions Dashboard
👉 **https://github.com/pradeep4ai/translator-agent-framework/actions**

- View all workflow runs
- Check test results
- Monitor deployments

---

## Troubleshooting

### Issue: Build Command Failed (Exit Code 127)

**Error:** `Command "cd frontend && npm run build" exited with 127`

**Solution:** npm modules weren't installed before build

**Fix Applied:**
```json
"buildCommand": "cd frontend && npm install && npm run build",
"installCommand": "cd frontend && npm install"
```

### Issue: Undefined Environment Variable

**Error:** `VITE_API_URL doesn't exist`

**Solution:** Remove undefined env vars from vercel.json

**Fix Applied:** Removed `"env": { "VITE_API_URL": "@vite_api_url" }`

### Issue: Project Not Found in Vercel CLI

**Error:** `Project not found (VERCEL_PROJECT_ID)`

**Solution:** Ensure project is properly imported in Vercel dashboard first, then get correct IDs

---

## How to Make Changes

### To Update Code:

1. Make changes locally
2. Commit to git:
   ```bash
   git add .
   git commit -m "your commit message"
   ```
3. Push to GitHub:
   ```bash
   git push origin main
   ```

### What Happens Automatically:

1. ✅ GitHub Actions runs tests
2. ✅ GitHub Actions builds frontend
3. ✅ Vercel auto-deploys to live URL
4. ✅ Frontend updates at https://translator-agent-framework.vercel.app

---

## How to Stop/Pause Deployments

### Option 1: Disable GitHub Actions Workflow
1. Go to https://github.com/pradeep4ai/translator-agent-framework/actions
2. Click on `Deploy to Production` workflow
3. Click **"..."** → **"Disable workflow"**

### Option 2: Disable Vercel Auto-Deploy
1. Go to Vercel project settings
2. Go to **Git** section
3. Toggle **"Deploy on Push"** to OFF

### Option 3: Remove GitHub Secrets
Delete the three secrets from GitHub repository settings (workflow will fail without them)

### To Re-enable:
Simply re-enable the workflow or re-add the secrets

---

## Backend Setup (Local Development)

### Overview

The backend is a **FastAPI** application that handles translation requests using multiple AI models and language detection. It runs **locally** and can be accessed by the frontend.

### Architecture

```
Backend (Local)
├── backend/main.py (FastAPI server)
├── agents/ (Translation agents)
│   ├── translator.py
│   ├── detector.py
│   ├── router.py
│   ├── reviewer.py
│   └── pipeline.py
├── framework/ (Agent framework)
│   ├── agent.py
│   ├── orchestrator.py
│   ├── llm.py
│   └── tools.py
└── config/ (Configuration)
    └── routing.yaml
```

### Step 1: Install Python Dependencies

```bash
cd C:/Users/deepa/workspace/PRADEEP-WORK/POC-DEMO/CLAUDE-AGENTS/GITHUB-PUBLISHED/translator-agent-framework

# Create virtual environment (optional but recommended)
python -m venv venv
source venv/Scripts/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

**Dependencies include:**
- `fastapi` - Web framework
- `uvicorn` - ASGI server
- `pydantic` - Data validation
- `openai` - LLM integration
- `pytest` - Testing framework

### Step 2: Set Environment Variables

Create a `.env` file in the project root:

```bash
# .env
OPENAI_API_KEY=your_openai_api_key_here
```

**Note:** This file is in `.gitignore` and won't be committed to GitHub

### Step 3: Run Backend Locally

```bash
# Start FastAPI server with auto-reload
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

**Server details:**
- 🟢 Running at: `http://localhost:8000`
- 📚 API docs: `http://localhost:8000/docs` (Swagger UI)
- 🔧 Alternative docs: `http://localhost:8000/redoc` (ReDoc)

### Step 4: Test Backend

**Using curl:**
```bash
# Get available languages
curl http://localhost:8000/api/languages

# Translate text
curl -X POST http://localhost:8000/api/translate \
  -H "Content-Type: application/json" \
  -d '{
    "source_text": "Hello, world!",
    "source_lang": "en",
    "target_lang": "es"
  }'
```

**Using Python:**
```python
import requests

response = requests.post(
    "http://localhost:8000/api/translate",
    json={
        "source_text": "Hello",
        "source_lang": "en",
        "target_lang": "fr"
    }
)
print(response.json())
```

### Step 5: Frontend + Backend Integration

**Frontend will connect to backend at:**
```
http://localhost:8000
```

When both are running:
1. Backend: `http://localhost:8000` (terminal 1)
2. Frontend: `http://localhost:5173` (terminal 2)
3. Frontend automatically calls backend API

### Step 6: Run Tests

```bash
# Run all tests
pytest tests/ -v

# Run specific test file
pytest tests/test_translator.py -v

# Run with coverage
pytest tests/ --cov=agents --cov=framework
```

---

## Backend Deployment Options (Future)

### When Ready to Deploy:

**Option 1: Railway.app (Recommended)**
1. Go to https://railway.app
2. Create account and connect GitHub
3. Select `pradeep4ai/translator-agent-framework` repository
4. Railway auto-detects Python/FastAPI
5. Set environment variables (OPENAI_API_KEY)
6. Deploy with one click
7. Get live API URL

**Option 2: Render.com**
1. Go to https://render.com
2. Create new **Web Service**
3. Connect GitHub repository
4. **Build Command:** `pip install -r requirements.txt`
5. **Start Command:** `uvicorn backend.main:app --host 0.0.0.0 --port 8000`
6. Add environment variables in dashboard
7. Deploy

**Option 3: Heroku (Requires Credit Card)**
1. Go to https://www.heroku.com
2. Create app and connect GitHub
3. Set buildpacks: Python
4. Add environment variables
5. Deploy

---

## Running Backend + Frontend Together (Local Development)

### Terminal 1: Start Backend

```bash
# From project root
pip install -r requirements.txt
uvicorn backend.main:app --reload --port 8000
```

**Output:**
```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```

### Terminal 2: Start Frontend

```bash
# From project root
cd frontend
npm install
npm run dev
```

**Output:**
```
  VITE v5.3.4  ready in 234 ms

  ➜  Local:   http://localhost:5173/
  ➜  Press q to open URL in browser
```

### Access Application

- Frontend UI: http://localhost:5173
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

---

## Backend Routes

### Available API Endpoints

#### 1. Get Languages
```
GET /api/languages
```

**Response:**
```json
{
  "languages": [
    {
      "code": "en",
      "name": "English",
      "script": "Latin",
      "group": "western"
    },
    ...
  ]
}
```

#### 2. Translate Text
```
POST /api/translate
Content-Type: application/json

{
  "source_text": "Hello, world!",
  "source_lang": "en",
  "target_lang": "es",
  "detect_source_lang": false
}
```

**Response:**
```json
{
  "translation": "¡Hola, mundo!",
  "source_lang": "en",
  "target_lang": "es",
  "detected_lang": null,
  "detection_confidence": null,
  "provider_used": "openai",
  "model_used": "gpt-3.5-turbo",
  "quality_score": 0.95
}
```

---

## Troubleshooting Backend

### Issue: "ModuleNotFoundError: No module named 'fastapi'"

**Solution:**
```bash
pip install -r requirements.txt
```

### Issue: "Connection refused" (Backend not running)

**Solution:**
1. Make sure backend is running: `uvicorn backend.main:app --reload`
2. Check port 8000 is available
3. Verify firewall isn't blocking port 8000

### Issue: "OPENAI_API_KEY not found"

**Solution:**
1. Create `.env` file in project root
2. Add: `OPENAI_API_KEY=your_key_here`
3. Restart backend server

### Issue: CORS Errors (Frontend can't access backend)

**Solution:** Backend already has CORS enabled for localhost in `backend/main.py`

---

## Summary of What Was Done

✅ Initialized Git repository locally
✅ Created `.gitignore` file
✅ Made initial commit (58 files)
✅ Created GitHub repository at `pradeep4ai/translator-agent-framework`
✅ Pushed code to GitHub
✅ Set up GitHub Actions CI/CD pipeline (test, build, deploy)
✅ Created Vercel account and imported project
✅ Configured Vercel with correct settings
✅ Generated and added GitHub secrets
✅ Fixed build configuration issues
✅ Successfully deployed frontend to Vercel
✅ Frontend now live at: https://translator-agent-framework.vercel.app

---

## Quick Command Reference

```bash
# View status
git status
git log --oneline

# Commit and push
git add .
git commit -m "message"
git push origin main

# Check GitHub Actions
git remote -v
```

---

**Last Updated:** May 28, 2026  
**Deployment Status:** ✅ Frontend Live, Backend Ready for Deployment
