# 🚀 Oracle Cloud Deployment Guide - MGNREGA Dashboard

Complete step-by-step guide to deploy your MGNREGA Dashboard on Oracle Cloud Free Tier and submit your project.

---

## 📋 Table of Contents
1. [Prerequisites](#prerequisites)
2. [Oracle Cloud Setup](#oracle-cloud-setup)
3. [VM Instance Creation](#vm-instance-creation)
4. [Server Configuration](#server-configuration)
5. [Application Deployment](#application-deployment)
6. [Database Setup](#database-setup)
7. [Domain & SSL Setup (Optional)](#domain--ssl-setup)
8. [Testing & Verification](#testing--verification)
9. [Project Submission](#project-submission)
10. [Troubleshooting](#troubleshooting)

---

## Prerequisites

### What You Need:
- ✅ Oracle Cloud account (Free Tier - no credit card required)
- ✅ GitHub account
- ✅ Your project code ready
- ✅ SSH client (PuTTY for Windows or built-in terminal for Mac/Linux)
- ✅ Loom account for video recording

### Time Required:
- Oracle Cloud setup: 15 minutes
- VM deployment: 20 minutes
- Application setup: 30 minutes
- **Total: ~1 hour**

---

## 🌐 Oracle Cloud Setup

### Step 1: Create Oracle Cloud Account

1. **Go to Oracle Cloud**
   - Visit: https://www.oracle.com/cloud/free/
   - Click "Start for free"

2. **Sign Up**
   - Enter your email
   - Choose your country/region: **India**
   - Verify email
   - Complete registration (no credit card needed for free tier)

3. **Verify Account**
   - Check email for verification link
   - Complete phone verification
   - Set up password

4. **Login to Console**
   - Go to: https://cloud.oracle.com/
   - Sign in with your credentials
   - You'll land on the Oracle Cloud Console

### Step 2: Understand Free Tier Limits

Oracle Cloud Free Tier includes:
- ✅ 2 AMD-based Compute VMs (1/8 OCPU, 1 GB RAM each)
- ✅ OR 4 ARM-based Ampere A1 cores (24 GB RAM total)
- ✅ 200 GB Block Storage
- ✅ 10 TB outbound data transfer per month
- ✅ Always Free (no time limit)

**We'll use: 1 ARM-based VM (2 cores, 12 GB RAM) - Perfect for our app!**

---

## 🖥️ VM Instance Creation

### Step 3: Create Compute Instance

1. **Navigate to Compute**
   - In Oracle Cloud Console, click hamburger menu (☰)
   - Go to: **Compute** → **Instances**
   - Click **"Create Instance"**

2. **Configure Instance**

   **Name:**
   ```
   mgnrega-dashboard-vm
   ```

   **Placement:**
   - Leave default (Availability Domain)

   **Image and Shape:**
   - Click **"Change Image"**
   - Select: **Ubuntu 22.04** (Canonical Ubuntu 22.04 Minimal)
   - Click **"Select Image"**

   - Click **"Change Shape"**
   - Select: **Ampere** (ARM-based)
   - Choose: **VM.Standard.A1.Flex**
   - Set:
     - **OCPUs:** 2
     - **Memory (GB):** 12
   - Click **"Select Shape"**

3. **Networking**
   - **Virtual Cloud Network:** Create new VCN (or use existing)
   - **Subnet:** Create new public subnet (or use existing)
   - **Assign Public IP:** ✅ **YES** (Important!)

4. **Add SSH Keys**
   
   **Option A: Generate SSH Key Pair (Recommended)**
   - Click **"Generate a key pair for me"**
   - Click **"Save Private Key"** → Save as `oracle-vm-key.key`
   - Click **"Save Public Key"** → Save as `oracle-vm-key.pub`
   - Keep these files safe!

   **Option B: Use Existing SSH Key**
   - If you have SSH keys, paste your public key

5. **Boot Volume**
   - Leave default (50 GB is enough)

6. **Create Instance**
   - Click **"Create"**
   - Wait 2-3 minutes for provisioning
   - Status will change to **"Running"** (green)

7. **Note Your Public IP**
   - Once running, copy the **Public IP Address**
   - Example: `129.159.123.45`
   - Save this - you'll need it!

### Step 4: Configure Firewall Rules

1. **Open Ingress Rules**
   - On your instance page, click on the **VCN name** (under "Primary VNIC")
   - Click on **"Public Subnet"**
   - Click on **"Default Security List"**

2. **Add Ingress Rules**
   
   Click **"Add Ingress Rules"** and add these:

   **Rule 1: HTTP (Port 80)**
   ```
   Source CIDR: 0.0.0.0/0
   IP Protocol: TCP
   Destination Port Range: 80
   Description: HTTP traffic
   ```

   **Rule 2: HTTPS (Port 443)**
   ```
   Source CIDR: 0.0.0.0/0
   IP Protocol: TCP
   Destination Port Range: 443
   Description: HTTPS traffic
   ```

   **Rule 3: Backend API (Port 8000)**
   ```
   Source CIDR: 0.0.0.0/0
   IP Protocol: TCP
   Destination Port Range: 8000
   Description: FastAPI Backend
   ```

   **Rule 4: Frontend (Port 3000)**
   ```
   Source CIDR: 0.0.0.0/0
   IP Protocol: TCP
   Destination Port Range: 3000
   Description: Next.js Frontend
   ```

   Click **"Add Ingress Rules"** for each

---

## 🔧 Server Configuration

### Step 5: Connect to Your VM

**For Windows (using PowerShell):**

1. **Set SSH Key Permissions**
   ```powershell
   # Navigate to where you saved the key
   cd Downloads
   
   # If using PuTTY, convert key using PuTTYgen:
   # Load oracle-vm-key.key → Save private key as oracle-vm-key.ppk
   ```

2. **Connect via SSH**
   ```powershell
   ssh -i oracle-vm-key.key ubuntu@YOUR_PUBLIC_IP
   ```
   Replace `YOUR_PUBLIC_IP` with your actual IP (e.g., 129.159.123.45)

3. **Accept Fingerprint**
   - Type `yes` when prompted
   - You're now connected! 🎉

**For Mac/Linux:**

```bash
# Set correct permissions
chmod 400 ~/Downloads/oracle-vm-key.key

# Connect
ssh -i ~/Downloads/oracle-vm-key.key ubuntu@YOUR_PUBLIC_IP
```

### Step 6: Update System & Install Dependencies

Once connected to your VM:

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install essential tools
sudo apt install -y git curl wget nano htop

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Add user to docker group
sudo usermod -aG docker ubuntu

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Verify installations
docker --version
docker-compose --version

# Logout and login again for docker group to take effect
exit
```

**Reconnect to VM:**
```bash
ssh -i oracle-vm-key.key ubuntu@YOUR_PUBLIC_IP
```

### Step 7: Configure VM Firewall (iptables)

```bash
# Allow HTTP, HTTPS, and application ports
sudo iptables -I INPUT 6 -m state --state NEW -p tcp --dport 80 -j ACCEPT
sudo iptables -I INPUT 6 -m state --state NEW -p tcp --dport 443 -j ACCEPT
sudo iptables -I INPUT 6 -m state --state NEW -p tcp --dport 8000 -j ACCEPT
sudo iptables -I INPUT 6 -m state --state NEW -p tcp --dport 3000 -j ACCEPT

# Save rules
sudo netfilter-persistent save

# If netfilter-persistent not found:
sudo apt install iptables-persistent -y
sudo netfilter-persistent save
```

---

## 📦 Application Deployment

### Step 8: Push Code to GitHub

**On your local machine (Windows PowerShell):**

```powershell
# Navigate to your project
cd "C:\Users\Niladri\OneDrive\Desktop\District information\mgnrega-dashboard"

# Initialize git (if not done)
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit - MGNREGA Dashboard for Oracle Cloud"

# Create GitHub repository
# Go to: https://github.com/new
# Name: mgnrega-dashboard
# Make it Public
# Click "Create repository"

# Add remote (replace YOUR_USERNAME with your GitHub username)
git remote add origin https://github.com/YOUR_USERNAME/mgnrega-dashboard.git

# Push to GitHub
git branch -M main
git push -u origin main
```

### Step 9: Clone Repository on VM

**Back on your Oracle VM:**

```bash
# Clone your repository
cd ~
git clone https://github.com/YOUR_USERNAME/mgnrega-dashboard.git
cd mgnrega-dashboard

# Verify files
ls -la
```

### Step 10: Configure Environment Variables

```bash
# Copy example env file
cp .env.example .env

# Edit environment file
nano .env
```

**Update these values:**

```env
# Database Configuration
DATABASE_URL=postgresql://postgres:postgres@db:5432/mgnrega
POSTGRES_USER=postgres
POSTGRES_PASSWORD=your_secure_password_here
POSTGRES_DB=mgnrega

# Redis Configuration
REDIS_URL=redis://redis:6379/0
REDIS_PASSWORD=your_redis_password_here

# API Configuration
DATA_GOV_API_KEY=your_api_key_if_needed
ENVIRONMENT=production

# Backend URL (use your Oracle VM public IP)
NEXT_PUBLIC_API_URL=http://YOUR_PUBLIC_IP:8000

# CORS (allow your frontend)
ALLOWED_ORIGINS=http://YOUR_PUBLIC_IP:3000,http://localhost:3000
```

**Save and exit:** Press `Ctrl+X`, then `Y`, then `Enter`

---

## 🗄️ Database Setup

### Step 11: Start Database First

```bash
# Start only database and redis
docker-compose up -d db redis

# Wait for database to be ready (30 seconds)
sleep 30

# Check if database is running
docker-compose ps
```

### Step 12: Initialize Database

```bash
# Run database initialization
docker-compose exec db psql -U postgres -d mgnrega -c "CREATE EXTENSION IF NOT EXISTS postgis;"

# Seed initial data
docker-compose exec backend python scripts/seed_data.py

# Or if backend not running yet, start it temporarily:
docker-compose up -d backend
sleep 20
docker-compose exec backend python scripts/seed_data.py
```

---

## 🚀 Full Application Deployment

### Step 13: Start All Services

```bash
# Build and start all containers
docker-compose up -d --build

# This will start:
# - PostgreSQL database
# - Redis cache
# - FastAPI backend
# - Next.js frontend
# - Nginx reverse proxy
# - Worker (data ingestion)

# Wait for all services to start (2-3 minutes)
sleep 120

# Check status
docker-compose ps

# All services should show "Up" status
```

### Step 14: Verify Services

```bash
# Check backend logs
docker-compose logs backend

# Check frontend logs
docker-compose logs frontend

# Check if backend is responding
curl http://localhost:8000/api/v1/health

# Should return: {"status":"healthy","version":"1.0.0"}
```

---

## 🌍 Testing & Verification

### Step 15: Test Your Application

**Open in your browser:**

1. **Frontend:**
   ```
   http://YOUR_PUBLIC_IP:3000
   ```
   - Should show the dashboard
   - Try selecting a state and district

2. **Backend API:**
   ```
   http://YOUR_PUBLIC_IP:8000/api/v1/health
   ```
   - Should return JSON: `{"status":"healthy"}`

3. **API Documentation:**
   ```
   http://YOUR_PUBLIC_IP:8000/api/docs
   ```
   - Should show Swagger UI with all endpoints

### Step 16: Test Key Features

1. **State & District Selection**
   - Select a state (e.g., West Bengal)
   - Select a district (e.g., North 24 Parganas)
   - Verify metrics display

2. **Geolocation (if implemented)**
   - Click "Use My Location" button
   - Allow location access
   - Verify district auto-detection

3. **API Endpoints**
   - Test `/api/v1/states` - should return list of states
   - Test `/api/v1/districts/{state_id}` - should return districts
   - Test `/api/v1/metrics/{district_id}` - should return metrics

---

## 🔒 Domain & SSL Setup (Optional)

### Step 17: Add Custom Domain (Optional)

If you have a domain name:

1. **Point Domain to Oracle VM**
   - Go to your domain registrar (GoDaddy, Namecheap, etc.)
   - Add A record:
     ```
     Type: A
     Name: @ (or subdomain like 'mgnrega')
     Value: YOUR_PUBLIC_IP
     TTL: 3600
     ```

2. **Install SSL Certificate**
   ```bash
   # Install Certbot
   sudo apt install certbot python3-certbot-nginx -y

   # Get SSL certificate
   sudo certbot --nginx -d yourdomain.com

   # Follow prompts
   # Certificate will auto-renew
   ```

3. **Update Environment Variables**
   ```bash
   nano .env
   # Change NEXT_PUBLIC_API_URL to https://yourdomain.com
   ```

4. **Restart Services**
   ```bash
   docker-compose restart
   ```

---

## 🎬 Project Submission

### Step 18: Record Loom Video

**What to show (< 2 minutes):**

1. **Oracle Cloud Dashboard (15 seconds)**
   - Show your VM instance running
   - Show public IP address
   - Show instance details (2 cores, 12 GB RAM)

2. **Live Application Demo (45 seconds)**
   - Open frontend: `http://YOUR_PUBLIC_IP:3000`
   - Select a state (e.g., West Bengal)
   - Select a district (e.g., North 24 Parganas)
   - Show metrics displaying with icons
   - Demonstrate any special features (geolocation, audio, etc.)

3. **Backend API (15 seconds)**
   - Show API docs: `http://YOUR_PUBLIC_IP:8000/api/docs`
   - Show health endpoint response
   - Briefly show available endpoints

4. **Code & Architecture (30 seconds)**
   - Show GitHub repository
   - Briefly explain:
     - FastAPI backend
     - Next.js frontend
     - PostgreSQL + Redis
     - Docker deployment
   - Mention production-ready features (caching, error handling)

5. **Deployment Explanation (15 seconds)**
   ```
   "I deployed on Oracle Cloud Free Tier using Docker Compose.
   The application runs on an ARM-based VM with 2 cores and 12GB RAM.
   It includes FastAPI backend, Next.js frontend, PostgreSQL database,
   and Redis caching. The architecture is scalable and production-ready."
   ```

**Recording Tips:**
- Use Loom: https://www.loom.com/
- Keep it under 2 minutes
- Speak clearly
- Show, don't just tell
- Test your mic before recording

### Step 19: Prepare Submission

**Collect these items:**

1. **Live URLs:**
   - Frontend: `http://YOUR_PUBLIC_IP:3000`
   - Backend API: `http://YOUR_PUBLIC_IP:8000/api/docs`

2. **GitHub Repository:**
   - `https://github.com/YOUR_USERNAME/mgnrega-dashboard`

3. **Loom Video:**
   - Your recorded walkthrough video link

4. **Documentation:**
   - README.md (already in your repo)
   - This deployment guide

### Step 20: Submit Your Project

**Create a submission document:**

```markdown
# MGNREGA Dashboard - Project Submission

## Student Information
- Name: [Your Name]
- Email: [Your Email]
- Date: [Submission Date]

## Live Application
- **Frontend URL:** http://YOUR_PUBLIC_IP:3000
- **Backend API:** http://YOUR_PUBLIC_IP:8000/api/docs
- **GitHub Repository:** https://github.com/YOUR_USERNAME/mgnrega-dashboard

## Video Walkthrough
- **Loom Video:** [Your Loom Video Link]

## Technology Stack
- **Frontend:** Next.js, React, TypeScript, Tailwind CSS
- **Backend:** FastAPI (Python)
- **Database:** PostgreSQL with PostGIS
- **Caching:** Redis
- **Deployment:** Docker Compose on Oracle Cloud (ARM-based VM)
- **Features:** 
  - District-wise MGNREGA metrics
  - Geolocation-based district detection
  - Historical data visualization
  - Accessible UI for low-literacy users
  - Production-ready caching and error handling

## Deployment Details
- **Platform:** Oracle Cloud Free Tier
- **VM Specs:** 2 ARM cores, 12 GB RAM
- **Deployment Method:** Docker Compose
- **Services:** 6 containers (frontend, backend, database, redis, nginx, worker)

## Key Features Implemented
- ✅ State and district selection
- ✅ Real-time MGNREGA metrics
- ✅ Historical data visualization
- ✅ Geolocation-based district detection (bonus)
- ✅ Accessible design for rural users
- ✅ Production-ready architecture
- ✅ API documentation (Swagger UI)
- ✅ Caching layer (Redis)
- ✅ Database with proper schema
- ✅ Containerized deployment

## Notes
[Add any additional notes about your implementation]
```

**Submit to:**
- Your assignment portal
- Email to instructor
- Or as specified in your course requirements

---

## 🐛 Troubleshooting

### Common Issues & Solutions

#### Issue 1: Cannot connect to VM via SSH

**Solution:**
```bash
# Check if key has correct permissions
chmod 400 oracle-vm-key.key

# Try verbose mode to see error
ssh -v -i oracle-vm-key.key ubuntu@YOUR_PUBLIC_IP

# Make sure you're using 'ubuntu' as username (not 'root')
```

#### Issue 2: Ports not accessible from browser

**Solution:**
```bash
# Check Oracle Cloud security list (see Step 4)
# Check VM firewall
sudo iptables -L -n

# Re-apply firewall rules
sudo iptables -I INPUT 6 -m state --state NEW -p tcp --dport 80 -j ACCEPT
sudo iptables -I INPUT 6 -m state --state NEW -p tcp --dport 8000 -j ACCEPT
sudo iptables -I INPUT 6 -m state --state NEW -p tcp --dport 3000 -j ACCEPT
sudo netfilter-persistent save
```

#### Issue 3: Docker containers not starting

**Solution:**
```bash
# Check logs
docker-compose logs

# Check specific service
docker-compose logs backend

# Restart services
docker-compose down
docker-compose up -d --build

# Check disk space
df -h

# Check memory
free -h
```

#### Issue 4: Database connection failed

**Solution:**
```bash
# Check if database is running
docker-compose ps db

# Check database logs
docker-compose logs db

# Restart database
docker-compose restart db

# Test connection
docker-compose exec db psql -U postgres -d mgnrega -c "SELECT 1;"
```

#### Issue 5: Frontend shows "Failed to fetch"

**Solution:**
```bash
# Check backend is running
curl http://localhost:8000/api/v1/health

# Check NEXT_PUBLIC_API_URL in .env
nano .env
# Should be: NEXT_PUBLIC_API_URL=http://YOUR_PUBLIC_IP:8000

# Rebuild frontend
docker-compose up -d --build frontend

# Check CORS settings in backend
# Make sure ALLOWED_ORIGINS includes your frontend URL
```

#### Issue 6: Out of memory

**Solution:**
```bash
# Check memory usage
free -h
docker stats

# Stop unnecessary services
docker-compose stop worker  # If not needed immediately

# Restart services one by one
docker-compose restart
```

#### Issue 7: SSL certificate issues

**Solution:**
```bash
# Renew certificate
sudo certbot renew

# Check certificate status
sudo certbot certificates

# Test nginx config
sudo nginx -t
```

---

## 📊 Monitoring Your Application

### Check Application Health

```bash
# Check all containers
docker-compose ps

# Check logs
docker-compose logs -f

# Check resource usage
docker stats

# Check disk space
df -h

# Check memory
free -h

# Check network
netstat -tulpn | grep LISTEN
```

### Useful Commands

```bash
# Restart all services
docker-compose restart

# Stop all services
docker-compose down

# Start all services
docker-compose up -d

# View logs for specific service
docker-compose logs -f backend

# Execute command in container
docker-compose exec backend bash

# Check database
docker-compose exec db psql -U postgres -d mgnrega

# Backup database
docker-compose exec -T db pg_dump -U postgres mgnrega > backup_$(date +%Y%m%d).sql

# Restore database
cat backup_20240101.sql | docker-compose exec -T db psql -U postgres -d mgnrega
```

---

## 🎯 Final Checklist

Before submitting, verify:

- [ ] Oracle Cloud VM is running
- [ ] All Docker containers are up
- [ ] Frontend accessible at `http://YOUR_PUBLIC_IP:3000`
- [ ] Backend accessible at `http://YOUR_PUBLIC_IP:8000`
- [ ] API docs accessible at `http://YOUR_PUBLIC_IP:8000/api/docs`
- [ ] Can select state and see districts
- [ ] Can select district and see metrics
- [ ] Database has data (test a few districts)
- [ ] GitHub repository is public and complete
- [ ] Loom video recorded (< 2 minutes)
- [ ] All submission materials ready

---

## 🎉 Congratulations!

You've successfully deployed your MGNREGA Dashboard on Oracle Cloud!

**Your application is now:**
- ✅ Live and accessible from anywhere
- ✅ Running on production-grade infrastructure
- ✅ Using industry-standard technologies
- ✅ Scalable and maintainable
- ✅ Ready for submission

**Next Steps:**
1. Monitor your application regularly
2. Keep your VM updated: `sudo apt update && sudo apt upgrade`
3. Check logs for any errors
4. Consider adding monitoring (Prometheus/Grafana)
5. Add more features as needed

**Need Help?**
- Check troubleshooting section above
- Review Docker logs: `docker-compose logs`
- Check Oracle Cloud documentation
- Review your code on GitHub

Good luck with your submission! 🚀
