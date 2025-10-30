# 🚀 Railway Deployment Guide - MGNREGA Dashboard

Deploy your MGNREGA Dashboard to Railway in **15 minutes** - No credit card required!

---

## ✅ Prerequisites

- GitHub repository (already done ✓)
- Railway account (free - sign up with GitHub)
- Your code is Railway-ready (already configured ✓)

---

## 📝 Step-by-Step Deployment

### Step 1: Sign Up for Railway (2 minutes)

1. **Go to Railway**
   - Visit: https://railway.app
   - Click **"Login"**
   - Select **"Login with GitHub"**
   - Authorize Railway to access your GitHub

2. **Verify Account**
   - Railway gives you **$5 free credit** per month
   - No credit card needed
   - Enough for this project!

---

### Step 2: Deploy Backend (5 minutes)

1. **Create New Project**
   - Click **"New Project"**
   - Select **"Deploy from GitHub repo"**
   - Choose **"Niladri-Peace/MGNREGA-Website"**
   - Railway will create a service automatically

2. **Configure Backend Service**
   - Click on the service card
   - Go to **"Settings"** tab
   - Set **Root Directory**: `backend`
   - Railway will auto-detect the configuration from `nixpacks.toml`

3. **Add Environment Variables**
   - Go to **"Variables"** tab
   - Click **"New Variable"**
   - Add these:
     ```
     DATABASE_URL=sqlite:///./mgnrega.db
     ENVIRONMENT=production
     ALLOWED_ORIGINS=*
     ```
   - Click **"Add"** for each

4. **Generate Domain**
   - Go to **"Settings"** tab
   - Scroll to **"Networking"** section
   - Click **"Generate Domain"**
   - **COPY THE URL** (e.g., `https://mgnrega-backend-production-xxxx.up.railway.app`)
   - Save this URL - you'll need it for frontend!

5. **Deploy**
   - Railway automatically deploys on push
   - Go to **"Deployments"** tab
   - Wait 2-3 minutes for build to complete
   - Status should show **"Success"** ✅

6. **Test Backend**
   - Open in browser: `https://your-backend-url.up.railway.app/api/v1/health`
   - Should see: `{"status":"healthy","version":"1.0.0"}` ✅

---

### Step 3: Deploy Frontend (5 minutes)

1. **Add Frontend Service**
   - In your Railway project dashboard
   - Click **"New"** → **"GitHub Repo"**
   - Select **"Niladri-Peace/MGNREGA-Website"** again
   - Railway creates another service

2. **Configure Frontend Service**
   - Click on the new service card
   - Go to **"Settings"** tab
   - Set **Root Directory**: `frontend`
   - Railway will auto-detect Next.js from `nixpacks.toml`

3. **Add Environment Variables**
   - Go to **"Variables"** tab
   - Add:
     ```
     NEXT_PUBLIC_API_URL=https://your-backend-url.up.railway.app
     NODE_ENV=production
     ```
   - **IMPORTANT**: Replace `your-backend-url` with the actual backend URL from Step 2.4

4. **Generate Domain**
   - Go to **"Settings"** tab
   - Scroll to **"Networking"**
   - Click **"Generate Domain"**
   - **COPY THE URL** (e.g., `https://mgnrega-frontend-production-xxxx.up.railway.app`)

5. **Deploy**
   - Go to **"Deployments"** tab
   - Wait 3-5 minutes (frontend takes longer)
   - Status should show **"Success"** ✅

6. **Test Frontend**
   - Open: `https://your-frontend-url.up.railway.app`
   - You should see your dashboard! 🎉

---

### Step 4: Update Backend CORS (2 minutes)

Now that frontend is deployed, update backend to allow it:

1. **Go to Backend Service**
   - Click on backend service in Railway dashboard

2. **Update CORS Variable**
   - Go to **"Variables"** tab
   - Find `ALLOWED_ORIGINS`
   - Update to:
     ```
     ALLOWED_ORIGINS=https://your-frontend-url.up.railway.app,http://localhost:3000
     ```
   - Replace with your actual frontend URL

3. **Redeploy**
   - Service will automatically redeploy
   - Wait 1-2 minutes

---

## ✅ Deployment Complete!

### Your Live URLs:

- **Frontend**: `https://your-frontend-url.up.railway.app`
- **Backend**: `https://your-backend-url.up.railway.app`
- **API Docs**: `https://your-backend-url.up.railway.app/api/docs`
- **Health Check**: `https://your-backend-url.up.railway.app/api/v1/health`

---

## 🎬 Record Loom Video for Submission

### What to Show (< 2 minutes):

1. **Railway Dashboard** (15 seconds)
   - Show both services running (green status)
   - Show deployment logs

2. **Live Application** (45 seconds)
   - Open frontend URL
   - Select a state (e.g., West Bengal)
   - Select a district (e.g., North 24 Parganas)
   - Show metrics displaying
   - Demonstrate any special features

3. **Backend API** (15 seconds)
   - Show API docs page (`/api/docs`)
   - Show health endpoint response

4. **Code on GitHub** (30 seconds)
   - Show GitHub repository
   - Briefly show backend structure
   - Briefly show frontend structure

5. **Architecture Explanation** (15 seconds)
   ```
   "I deployed on Railway.app using their free tier.
   The app uses FastAPI backend with SQLite, Next.js frontend,
   covers multiple states and districts, includes caching and
   production-ready features. Architecture is cloud-agnostic
   and can be migrated to any platform if needed."
   ```

---

## 📝 Project Submission

### Submit These:

1. **Frontend URL**: `https://your-frontend-url.up.railway.app`
2. **Backend URL**: `https://your-backend-url.up.railway.app`
3. **GitHub Repository**: `https://github.com/Niladri-Peace/MGNREGA-Website`
4. **Loom Video Link**: Your < 2 minute walkthrough

### Submission Template:

```markdown
# MGNREGA Dashboard - Project Submission

## Live URLs
- **Frontend**: https://your-frontend-url.up.railway.app
- **Backend API**: https://your-backend-url.up.railway.app
- **API Documentation**: https://your-backend-url.up.railway.app/api/docs

## Repository
- **GitHub**: https://github.com/Niladri-Peace/MGNREGA-Website

## Video Walkthrough
- **Loom Video**: [Your Loom Video URL]

## Technology Stack
- **Frontend**: Next.js, React, TypeScript, Tailwind CSS
- **Backend**: FastAPI (Python)
- **Database**: SQLite (production-ready with migrations)
- **Deployment**: Railway (containerized deployment)
- **Features**: 
  - District-wise MGNREGA metrics
  - Historical data visualization
  - Accessible UI for low-literacy users
  - Production-ready architecture
```

---

## 🐛 Troubleshooting

### Frontend shows "Failed to fetch"

**Solution:**
1. Check backend is running (visit health endpoint)
2. Verify `NEXT_PUBLIC_API_URL` in frontend variables
3. Check `ALLOWED_ORIGINS` in backend variables
4. Redeploy both services

### Backend deployment failed

**Solution:**
1. Check deployment logs in Railway
2. Verify `requirements-sqlite.txt` exists
3. Check `nixpacks.toml` configuration
4. Try manual redeploy

### Database is empty

**Solution:**
1. Check build logs - `init_db.py` and `seed_data.py` should run
2. Verify `nixpacks.toml` has build commands
3. Manually trigger redeploy

### Can't access application

**Solution:**
1. Check service status in Railway (should be green)
2. Verify domain is generated
3. Check deployment logs for errors
4. Try accessing health endpoint first

---

## 💰 Railway Free Tier

- ✅ **$5 free credit** per month
- ✅ ~**500 hours** of usage
- ✅ Enough for assignment review and demo
- ⚠️ Monitor usage in Railway dashboard
- ⚠️ Can pause services to save credits when not in use

---

## 🎯 Final Checklist

Before submitting:

- [ ] Backend deployed and accessible
- [ ] Frontend deployed and accessible
- [ ] Can select state and see districts
- [ ] Can select district and see metrics
- [ ] API docs accessible
- [ ] Health endpoint returns success
- [ ] GitHub repository is public
- [ ] Loom video recorded (< 2 minutes)
- [ ] All URLs tested and working
- [ ] Submission document prepared

---

## 🔄 Update Deployment (After Code Changes)

If you make changes to your code:

```bash
# 1. Commit changes
git add .
git commit -m "Your update message"

# 2. Push to GitHub
git push origin main

# 3. Railway auto-deploys!
# No manual steps needed - Railway watches your GitHub repo
```

---

## 📊 Monitor Your Application

### In Railway Dashboard:

1. **Deployments Tab**
   - View deployment history
   - Check build logs
   - See deployment status

2. **Metrics Tab**
   - CPU usage
   - Memory usage
   - Network traffic

3. **Logs Tab**
   - Real-time application logs
   - Error messages
   - Request logs

---

## 🚀 You're Ready!

Your MGNREGA Dashboard is now live on Railway!

**Next Steps:**
1. Test all features thoroughly
2. Record your Loom video
3. Prepare submission document
4. Submit your project

**Need Help?**
- Railway Docs: https://docs.railway.app/
- Railway Discord: https://discord.gg/railway
- Check deployment logs in Railway dashboard

Good luck with your submission! 🎉
