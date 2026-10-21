# Project Report: DevSecOps CI/CD Pipeline

## Abstract
This project integrates testing and security checks into a continuous integration workflow. GitHub Actions coordinates linting, tests, secret scanning, static analysis, repository scanning, optional SonarQube analysis, container building, and image scanning.

## Problem Statement
Manual security checks can be inconsistent and allow defects or vulnerable dependencies to be missed. Automated pipeline checks provide repeatable feedback during code changes.

## Objectives
1. Automate linting and unit tests.
2. Measure test coverage.
3. Detect committed secrets.
4. Perform static analysis on Python and Flask code.
5. Scan source files and the Docker image for high-severity vulnerabilities.
6. Integrate SonarQube.
7. Package the API as a container.

## Technologies
Python, Flask, SQLite, pytest, pytest-cov, Ruff, GitHub Actions, Gitleaks, Semgrep, Trivy, SonarQube, Docker, and Gunicorn.

## Methodology
1. A developer pushes code to GitHub.
2. GitHub Actions starts the workflow.
3. Ruff checks style and pytest runs tests.
4. Gitleaks scans repository history for secrets.
5. Semgrep analyzes Python and Flask code.
6. Trivy scans repository files.
7. SonarQube runs when configured with a server URL and token.
8. Docker builds the image.
9. Trivy scans the image against configured severity thresholds.

## Expected Results
The workflow provides repeatable test and security results. Failed tests, lint errors, or configured HIGH/CRITICAL Trivy findings can fail jobs. Record the actual outcomes from GitHub Actions.

## Security Considerations
The API uses parameterized SQL, validates item names, and sets HTTP security headers. The container runs as a non-root user. Tokens belong in GitHub secrets, not source code.

## Limitations
SonarQube requires an accessible server and token. Scan results can change as vulnerability databases update. This demo does not deploy to production or publish images.

## Conclusion
The project demonstrates embedding automated tests and security checks in CI/CD. Future work includes enforcing a SonarQube quality gate, pinning actions to full commit SHAs, publishing signed images, and controlled Kubernetes deployment.
