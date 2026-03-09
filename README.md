# ResuM8 — AI-Powered Talent Matcher

> Bridge the gap between job seekers and recruiters using semantic AI matching powered by Google Gemini.

![ResuM8 Banner](https://placehold.co/1200x400/1e1b4b/818cf8?text=ResuM8+—+AI-Powered+Talent+Matcher)

## What is ResuM8?

ResuM8 is a full-stack web application that uses **Large Language Model embeddings** to intelligently match resumes to job listings. Unlike traditional keyword-based systems, ResuM8 _understands_ that "MERN Stack developer" matches "Full Stack Engineer" roles.

**Dual-sided platform:**
- **Candidates** upload their resume and get ranked job matches with skill gap analysis
- **Recruiters** upload multiple resumes and get candidates ranked by fit for their job description

---

## Tech Stack

| Layer | Technology |
|---|---|
| **Backend** | Python 3.11 + FastAPI (async) |
| **AI / Embeddings** | Google Gemini API (`text-embedding-004`) |
| **Database** | PostgreSQL + SQLAlchemy 2.0 (async) |
| **Similarity** | NumPy cosine similarity |
| **Resume Parsing** | PyPDF2 (PDF) + python-docx (DOCX) |
| **Security** | Cryptography (Fernet encryption), data masking |
| **Frontend** | React 18 + Vite + Tailwind CSS |
| **Routing** | React Router DOM v6 |
| **HTTP Client** | Axios |
| **Icons** | Lucide React |
| **Containers** | Docker + Docker Compose |

---

## Prerequisites

Before starting, make sure you have:

- **Python 3.11+** — [python.org/downloads](https://python.org/downloads)
- **Node.js 20+** — [nodejs.org](https://nodejs.org)
- **PostgreSQL 14+** — [postgresql.org/download](https://postgresql.org/download)
- **Git** — [git-scm.com/downloads](https://git-scm.com/downloads)
- **Google Gemini API Key** (free) — [aistudio.google.com/apikey](https://aistudio.google.com/apikey)

---

## Local Development Setup

### Step 1: Clone the Repository

```bash
git clone https://github.com/soumyadeepkhanra30-ui/resum8.git
cd resum8
```

### Step 2: Set Up the Backend

```bash
# Navigate to backend
cd backend

# Create a virtual environment
python -m venv venv

# Activate it
source venv/bin/activate        # Mac / Linux
# venv\Scripts\activate         # Windows

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Open .env and add your GEMINI_API_KEY
```

### Step 3: Set Up PostgreSQL

```bash
# Create the database (in psql or pgAdmin)
psql -U postgres
CREATE DATABASE resum8;
\q
```

Update your `backend/.env`:
```env
DATABASE_URL=postgresql+asyncpg://postgres:your_password@localhost:5432/resum8
```

### Step 4: Run the Backend

```bash
cd backend
uvicorn app.main:app --reload
```

✅ API is now running at: **http://localhost:8000**  
📚 Interactive docs: **http://localhost:8000/docs**

### Step 5: Seed the Database

The app comes with 50+ real-world job listings. Seed them with:

```bash
curl -X POST http://localhost:8000/api/jobs/seed
```

Or visit **http://localhost:8000/docs** → `POST /api/jobs/seed` → Execute

> ⚠️ This calls the Gemini API to generate embeddings for each job. It may take 60-90 seconds.

### Step 6: Set Up the Frontend

```bash
# In a new terminal, navigate to frontend
cd frontend

# Install dependencies
npm install

# Create env file
echo "VITE_API_URL=http://localhost:8000" > .env.local

# Start the dev server
npm run dev
```

✅ Frontend is now running at: **http://localhost:5173**

---

## Getting Your Google Gemini API Key (Free)

1. Go to **[aistudio.google.com/apikey](https://aistudio.google.com/apikey)**
2. Sign in with your Google account
3. Click **"Create API Key"**
4. Select or create a Google Cloud project
5. Copy the API key
6. Add it to `backend/.env`:
   ```env
   GEMINI_API_KEY=your_api_key_here
   ```

**Free tier limits:**
- 15 requests/minute
- 1,000 requests/day
- Perfect for development and demos

---

## Docker Setup (Alternative)

Run the entire stack with Docker Compose:

```bash
# 1. Copy and configure environment variables
cp .env.example .env
# Edit .env and add your GEMINI_API_KEY

# 2. Start all services (db + backend + frontend)
docker-compose up --build

# 3. Seed the database (in another terminal)
curl -X POST http://localhost:8000/api/jobs/seed
```

Services will be available at:
- **Frontend:** http://localhost:80
- **Backend API:** http://localhost:8000
- **API Docs:** http://localhost:8000/docs
- **Database:** localhost:5432

---

## API Documentation

### Candidate Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/api/candidate/upload-resume` | Parse PDF/DOCX resume, extract text |
| `POST` | `/api/candidate/match-jobs` | Match resume to top 5 jobs (semantic) |
| `POST` | `/api/candidate/gap-analysis` | AI gap analysis for a specific job |

### Recruiter Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/api/recruiter/upload-resumes` | Bulk upload + rank candidates by JD |
| `POST` | `/api/recruiter/summary/{id}` | AI executive summary for a candidate |

### Job Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/api/jobs` | List all jobs in database |
| `POST` | `/api/jobs/seed` | Seed database with 50+ dummy jobs |

### Health

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/health` | Health check |
| `GET` | `/` | Root with links |

---

## Environment Variables

### Backend (`backend/.env`)

| Variable | Required | Description |
|---|---|---|
| `GEMINI_API_KEY` | ✅ Yes | Google Gemini API key for embeddings + AI |
| `DATABASE_URL` | ✅ Yes | PostgreSQL connection string (asyncpg) |
| `FRONTEND_URL` | No | Frontend URL for CORS (default: localhost:5173) |
| `SECRET_KEY` | No | Encryption key for resume data masking |
| `DEBUG` | No | Enable debug logging (default: false) |
| `SAVE_RESUME_DATA` | No | Persist resumes in DB (default: false) |

### Frontend (`frontend/.env.local`)

| Variable | Required | Description |
|---|---|---|
| `VITE_API_URL` | No | Backend API URL (default: proxied to localhost:8000) |

---

## Deployment Guide

### Backend → Render (Free)

1. Go to [render.com](https://render.com) → Sign up with GitHub
2. Click **"New +"** → **"Web Service"**
3. Connect your `resum8` repository
4. Configure:
   - **Root Directory:** `backend`
   - **Runtime:** Python 3
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
5. Add **Environment Variables:**
   - `GEMINI_API_KEY` = your Gemini API key
   - `DATABASE_URL` = (from Render PostgreSQL, see below)
   - `SECRET_KEY` = any random string
6. Create PostgreSQL database:
   - Click **"New +"** → **"PostgreSQL"**
   - Copy the **Internal Database URL**
   - Add it as `DATABASE_URL` in your web service

Your API will be live at: `https://resum8-backend.onrender.com`

### Frontend → Vercel (Free)

1. Go to [vercel.com](https://vercel.com) → Sign up with GitHub
2. Click **"Add New Project"** → Import `resum8`
3. Configure:
   - **Root Directory:** `frontend`
   - **Framework Preset:** Vite (auto-detected)
4. Add **Environment Variable:**
   - `VITE_API_URL` = `https://resum8-backend.onrender.com`
5. Click **Deploy**

Your frontend will be live at: `https://resum8.vercel.app`

---

## Project Structure

```
resum8/
├── backend/
│   ├── app/
│   │   ├── main.py                 # FastAPI entry point, CORS, routes
│   │   ├── api/routes/
│   │   │   ├── candidate.py        # Candidate API routes
│   │   │   └── recruiter.py        # Recruiter API routes
│   │   ├── services/
│   │   │   ├── parser.py           # PDF/DOCX resume parsing
│   │   │   ├── embeddings.py       # Gemini embedding generation
│   │   │   ├── matcher.py          # Cosine similarity matching
│   │   │   ├── gap_analysis.py     # AI gap analysis
│   │   │   └── summarizer.py       # AI executive summaries
│   │   ├── models/
│   │   │   ├── candidate.py        # SQLAlchemy Candidate model
│   │   │   ├── job.py              # SQLAlchemy Job model
│   │   │   └── match.py            # SQLAlchemy Match model
│   │   ├── db/
│   │   │   ├── database.py         # PostgreSQL async connection
│   │   │   └── seed_jobs.py        # 50+ job listings + seeder
│   │   └── core/
│   │       ├── config.py           # pydantic-settings configuration
│   │       └── security.py         # Encryption, data masking
│   ├── requirements.txt
│   ├── Dockerfile
│   └── .env.example
├── frontend/
│   ├── src/
│   │   ├── App.jsx                 # React Router setup
│   │   ├── pages/
│   │   │   ├── HomePage.jsx        # Landing page
│   │   │   ├── CandidatePage.jsx   # Resume upload + job matching
│   │   │   └── RecruiterDashboard.jsx # Bulk upload + ranking
│   │   └── components/
│   │       ├── Navbar.jsx
│   │       ├── FileUploader.jsx    # Drag & drop uploader
│   │       ├── MatchScoreCard.jsx  # Circular progress score
│   │       ├── GapAnalysis.jsx     # Skills gap display
│   │       ├── JobCard.jsx         # Job match card
│   │       └── CandidateRankTable.jsx # Sortable results table
│   ├── package.json
│   ├── vite.config.js
│   ├── tailwind.config.js
│   └── Dockerfile
├── docker-compose.yml
├── .env.example
└── README.md
```

---

## How the Matching Works

```
Resume (PDF/DOCX)
    ↓
Parse text (PyPDF2 / python-docx)
    ↓
Generate embedding vector (Gemini text-embedding-004)
    ↓
Compare against 50+ pre-computed job embeddings
    ↓
Cosine similarity → Match Score (0-100%)
    ↓
Return top 5 matches + gap analysis
```

**Why this is better than keyword matching:**
- "MERN Stack" → semantically similar to "Full Stack Developer (React + Node)"
- "5 years Java Spring" → matches "Backend Java Engineer"
- "Built ML models in PyTorch" → matches "Machine Learning Engineer"

The embedding model captures _meaning_, not just word overlap.

---

## Screenshots

> 📸 Add screenshots here after running the app

| Page | Description |
|---|---|
| `[Homepage]` | Role selection landing page |
| `[Candidate]` | Resume upload + top 5 job matches |
| `[Gap Analysis]` | Missing skills and improvement tips |
| `[Recruiter]` | Ranked candidate table |
| `[AI Summary]` | Executive summary modal |

---

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/my-feature`
3. Make your changes
4. Submit a Pull Request

---

## License

MIT License — see [LICENSE](LICENSE) for details.

---

## Acknowledgments

- **Google Gemini AI** for the free embedding API
- **FastAPI** for the excellent async Python framework
- **Tailwind CSS** for making the UI beautiful
- **SQLAlchemy** for the powerful async ORM

---

*Built with ❤️ using 100% free-tier tools*
