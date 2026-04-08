# MentorIQ

A full-stack AI mentorship platform.

```
MentorIQ/
├── backend/          # FastAPI (Python) — REST API
│   ├── app/
│   │   ├── api/      # Route handlers
│   │   ├── core/     # Config, auth helpers
│   │   ├── db/       # Database models & sessions
│   │   ├── services/ # Business logic
│   │   └── main.py   # App entrypoint
│   ├── tests/
│   ├── requirements.txt
│   └── .env.example
├── frontend/         # React + Vite + Tailwind
│   ├── app/
│   ├── public/
│   ├── package.json
│   └── .env.example
├── Dockerfile        # Builds the backend image
├── docker-compose.yml
└── README.md
```

---

## Quick Start (Docker)

```bash
# 1. Copy env files and fill in your secrets
cp backend/.env.example backend/.env
cp frontend/.env.example frontend/.env

# 2. Start everything
docker-compose up --build
```

- Backend API → http://localhost:8000
- Frontend  → http://localhost:5173

---

## Local Dev (without Docker)

### Backend

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate        # Windows
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```
