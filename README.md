# Module 12 – FastAPI User and Calculation Routes

This project implements user authentication and calculation BREAD operations using FastAPI, SQLAlchemy, Pydantic, Docker, GitHub Actions, and Docker Hub deployment.

## Project Overview

In this module, I connected the existing `User` and `Calculation` models to FastAPI routes so the application supports real REST API functionality for authentication and calculation management.

This project includes:

- User registration
- User login
- Token-based authentication
- Calculation BREAD routes:
  - Browse
  - Read
  - Edit
  - Add
  - Delete
- Pydantic validation for requests and responses
- Integration tests using pytest
- Dockerized app and Postgres database
- GitHub Actions CI pipeline
- Docker Hub image publishing
- Trivy security scanning

## Technologies Used

- FastAPI
- SQLAlchemy
- Pydantic
- PostgreSQL
- Docker / Docker Compose
- Pytest
- GitHub Actions
- Docker Hub

## API Endpoints

### Health
- `GET /health`

### Authentication
- `POST /auth/register`
- `POST /auth/login`
- `POST /auth/token`

### Calculations
- `GET /calculations`
- `POST /calculations`
- `GET /calculations/{calc_id}`
- `PUT /calculations/{calc_id}`
- `DELETE /calculations/{calc_id}`

## How to Run the Project Locally

### 1. Clone the repository

```bash
git clone https://github.com/danielleev33/module12_is601.git
cd module12_is601