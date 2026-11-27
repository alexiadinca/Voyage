# Voyage

**AI Travel Planner.** Discover destinations with a machine learning ranking, explore points of interest on an interactive map and generate personalized day-by-day itineraries.

| Part | Stack |
|---|---|
| Frontend | Next.js, React, TypeScript, Tailwind CSS, React Leaflet |
| Backend | Python, FastAPI, Pydantic |
| Database and auth | Supabase (PostgreSQL and Supabase Auth) |
| Machine learning | pandas, scikit-learn (RandomForestRegressor) |
| External services | OpenStreetMap / Overpass, Open-Meteo, OpenAI |
| Tests and quality | pytest, Vitest, React Testing Library, Playwright, Ruff, ESLint, Prettier |

The full technical specification (`Voyage_Technical_Specification_v1.0.md`) is shared with the team separately and is **not** stored in the repository (it is git-ignored). Put your copy in the project root.

---

## Quick start

Once the tools in step 1 are installed, setting up takes three commands:

```bash
git clone <repository-url> Voyage
cd Voyage
python setup.py          # on macOS / Linux use: python3 setup.py
```

The sections below go through each step.

---

## Setup tutorial

### Step 1. Install the required tools (once per computer)

| Tool | Minimum version | Download |
|---|---|---|
| **Python** | 3.12 | https://www.python.org/downloads/ |
| **Node.js** (LTS, includes npm) | 20.9 | https://nodejs.org/ |
| **Git** | any recent | https://git-scm.com/downloads |
| VS Code (recommended) | any | https://code.visualstudio.com/ |

> **Windows:** in the Python installer, tick **"Add python.exe to PATH"** on the first screen.

When the installers finish, **close the terminal and open a new one**, then check that each tool is available:

```bash
python --version    # Python 3.12 or newer   (macOS/Linux: python3 --version)
node --version      # v20.9 or newer
npm --version
git --version
```

If any of these says "not recognized" or "command not found", that tool is not on your PATH. Reinstall it, or restart your computer.

### Step 2. Clone the repository

```bash
git clone <repository-url> Voyage
cd Voyage
```

### Step 3. Run the setup script

From the **project root folder** (the one containing `setup.py`):

```bash
# Windows
python setup.py

# macOS / Linux
python3 setup.py
```

The script takes a few minutes the first time and does the following:

1. Checks that Python, Node.js, npm and Git are installed and recent enough. If something is missing, it stops and tells you what to install.
2. Creates a Python virtual environment in `.venv/` and installs everything in [requirements.txt](requirements.txt): FastAPI, Supabase, scikit-learn, pandas, OpenAI, pytest, Ruff and the rest.
3. Installs the frontend packages in `frontend/` with `npm ci`, using the exact versions in `package-lock.json`.
4. Downloads the Chromium browser that Playwright uses for end-to-end tests.
5. Creates your personal config files `backend/.env` and `frontend/.env.local` from the `.example` templates.
6. Runs the backend and frontend tests to confirm everything works.

It finishes with **"Setup complete!"**.

You can run the script again at any time, for example after `git pull` when someone has added a dependency. It reuses what is already installed and never overwrites your `.env` files.

Optional flags:

| Flag | Effect |
|---|---|
| `--skip-browsers` | Skip the Playwright browser download (~300 MB) |
| `--skip-tests` | Skip the smoke tests at the end |
| `--recreate-venv` | Delete `.venv` and rebuild it from scratch (use this if Python packages get corrupted) |

### Step 4. Fill in the environment files

The setup script created two files with placeholder values:

| File | Contents |
|---|---|
| `backend/.env` | Supabase URL and keys, database URL, OpenAI key, service URLs |
| `frontend/.env.local` | Supabase URL and **anon (public)** key, backend API URL, map tile settings |

Ask the project manager for the team's values, or copy them from the Supabase dashboard (**Project Settings → API**).

> ⚠️ **Never commit `.env` files.** They are already in `.gitignore`. The Supabase **service-role key** and the **OpenAI key** go only in `backend/.env`, never in the frontend, because everything prefixed with `NEXT_PUBLIC_` is sent to the browser.

The app starts without real keys, so you can begin working right away. Only features that call Supabase or OpenAI need them.

### Step 5. Run the project

Open **two terminals** in the project root.

**Terminal 1: backend (FastAPI)**

```bash
# Windows (PowerShell)
.venv\Scripts\activate
# macOS / Linux
source .venv/bin/activate

cd backend
uvicorn app.main:app --reload
```

- API: http://localhost:8000/api/v1/health
- Interactive API docs (Swagger): http://localhost:8000/docs

**Terminal 2: frontend (Next.js)**

```bash
cd frontend
npm run dev
```

- App: http://localhost:3000

If the homepage says **"Backend is online"**, your setup is complete. 🎉

> **VS Code tip:** press `Ctrl+Shift+P`, choose **Python: Select Interpreter** and pick `.venv`. Imports will then resolve, and notebooks in `ml/notebooks/` will use the right kernel.

---

## Everyday commands

Run Python commands with the virtual environment **activated** (see step 5).

| Task | Command | Where |
|---|---|---|
| Backend tests | `pytest` | project root |
| Python lint | `ruff check .` | project root |
| Python auto-format | `ruff format .` | project root |
| Start backend | `uvicorn app.main:app --reload` | `backend/` |
| Start frontend | `npm run dev` | `frontend/` |
| Frontend unit tests | `npm test` | `frontend/` |
| End-to-end tests | `npm run test:e2e` | `frontend/` |
| Lint TypeScript | `npm run lint` | `frontend/` |
| Type-check | `npm run typecheck` | `frontend/` |
| Format frontend | `npm run format` | `frontend/` |
| Supabase CLI (migrations) | `npx supabase <command>` | project root |

---

## Adding a new dependency

Install new dependencies the same way every time, so the whole team stays in sync.

**Python package:**

```bash
# with .venv activated
pip install some-package
pip show some-package          # note the version
```

Add `some-package==X.Y.Z` to the matching section of [requirements.txt](requirements.txt) and commit it.

**Frontend package:**

```bash
cd frontend
npm install some-package       # or: npm install -D some-package   for dev tools
```

Commit **both** `package.json` and `package-lock.json`.

After pulling these changes, teammates just run `python setup.py` again.

---

## Project structure

```text
Voyage/
├── .gitignore               # single ignore file for the whole project
├── setup.py                 # one-command dev environment setup
├── requirements.txt         # pinned Python dependencies
├── pyproject.toml           # Ruff + pytest configuration
├── frontend/                # Next.js app (TypeScript, Tailwind, React Leaflet)
│   ├── src/app/             # routes (pages)
│   ├── src/components/      # reusable UI components
│   ├── src/features/        # feature modules (onboarding, map, itinerary…)
│   ├── src/lib/             # API client, Supabase client
│   ├── src/types/           # shared TypeScript types
│   └── e2e/                 # Playwright end-to-end tests
├── backend/                 # FastAPI modular monolith
│   ├── app/api/v1/          # REST endpoints under /api/v1
│   ├── app/core/            # config, security
│   ├── app/schemas/         # Pydantic request/response models
│   ├── app/services/        # business logic (recommendations, itinerary, budget…)
│   ├── app/repositories/    # database access
│   ├── app/ml/              # model loading and inference
│   └── tests/               # pytest tests
├── ml/                      # offline model training and evaluation
│   ├── data/  notebooks/  training/  evaluation/  artifacts/
├── data/                    # POI import and normalization scripts (Overpass/OSM)
│   ├── importers/  normalization/  seed/  validation/
├── supabase/                # SQL migrations and seed data
├── docs/                    # architecture, API, decisions, project management
└── .github/workflows/       # CI pipelines
```

---

## Troubleshooting

| Problem | Fix |
|---|---|
| `python` is not recognized (Windows) | Reinstall Python with **"Add python.exe to PATH"** ticked, or use `py setup.py`. Open a new terminal afterwards. |
| `python` opens the Microsoft Store (Windows) | Open **Settings → Apps → Advanced app settings → App execution aliases** and turn off both "python" aliases. |
| "Python 3.12+ is required" | Install a newer Python. Then run the script with it, for example `py -3.12 setup.py` (Windows) or `python3.12 setup.py` (macOS/Linux). |
| `.venv\Scripts\activate` says "running scripts is disabled" | Run this once in PowerShell: `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` |
| `npm ci` fails | Delete `frontend/node_modules` and run `python setup.py` again. |
| Python packages are broken or out of date | `python setup.py --recreate-venv` |
| Port 3000 or 8000 is already in use | Stop the other process, or run `uvicorn app.main:app --reload --port 8001` / `npm run dev -- -p 3001`. If you change the backend port, update `NEXT_PUBLIC_API_BASE_URL`. |
| Playwright tests fail on Linux | `cd frontend && sudo npx playwright install-deps chromium` |
| Homepage says "Backend is offline" | Start the backend in a second terminal (step 5), then refresh the page. |
