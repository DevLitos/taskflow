<div align="center">

# ✅ TaskFlow

**A lightweight RESTful task manager built with FastAPI and PostgreSQL.**

[![Python 3.12+](https://img.shields.io/badge/python-3.12%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![PostgreSQL 17](https://img.shields.io/badge/PostgreSQL-17-4169E1?logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![Docker](https://img.shields.io/badge/Docker-2496ED?logo=docker&logoColor=white)](https://www.docker.com/)
[![License: MIT](https://img.shields.io/badge/license-MIT-yellow.svg)](#license)

</div>

---

## 📖 About

**TaskFlow** is a clean, minimal REST API for managing tasks (to‑dos). It exposes a full **CRUD** interface over HTTP and persists data in a PostgreSQL database. The project is fully containerised with Docker Compose, making it easy to spin up locally or deploy to any environment.

---

## 🏗️ Tech Stack

| Layer | Technology |
|---|---|
| **Language** | Python 3.12 |
| **Framework** | FastAPI |
| **Database** | PostgreSQL 17 |
| **DB Driver** | psycopg 3 (binary) |
| **Validation** | Pydantic v2 |
| **Server** | Uvicorn |
| **Packaging** | uv |
| **Containers** | Docker + Docker Compose |

---

## 📂 Project Structure

```
taskflow/
├── src/taskflow/
│   ├── __init__.py
│   ├── main.py              # FastAPI app & lifespan setup
│   ├── api/
│   │   ├── health.py         # Health & DB connectivity checks
│   │   └── tasks.py          # Task CRUD endpoints
│   ├── db/
│   │   └── database.py       # Table creation on startup
│   ├── schemas/
│   │   └── task.py           # Pydantic request/response models
│   └── services/
│       └── task_service.py   # Business logic & SQL queries
├── compose.yaml              # Docker Compose orchestration
├── Dockerfile                # Multi-stage build with uv
├── pyproject.toml            # Project metadata & dependencies
├── uv.lock                   # Deterministic dependency lock
├── .env                      # Environment variables (not tracked)
└── README.md
```

---

## 🚀 Getting Started

### Prerequisites

- [Docker](https://docs.docker.com/get-docker/) & [Docker Compose](https://docs.docker.com/compose/install/) **or**
- [Python 3.12+](https://www.python.org/downloads/) & [uv](https://docs.astral.sh/uv/) for local development

### 1 — Clone the repository

```bash
git clone https://github.com/<your-username>/taskflow.git
cd taskflow
```

### 2 — Configure environment variables

Create a `.env` file in the project root:

```env
POSTGRES_DB=taskflow
POSTGRES_USER=taskflow
POSTGRES_PASSWORD=your_secure_password
```

### 3a — Run with Docker Compose (recommended)

```bash
# Build the image
docker build -t taskflow:1.0 .

# Start all services
docker compose up -d
```

This starts:
- **taskflow-api** on `http://localhost:8000`
- **taskflow-db** (PostgreSQL 17) with a health check — the API waits until the database is ready.

### 3b — Run locally (without Docker)

```bash
# Install dependencies
uv sync

# Make sure DATABASE_URL is set
export DATABASE_URL="postgresql://taskflow:your_secure_password@localhost:5432/taskflow"

# Start the server
uvicorn taskflow.main:app --reload
```

---

## 📡 API Reference

Base URL: `http://localhost:8000`

### Health

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/` | Root check — returns `{"message": "Running"}` |
| `GET` | `/health` | Health check — returns `{"status": "healthy"}` |
| `GET` | `/db-check` | Database connectivity check |

### Tasks

| Method | Endpoint | Description | Status |
|---|---|---|---|
| `POST` | `/tasks` | Create a new task | `201 Created` |
| `GET` | `/tasks` | List all tasks | `200 OK` |
| `GET` | `/tasks/{task_id}` | Get a task by ID | `200 OK` |
| `PATCH` | `/tasks/{task_id}` | Update task completion status | `200 OK` |
| `DELETE` | `/tasks/{task_id}` | Delete a task | `204 No Content` |

### Request & Response Examples

#### Create a task

```bash
curl -X POST http://localhost:8000/tasks \
  -H "Content-Type: application/json" \
  -d '{"name": "Buy groceries"}'
```

```json
{
  "id": 1,
  "name": "Buy groceries",
  "completed": false
}
```

#### List all tasks

```bash
curl http://localhost:8000/tasks
```

```json
[
  {
    "id": 1,
    "name": "Buy groceries",
    "completed": false
  }
]
```

#### Update task status

```bash
curl -X PATCH http://localhost:8000/tasks/1 \
  -H "Content-Type: application/json" \
  -d 'true'
```

```json
{
  "id": 1,
  "name": "Buy groceries",
  "completed": true
}
```

#### Delete a task

```bash
curl -X DELETE http://localhost:8000/tasks/1
# 204 No Content
```

### Interactive Docs

FastAPI auto-generates interactive API documentation:

- **Swagger UI** → [`http://localhost:8000/docs`](http://localhost:8000/docs)
- **ReDoc** → [`http://localhost:8000/redoc`](http://localhost:8000/redoc)

---

## 🗄️ Database Schema

The `tasks` table is automatically created on application startup:

```sql
CREATE TABLE IF NOT EXISTS tasks (
    id        SERIAL PRIMARY KEY,
    name      TEXT    NOT NULL,
    completed BOOLEAN NOT NULL DEFAULT FALSE
);
```

---

## 🐳 Docker

### Build the image

```bash
docker build -t taskflow:1.0 .
```

### Full stack with Compose

```bash
docker compose up -d      # Start
docker compose logs -f     # Follow logs
docker compose down        # Stop
docker compose down -v     # Stop and remove volumes
```

| Service | Container | Port |
|---|---|---|
| API | `taskflow-api` | `8000` |
| Database | `taskflow-db` | `5432` (internal) |

> [!NOTE]
> The PostgreSQL database uses a named volume (`postgres_data`) for data persistence across restarts.

---

## 🛠️ Development

```bash
# Install dependencies
uv sync

# Run with hot-reload
uvicorn taskflow.main:app --reload

# Add a new dependency
uv add <package>
```

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).

---

<div align="center">

**Built with ❤️ by [DevLitos](https://github.com/DevLitos)**

</div>
