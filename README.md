# DevSecOps CI/CD Pipeline

## Overview
A Flask REST API packaged with Docker and validated through GitHub Actions. The workflow runs Ruff linting, pytest coverage, Gitleaks secret scanning, Semgrep static analysis, Trivy filesystem scanning, SonarQube analysis when configured, Docker image build, and Trivy image scanning.

## Technology stack
Python 3.12, Flask, SQLite, pytest, pytest-cov, Ruff, GitHub Actions, Gitleaks, Semgrep, Trivy, SonarQube, Docker, and Gunicorn.

## API endpoints
- `GET /` — project status.
- `GET /health` — health status.
- `GET /api/items` — list items.
- `POST /api/items` — create an item with JSON such as `{"name":"demo"}`.
- `GET /api/items/search?q=demo` — search item names.

## Run locally
Create a virtual environment:
```bash
python -m venv .venv
```
Windows PowerShell activation:
```powershell
.venv\Scripts\Activate.ps1
```
Install, lint, test, and run:
```bash
python -m pip install -r requirements-dev.txt
ruff check app tests
pytest --cov=app --cov-report=term
python -m app.main
```
The API listens on port 8000. Check `http://127.0.0.1:8000/health`.

## Docker
```bash
docker build -t devsecops-demo .
docker run --rm -p 8000:8000 devsecops-demo
```

## SonarQube
In GitHub repository Settings -> Secrets and variables -> Actions:
- Add variable `SONAR_HOST_URL` with your SonarQube server URL.
- Add secret `SONAR_TOKEN` with a project analysis token.
- Ensure `sonar.projectKey` matches your SonarQube project.
If credentials are missing, the workflow warns that SonarQube was skipped. Do not claim a scan ran unless it actually executed.

## Workflow
Runs on pushes and pull requests to `main` or `master`, and can be started manually. Test/lint failures and configured HIGH/CRITICAL Trivy findings can fail the workflow. Investigate findings instead of suppressing them.

## Evidence
Capture genuine screenshots of the repository, Actions run, Trivy results, and SonarQube dashboard if configured. The workflow is not verified until executed in your GitHub account.

## Limitations
This demonstration does not deploy to production or publish container images. For production use, pin third-party Actions to full commit SHAs, enforce a SonarQube quality gate, and add signed image publishing.
