# Kicks & Co

Full-stack sneaker ecommerce starter built from the uploaded HTML design fileciteturn0file0.

## Stack
- Frontend: React + Vite
- Backend: FastAPI
- Database: PostgreSQL
- Auth: Cookie-based session login (no JWT)

## Features
- Landing page based on the uploaded HTML design
- Products listing with category filters
- Auctions with countdown timers
- Lucky draw wheel
- Newsletter subscription API
- User signup, login, logout, and current-user session API
- PostgreSQL schema for users, sessions, newsletter subscribers, products, and auctions

## Project structure
- `frontend/` React app
- `backend/` FastAPI app

## Run locally

### 1) PostgreSQL
Create a database named `kicks_co`.

```sql
CREATE DATABASE kicks_co;
```

### 2) Backend
```bash
cd backend
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/macOS
source venv/bin/activate
pip install -r requirements.txt
copy .env.example .env
# edit .env with your postgres credentials
uvicorn app.main:app --reload
```

Backend runs on `http://127.0.0.1:8000`

### 3) Frontend
```bash
cd frontend
npm install
npm run dev
```

Frontend runs on `http://127.0.0.1:5173`

## Default API routes
- `POST /api/auth/signup`
- `POST /api/auth/login`
- `POST /api/auth/logout`
- `GET /api/auth/me`
- `GET /api/products`
- `GET /api/auctions`
- `POST /api/newsletter/subscribe`

## Notes
- This project uses secure password hashing with `passlib[bcrypt]`.
- Authentication is handled using an HttpOnly cookie and a `user_sessions` table in PostgreSQL.
- CORS is configured for the Vite dev server by default.
