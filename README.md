# Server-Side Web Programming — Lab Works

University lab works for the "Server-Side Web Programming" course: a users REST API built with FastAPI.
Each lab lives in its own branch and builds on the previous one.

| Lab | Branch | What's added |
|---|---|---|
| #1 | [`lab1`](../../tree/lab1) | REST API with CRUD operations for users |
| #2 | [`lab2`](../../tree/lab2) | PostgreSQL storage, SQLAlchemy, Alembic migrations, docker-compose |

Changes between labs: [lab1 → lab2](../../compare/lab1...lab2)

## Tech stack
Python, FastAPI, Pydantic, PostgreSQL, SQLAlchemy, Alembic, Docker Compose

## Getting started
cd users-api
docker compose up -d          # lab2+
pip install -r requirements.txt
cp .env.example .env
alembic upgrade head          # lab2+
uvicorn app.main:app --reload

API docs: http://localhost:8000/docs
