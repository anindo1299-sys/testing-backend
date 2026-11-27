# FastAPI E-Commerce Backend

A containerized backend service built with FastAPI, MySQL, Redis, and Celery, orchestrated with Docker Swarm and automated via GitHub Actions on a self-hosted WSL2 runner.

## Tech Stack

- **API Framework:** FastAPI (Python 3.11) with Gunicorn & Uvicorn workers
- **Database & Migrations:** MySQL (async via `aiomysql`) and Alembic
- **Task Queue & Caching:** Redis & Celery
- **Containerization & Orchestration:** Docker & Docker Swarm
- **CI/CD:** GitHub Actions (self-hosted WSL2 runner)

## Project Structure

```text
.
├── .github/workflows/      # GitHub Actions CI/CD pipeline
├── app/                    # FastAPI application source code
├── alembic/                # Database migration scripts
├── Dockerfile.prod         # Production multi-stage Docker image
└── compose.prod.swarm.yaml # Docker Swarm stack configuration