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

## Quick Start with Docker

The easiest way to run the full stack. Requires [Docker Desktop](https://www.docker.com/products/docker-desktop/) and [Node.js 18+](https://nodejs.org/).

All Docker Compose commands are wrapped as `npm run` scripts at the project root:

| Command | Env file | Description |
|---|---|---|
| `npm run docker` | `.env.docker` | Start the full stack (Docker environment) |
| `npm run dev` | `.env.dev` | Start the full stack (dev environment) |
| `npm run prod` | `.env.prod` | Start the full stack (production environment) |
| `npm run test` | `.env.test` | Start the full stack (test environment) |
| `npm run local` | `.env.local` | Start the full stack (local environment) |
| `npm run down` | — | Stop all containers and remove volumes + images |

To start the stack with the default Docker environment:

```sh
npm run docker
```

| Service | URL |
|---|---|
| Frontend | http://localhost:5173 |
| Backend API | http://localhost:8000 |
| Swagger docs | http://localhost:8000/docs |
| MariaDB | localhost:3306 |

On first start the backend container automatically runs `alembic upgrade head`, creating all tables and seeding the default `admin` user.

To stop all containers and perform a full cleanup (removes containers, volumes, images, and orphan services):

```sh
npm run down
```

> **Note:** `npm run down` runs `docker compose down -v --remove-orphans --rmi all`. Images will be rebuilt on the next `npm run` start command.

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
Password: @Test2026
```

### 2.4 Available Routes

| Route | Description | Auth required |
|---|---|---|
| `/login` | Login screen | No |
| `/dashboard` | Inventory dashboard | Yes |

### 2.5 Frontend Scripts

| Command | Description |
|---|---|
| `npm run dev` | Start dev server (mode: dev) |
| `npm run build` | Type-check + production build (mode: prod) |
| `npm run preview` | Preview the production build locally |
| `npm run test:unit` | Run Vitest unit tests |
| `npm run test:e2e:dev` | Open Cypress against the dev server |
| `npm run test:e2e` | Run Cypress against the production build |
| `npm run lint` | Lint & auto-fix with ESLint |
| `npm run format` | Format source files with Prettier |

---

## API Reference

All protected endpoints require the header:
```
Authorization: Bearer <token>
```

### Authentication

| Method | Path | Auth | Description |
|---|---|---|---|
| `POST` | `/login/` | No | Returns a JWT Bearer token |

### Products

| Method | Path | Auth | Description |
|---|---|---|---|
| `GET` | `/product/` | Yes | List all products |
| `POST` | `/product/` | Yes | Create a product |
| `PUT` | `/product/` | Yes | Update a product |
| `DELETE` | `/product/?id_product={id}` | Yes | Delete a product by ID |

### Categories

| Method | Path | Auth | Description |
|---|---|---|---|
| `GET` | `/category/` | Yes | List all categories |
| `POST` | `/category/` | Yes | Create a category |
| `PUT` | `/category/` | Yes | Update a category |
| `DELETE` | `/category/?id_category={id}` | Yes | Delete a category by ID |

> The full interactive API docs (Swagger UI) are available at **http://localhost:8000/docs** when the backend is running.

---

## Environment Variables

All environment files live in `environments/`. Copy `.env.exemple` as a starting point.

| Variable | Description | Example |
|---|---|---|
| `ENVIRONMENT` | Environment label | `dev`, `docker` |
| `SHORT_ENV` | Short label used by Docker Compose | `dev`, `docker` |
| `DATABASE_USER` | MariaDB username | `root` |
| `DATABASE_PASSWORD` | MariaDB password | `root` |
| `DATABASE_HOST` | MariaDB host + port | `localhost:3306` |
| `DATABASE_NAME` | Main database name | `vue-challenge` |
| `TEST_DATABASE_NAME` | Test database name | `vue-challenge-test` |
| `MARIADB_ROOT_PASSWORD` | Root password (used by the DB container) | `root` |
| `BACKEND_URL` | Base URL used by the frontend to reach the API | `http://localhost:8000/` |
| `WS_URL` | WebSocket base URL | `ws://localhost:8000/` |
| `ACCESS_TOKEN_SECRET_KEY` | HS256 secret for signing JWTs | 64-char hex string |
| `ACCESS_TOKEN_ALGORITHM` | JWT algorithm | `HS256` |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Token lifetime in minutes | `30` |

> **Security:** Never commit a real `ACCESS_TOKEN_SECRET_KEY` to version control. Generate one with:
> ```sh
> openssl rand -hex 32
> ```

---

## WebSocket

The backend exposes a WebSocket endpoint that broadcasts inventory change events to connected clients. The frontend connects using `WS_URL` (defined in the environment file).

| Variable | Example |
|---|---|
| `WS_URL` | `ws://localhost:8000/` |

Use this URL in the frontend to subscribe to real-time updates (product/category changes).

---

## Troubleshooting

### Docker — containers exit immediately
- Run `docker compose logs backend` to inspect startup errors.
- Ensure the `environments/.env.docker` file exists and all required variables are set.
- Each `npm run <env>` command calls `npm run down` first, so a failed previous run is cleaned up automatically.

### Database connection refused (local dev)
- Confirm MariaDB is running: `mysqladmin ping -uroot -proot`
- Check the connection string in `backend/alembic.ini` matches your local credentials.
- If the `vue-challenge` database does not exist, create it manually (see §1.1).

### Alembic migration errors
- Make sure the virtual environment is activated before running `alembic upgrade head`.
- If you get a `Can't locate revision` error, run `alembic stamp head` to reset the migration state, then re-run `alembic upgrade head`.

### Pytest — `Connection refused`
- A running backend is **not** required; pytest uses its own in-process test database (`vue-challenge-test`).
- Confirm `TEST_DATABASE_NAME` in `environments/.env.dev` points to the test database and that the database exists.

### Frontend — `Network Error` on API calls
- Ensure `BACKEND_URL` in the active environment file ends with a trailing slash (`http://localhost:8000/`).
- Verify the backend is running on port 8000.
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