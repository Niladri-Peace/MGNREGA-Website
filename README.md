<div align="center">

# 🌾 MGNREGA Dashboard
### Our Voice, Our Rights | हमारी आवाज़, हमारे अधिकार

<p align="center">
  <strong>A citizen-friendly web application for visualizing MGNREGA performance metrics across India</strong>
</p>

<p align="center">
  <a href="https://mgnrega-website.up.railway.app/">
    <img src="https://img.shields.io/badge/🌐_Live_Demo-Visit_Now-success?style=for-the-badge&logo=railway&logoColor=white" alt="Live Demo">
  </a>
  <a href="https://github.com/Niladri-Peace/MGNREGA-Website">
    <img src="https://img.shields.io/badge/⭐_GitHub-Repository-blue?style=for-the-badge&logo=github" alt="GitHub">
  </a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Next.js-14-black?style=flat&logo=next.js" alt="Next.js">
  <img src="https://img.shields.io/badge/FastAPI-Python-009688?style=flat&logo=fastapi" alt="FastAPI">
  <img src="https://img.shields.io/badge/Railway-Deployed-blueviolet?style=flat&logo=railway" alt="Railway">
  <img src="https://img.shields.io/badge/License-MIT-green?style=flat" alt="License">
</p>

---

</div>

## 📖 About

This dashboard makes MGNREGA (Mahatma Gandhi National Rural Employment Guarantee Act) data accessible to citizens, especially those in rural areas with limited technical literacy. It empowers users to understand their district's performance in simple, visual terms.

### ✨ Key Features

<table>
<tr>
<td width="33%">

#### 🌍 Bilingual Support
Hindi and English interface for wider accessibility

</td>
<td width="33%">

#### 📱 Mobile-First Design
Large touch targets and responsive layout

</td>
<td width="33%">

#### 📍 Auto-Location
Geolocation-based district detection

</td>
</tr>
<tr>
<td width="33%">

#### 📊 Rich Metrics
Employment, wages, works, person-days

</td>
<td width="33%">

#### 📈 Historical Data
View trends over 12 months

</td>
<td width="33%">

#### 🎯 Accessible UI
Icons, colors, simple visualizations

</td>
</tr>
</table>

---

## 🛠️ Technology Stack

<div align="center">

| Frontend | Backend | Deployment |
|:--------:|:-------:|:----------:|
| ![Next.js](https://img.shields.io/badge/Next.js_14-black?style=for-the-badge&logo=next.js) | ![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white) | ![Railway](https://img.shields.io/badge/Railway-0B0D0E?style=for-the-badge&logo=railway&logoColor=white) |
| ![React](https://img.shields.io/badge/React_18-61DAFB?style=for-the-badge&logo=react&logoColor=black) | ![Python](https://img.shields.io/badge/Python_3.11-3776AB?style=for-the-badge&logo=python&logoColor=white) | ![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white) |
| ![TypeScript](https://img.shields.io/badge/TypeScript-3178C6?style=for-the-badge&logo=typescript&logoColor=white) | ![SQLite](https://img.shields.io/badge/SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white) | ![GitHub](https://img.shields.io/badge/GitHub_Actions-2088FF?style=for-the-badge&logo=github-actions&logoColor=white) |
| ![Tailwind](https://img.shields.io/badge/Tailwind_CSS-06B6D4?style=for-the-badge&logo=tailwind-css&logoColor=white) | ![Pydantic](https://img.shields.io/badge/Pydantic-E92063?style=for-the-badge&logo=pydantic&logoColor=white) | |

</div>

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

<div align="center">

| 🗺️ Coverage | 📈 Details |
|:------------|:-----------|
| **5** Major States | West Bengal, Uttar Pradesh, Bihar, Maharashtra, Tamil Nadu |
| **30+** Districts | Comprehensive district-level data |
| **12** Months | Historical trends and comparisons |
| **4** Key Metrics | Employment • Wages • Works • Person-Days |

</div>

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

<div align="center">

### 🌟 Live Application

**Visit the dashboard:** [https://mgnrega-website.up.railway.app/](https://mgnrega-website.up.railway.app/)

---

<p>
Made with ❤️ for empowering citizens
</p>

<p>
  <a href="https://mgnrega-website.up.railway.app/">
    <img src="https://img.shields.io/badge/🚀_View_Live_Demo-Visit_Now-success?style=for-the-badge" alt="Live Demo">
  </a>
</p>

</div>
