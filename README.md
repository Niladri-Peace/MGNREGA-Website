# 🌾 MGNREGA Dashboard

A citizen-friendly web application for visualizing MGNREGA (Mahatma Gandhi National Rural Employment Guarantee Act) performance metrics at the district level across India.

**Live Demo**: https://carefree-integrity-production.up.railway.app

---

## 📖 About

This dashboard makes MGNREGA data accessible to citizens, especially those in rural areas with limited technical literacy. It empowers users to understand their district's performance in simple, visual terms.

### Key Features

- **Bilingual Interface**: Hindi and English support
- **Accessible Design**: Large icons, simple visualizations, audio features
- **District Selection**: Browse by state/district or auto-detect location
- **Performance Metrics**: Employment, wages, completed works, person-days
- **Historical Data**: View trends over time
- **Mobile-Friendly**: Responsive design with large touch targets

---

## 🛠️ Technology Stack

**Frontend**
- Next.js 14 (React 18)
- TypeScript
- Tailwind CSS
- PWA support

**Backend**
- FastAPI (Python)
- SQLite database
- RESTful API
- Auto-generated API documentation

**Deployment**
- Railway (Platform as a Service)
- Docker support
- Automated CI/CD

---

## 🚀 Quick Start

### Local Development

**Backend:**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: .\venv\Scripts\activate
pip install -r requirements-sqlite.txt
python scripts/init_db.py
python scripts/seed_data.py
uvicorn app.main:app --reload --port 8000
```

**Frontend:**
```bash
cd frontend
npm install
npm run dev
```

Access the application at `http://localhost:3000`

### Docker Deployment

```bash
docker-compose up -d --build
```

Services will be available at:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/api/docs

---

## 📁 Project Structure

```
mgnrega-dashboard/
├── backend/              # FastAPI backend
│   ├── app/             # Application code
│   ├── scripts/         # Database scripts
│   └── requirements-sqlite.txt
├── frontend/            # Next.js frontend
│   ├── src/
│   │   ├── app/        # Pages
│   │   ├── components/ # React components
│   │   ├── hooks/      # Custom hooks
│   │   └── lib/        # API client
│   └── package.json
└── docker-compose.yml   # Docker configuration
```

---

## 📊 Data Coverage

- **States**: 5 major states (West Bengal, Uttar Pradesh, Bihar, Maharashtra, Tamil Nadu)
- **Districts**: 30+ districts with comprehensive data
- **Metrics**: Employment statistics, wage data, works completed, person-days
- **Time Range**: 12 months of historical data per district

---

## 🌐 Deployment

The application is deployed on Railway with two services:

- **Backend API**: Handles data and business logic
- **Frontend**: User interface

For deployment instructions, see the Railway documentation or contact the repository maintainer.

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues for bugs and feature requests.

---

## 📄 License

This project is open source and available under the MIT License.

---

## 🙏 Acknowledgments

- MGNREGA data structure inspired by data.gov.in
- Built with modern web technologies
- Designed for accessibility and ease of use

---

Made with ❤️ for empowering citizens
