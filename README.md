# CrewPulse

CrewPulse is a local-first, science-conscious health monitoring and decision-support prototype for long-duration mission simulations. It is not a diagnostic tool and does not represent NASA endorsement.

The project now includes a structured FastAPI backend, SQLAlchemy persistence, JWT authentication boundaries, deterministic analysis services, a PostgreSQL Docker Compose setup, reproducible seed data, and the Next.js dashboard.

## Run the frontend locally

```bash
npm install
npm run dev
```

Open `http://localhost:3000`. The demo records are deterministic and visibly marked **SIMULATED**. The dashboard, chart, task state, and check-in action are functional in the browser. Data stays local to the prototype session; no server synchronization is implied.

## Run the backend locally

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r backend/requirements.txt
uvicorn backend.app.main:app --reload --port 8000
```

Set `DATABASE_URL` and `JWT_SECRET` from `.env.example`. The default backend URL expects PostgreSQL. The API exposes OpenAPI documentation at `http://localhost:8000/docs`.

## Docker

Docker is optional but provides PostgreSQL, the backend, and frontend together:

```bash
docker compose up --build
```

Seed the demo database after the services are ready:

```bash
python database/seed.py
```

The seed account is explicitly synthetic: `demo@crewpulse.local` / `demo-password`.

## Routes

`/`, `/dashboard`, `/health-check`, `/analytics`, `/body-map`, `/risk-assessment`, `/mission`, `/guidance`, and `/research`.

## Scientific boundaries

The analysis layer uses personal reference baselines only after sufficient observations and reports uncertainty when history is insufficient. It does not invent population thresholds or urgent escalation rules. Use the approved mission medical protocol for clinical decisions. Official starting resources include [NASA Human Research Program](https://www.nasa.gov/hrp/), [NASA Open Science Data Repository](https://osdr.nasa.gov/), and the [Human Research Roadmap](https://humanresearchroadmap.nasa.gov/evidence/).

## Backend API

Implemented API families include registration/login/me, missions, health measurement ingestion/listing, and explainable risk analysis under `/api/v1`. Measurements are isolated by authenticated astronaut profile and validated before persistence.

## Next steps

An operational version would need authenticated storage, validated measurement protocols, provenance-aware sensor ingestion, clinician review, accessibility testing, and formal scientific/medical validation before use.
