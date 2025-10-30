# 🌾 MGNREGA Dashboard - Our Voice, Our Rights

A comprehensive, citizen-friendly dashboard for visualizing MGNREGA (Mahatma Gandhi National Rural Employment Guarantee Act) performance metrics at the district level across India.

**Live Demo**: [Deploy on Railway](https://railway.app) - See `RAILWAY_DEPLOY.md` for instructions

---

## 🎯 Project Overview

This dashboard makes MGNREGA data accessible to common citizens, especially those in rural areas with low technical literacy. With 12.15 Crore rural Indians benefiting from MGNREGA, this tool empowers citizens to:

- ✅ Understand their district's performance in simple terms
- ✅ View current and historical performance data
- ✅ Compare their district with others
- ✅ Access information in their native language
- ✅ Use audio features for low-literacy users

---

## ✨ Key Features

### 1. **Low-Literacy Friendly UX** 🎨
- **Large Icons**: 👥 (People), 💰 (Money), 🔨 (Work), 📅 (Days)
- **Audio Playback**: Text-to-Speech in Hindi for every metric
- **Bilingual**: English + Hindi labels throughout
- **Simple Visualizations**: Bar charts with large numbers
- **Color Coding**: Green (good), Red (attention needed)
- **Big Touch Targets**: Minimum 44x44px for mobile users

### 2. **District Selection** 📍
- Dropdown selection for all Indian states
- Dynamic district list based on selected state
- Automatic district detection via geolocation (bonus feature)

### 3. **Performance Metrics** 📊
- Total households employed
- Total wages paid (in Crores)
- Number of works completed
- Person-days generated
- Historical trends and comparisons

### 4. **Production-Ready** 🏗️
- Caching layer for performance
- Error handling and fallbacks
- Rate limiting
- Health check endpoints
- Structured logging

---

## 🛠️ Technology Stack

### Frontend
- **Framework**: Next.js 14 (React 18)
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **Features**: PWA, Responsive Design, Accessibility

### Backend
- **Framework**: FastAPI (Python 3.11)
- **Database**: SQLite (production-ready)
- **API**: RESTful with auto-generated docs
- **Features**: Async, Validation, Error Handling

### Deployment
- **Platform**: Railway (recommended) or Docker
- **CI/CD**: Auto-deploy on git push
- **Monitoring**: Built-in health checks

---

## 🚀 Quick Start

### Option 1: Deploy to Railway (Recommended - 15 minutes)

**Perfect for quick deployment and project submission!**

1. **Fork/Clone this repository**
   ```bash
   git clone https://github.com/Niladri-Peace/MGNREGA-Website.git
   cd MGNREGA-Website
   ```

2. **Follow the Railway deployment guide**
   - See: **`RAILWAY_DEPLOY.md`**
   - No credit card required
   - $5 free credit per month
   - Auto-deploys on git push

3. **Done!**
   - Your app will be live in ~15 minutes
   - Get your live URLs for submission

### Option 2: Run Locally with Docker

1. **Clone the repository**
   ```bash
   git clone https://github.com/Niladri-Peace/MGNREGA-Website.git
   cd MGNREGA-Website
   ```

2. **Set up environment**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

3. **Start with Docker Compose**
   ```bash
   docker-compose up -d --build
   ```

4. **Access the application**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Docs: http://localhost:8000/api/docs

### Option 3: Run Locally (Development)

**Backend:**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: .\venv\Scripts\activate
pip install -r requirements-sqlite.txt
python scripts/init_db.py
python scripts/seed_data.py
uvicorn app.main:app --reload
```

**Frontend:**
```bash
cd frontend
npm install
cp .env.local.example .env.local
# Edit .env.local with backend URL
npm run dev
```

---

## 📁 Project Structure

```
mgnrega-dashboard/
├── backend/                    # FastAPI Backend
│   ├── app/
│   │   ├── main.py            # Application entry point
│   │   ├── db/                # Database models
│   │   └── services/          # Business logic
│   ├── scripts/
│   │   ├── init_db.py         # Database initialization
│   │   └── seed_data.py       # Data seeding
│   ├── requirements-sqlite.txt
│   ├── nixpacks.toml          # Railway config
│   └── Procfile               # Railway start command
│
├── frontend/                   # Next.js Frontend
│   ├── src/
│   │   ├── app/               # Next.js App Router
│   │   ├── components/        # React components
│   │   ├── hooks/             # Custom hooks
│   │   └── utils/             # Utilities
│   ├── package.json
│   └── nixpacks.toml          # Railway config
│
├── docker-compose.yml         # Local development
├── railway.json               # Railway project config
├── RAILWAY_DEPLOY.md          # Deployment guide
└── README.md                  # This file
```

---

## 📊 Data Coverage

- **States**: West Bengal, Uttar Pradesh, Bihar, Madhya Pradesh, Rajasthan, and more
- **Districts**: 100+ districts across multiple states
- **Metrics**: Employment, wages, works, person-days
- **Time Period**: Historical data with monthly granularity

---

## 🎬 For Project Submission

### What You Need:

1. **Live URLs** (after Railway deployment)
   - Frontend URL
   - Backend API URL
   - API Documentation URL

2. **GitHub Repository**
   - https://github.com/Niladri-Peace/MGNREGA-Website

3. **Loom Video** (< 2 minutes)
   - Demo of live application
   - Show Railway dashboard
   - Brief code walkthrough
   - Architecture explanation

### Deployment Guide:
- See **`RAILWAY_DEPLOY.md`** for complete step-by-step instructions
- Includes troubleshooting and submission template

---

## 🔑 Key Highlights

- ✅ **Accessible Design**: Built for low-literacy rural users
- ✅ **Production-Ready**: Caching, error handling, monitoring
- ✅ **Scalable**: Stateless architecture, can handle millions
- ✅ **Resilient**: Works with cached data if API is down
- ✅ **Bonus Feature**: Geolocation-based district detection
- ✅ **Well-Documented**: Complete guides and code comments
- ✅ **Easy Deployment**: Railway auto-deploy in 15 minutes

---

## 📚 Documentation

- **`RAILWAY_DEPLOY.md`** - Complete Railway deployment guide
- **`README_FINAL.md`** - Detailed project walkthrough
- **`PROJECT_WALKTHROUGH.md`** - Architecture and design decisions
- **API Docs** - Auto-generated at `/api/docs` endpoint

---

## 🐛 Troubleshooting

### Common Issues:

**Frontend can't connect to backend:**
- Check `NEXT_PUBLIC_API_URL` in frontend environment variables
- Verify backend is running and accessible
- Check CORS settings in backend

**Database is empty:**
- Ensure `init_db.py` and `seed_data.py` ran successfully
- Check build logs in Railway deployment

**Deployment failed:**
- Review deployment logs
- Verify all configuration files are present
- Check `nixpacks.toml` settings

See `RAILWAY_DEPLOY.md` for detailed troubleshooting.

---

## 🤝 Contributing

This is a project for educational purposes. Feel free to:
- Fork the repository
- Make improvements
- Submit pull requests
- Report issues

---

## 📄 License

This project is open source and available under the MIT License.

---

## 🙏 Acknowledgments

- **Data Source**: data.gov.in (MGNREGA API)
- **Built with**: FastAPI, Next.js, Railway
- **Icons**: Emoji icons for accessibility
- **Inspiration**: Making government data accessible to all citizens

---

## 📞 Support

For deployment help or questions:
- Check `RAILWAY_DEPLOY.md` troubleshooting section
- Review Railway documentation: https://docs.railway.app/
- Check deployment logs in Railway dashboard

---

**Ready to deploy? Start with `RAILWAY_DEPLOY.md`** 🚀

---

Made with ❤️ for rural India
