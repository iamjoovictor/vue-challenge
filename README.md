# Vue Challenge — Inventory Management System

Full-stack inventory management application built with **Vue 3** on the frontend and **FastAPI** on the backend, featuring JWT authentication, product/category CRUD, and real-time WebSocket support.

---

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | Vue 3, TypeScript, PrimeVue 4, Vue Router 4, SCSS |
| Backend | Python 3, FastAPI, SQLAlchemy, Alembic |
| Database | MariaDB (MySQL-compatible) |
| Auth | JWT (Bearer token) |
| Testing | Pytest (backend) · Vitest + Cypress (frontend) |

---

## Project Structure

```
vue-challenge/
├── backend/          # FastAPI application
│   ├── src/
│   │   ├── api.py              # App entry point
│   │   ├── routes/             # Route definitions
│   │   ├── controllers/        # Request handlers
│   │   ├── services/           # Business logic
│   │   ├── models/             # SQLAlchemy models
│   │   ├── schemas/            # Pydantic schemas
│   │   ├── repository/         # DB queries
│   │   ├── middleware/         # Auth, utils
│   │   └── migrations/         # Alembic migrations
│   └── requirements.txt
├── frontend/         # Vue 3 application
│   ├── src/
│   │   ├── views/              # Page-level components
│   │   ├── components/         # UI components
│   │   ├── services/           # API service layer
│   │   ├── router/             # Vue Router config
│   │   ├── middleware/         # Interfaces, SCSS, services
│   │   └── environments/       # Env configs
│   └── package.json
└── environments/     # Shared environment variable files
```

---

## Prerequisites

- [Python 3.10+](https://www.python.org/downloads/)
- [Node.js 18+](https://nodejs.org/)
- [MariaDB 10.3+](https://mariadb.org/download/)

---

## 1. Backend Setup

### 1.1 Database

1. Install and start MariaDB, then connect with a client (e.g. HeidiSQL) using:

```
Host:     127.0.0.1
Port:     3306
User:     root
Password: root
```

> Credentials are defined in `environments/.env.dev`.

2. Create two databases (tables are created automatically by Alembic):

```sql
CREATE DATABASE `vue-challenge`;
CREATE DATABASE `vue-challenge-test`;
```

### 1.2 Python Environment

Run the following inside the `backend/` directory:

```sh
# Create and activate virtual environment
py -m venv venv
venv\Scripts\activate      # Windows
# source venv/bin/activate  # macOS / Linux

# Install dependencies
pip install -r requirements.txt
```

### 1.3 Run Migrations

```sh
alembic upgrade head
```

This creates all tables and seeds initial data (including the default `admin` user).

> If you get a connection error, verify the connection string in `backend/alembic.ini`:
> ```
> sqlalchemy.url = mysql+pymysql://root:root@localhost:3306/vue-challenge
> ```

### 1.4 Start the API

```sh
uvicorn src.api:app --reload
```

The API will be available at:
- **Base URL:** `http://127.0.0.1:8000`
- **Interactive docs (Swagger):** `http://127.0.0.1:8000/docs`

### 1.5 Run Backend Tests

Open a **second terminal** (keep the API running in the first), then:

```sh
cd backend
venv\Scripts\activate
pytest
```

Expected: **21 tests** passing.

---

## 2. Frontend Setup

### 2.1 Environment Variables

The frontend reads the backend URL from `environments/.env.dev`:

```env
BACKEND_URL=http://localhost:8000/
```

### 2.2 Install & Run

```sh
cd frontend
npm install
npm run dev
```

The app will be available at `http://localhost:5173`.

### 2.3 Default Credentials

```
Username: admin
Password: admin
```

### 2.4 Available Routes

| Route | Description | Auth required |
|---|---|---|
| `/login` | Login screen | No |
| `/registration` | Inventory dashboard | Yes |

### 2.5 Frontend Scripts

| Command | Description |
|---|---|
| `npm run dev` | Start dev server |
| `npm run build` | Production build |
| `npm run test:unit` | Run Vitest unit tests |
| `npm run test:e2e:dev` | Run Cypress e2e tests |
| `npm run lint` | Lint & auto-fix |

---

## 3. Alembic — Database Migrations

<details>
<summary><strong>Migration reference</strong></summary>

### 3.1 Overview

[Alembic](https://alembic.sqlalchemy.org/en/latest/tutorial.html) manages incremental database schema changes through versioned migration scripts located in `backend/src/migrations/versions/`.

### 3.2 Create a New Revision

```sh
alembic revision -m "describe_your_change"
```

Edit the generated file and implement `upgrade()` and `downgrade()`.

### 3.3 Apply / Rollback

```sh
alembic upgrade head       # Apply all pending migrations
alembic downgrade base     # Roll back all migrations
alembic downgrade -1       # Roll back one migration
```

### 3.4 Common Migration Snippets

**Create a table:**
```python
def upgrade():
    op.create_table(
        'table_name',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('name', sa.String(100), nullable=False),
        sa.Column('active', sa.Boolean, nullable=False, server_default='1'),
    )

def downgrade():
    op.drop_table('table_name')
```

**Add a column:**
```python
def upgrade():
    op.add_column('table_name', sa.Column('new_column', sa.String(50)))

def downgrade():
    op.drop_column('table_name', 'new_column')
```

</details>