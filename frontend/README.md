# Vue Challenge — Frontend

Vue 3 + TypeScript single-page application that provides the UI for the inventory management system. Built with Vite, PrimeVue 4, Vue Router 4, and SCSS.

---

## Tech Stack

| Tool | Version |
|---|---|
| Vue 3 | ^3.4 |
| TypeScript | ~5.4 |
| Vite | ^5.3 |
| PrimeVue | ^4.0 |
| Vue Router | ^4.3 |
| Vitest | ^1.6 |
| Cypress | ^13 |

---

## Project Structure

```
src/
├── App.vue               # Root component (only mounts <RouterView>)
├── main.ts               # App entry point — registers plugins
├── router/
│   └── index.ts          # Route definitions and navigation guards
├── views/
│   ├── LoginView.vue       # /login  — unauthenticated entry point
│   └── RegistrationView.vue # /registration — inventory dashboard (auth required)
├── components/
│   ├── login/             # LoginComponent
│   └── registration/      # RegistrationComponent
├── services/
│   ├── login/             # Login API service
│   ├── product/           # Product CRUD service
│   └── category/          # Category CRUD service
├── middleware/
│   ├── inteface/          # TypeScript interfaces (Category, Product, Login)
│   ├── service/           # Shared service utilities
│   ├── components/        # Toast notification service
│   └── scss/              # Global and PrimeVue style overrides
├── environments/
│   ├── environment.ts      # Dev environment config (BACKEND_URL, WS_URL)
│   └── environment.prod.ts # Production environment config
└── assets/
    ├── base.css
    └── main.scss
```

---

## Getting Started

### Prerequisites

- Node.js 18+
- Backend running at `http://localhost:8000` (see [root README](../README.md))

### Install dependencies

```sh
npm install
```

### Start development server

```sh
npm run dev
```

The app is served at **http://localhost:5173**.

### Default credentials

```
Username: admin
Password: @Test2026
```

---

## Available Routes

| Route | View | Auth required |
|---|---|---|
| `/login` | `LoginView.vue` | No |
| `/registration` | `RegistrationView.vue` | Yes |

---

## Scripts

| Command | Description |
|---|---|
| `npm run dev` | Start Vite dev server (mode: dev) |
| `npm run build` | Type-check + production build (mode: prod) |
| `npm run preview` | Serve the production build locally |
| `npm run test:unit` | Run Vitest unit tests |
| `npm run test:e2e:dev` | Open Cypress against the dev server |
| `npm run test:e2e` | Run Cypress against the production build |
| `npm run lint` | Lint & auto-fix with ESLint |
| `npm run format` | Format source files with Prettier |

---

## Environment Configuration

The frontend reads configuration from `environments/environment.ts` (dev) or `environments/environment.prod.ts` (prod), which are populated at build time from the shared `environments/.env.*` files.

| Variable | Description |
|---|---|
| `BACKEND_URL` | Base URL of the FastAPI backend (must end with `/`) |
| `WS_URL` | WebSocket base URL for real-time updates |

---

## IDE Setup

[VS Code](https://code.visualstudio.com/) + [Volar](https://marketplace.visualstudio.com/items?itemName=Vue.volar) (disable Vetur if installed).
