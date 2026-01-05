# Build Fire Alarm System (Cicuma Architecture)

This project demonstrates the Neuro-Symbolic architecture of Cicuma.

## Components
1.  **Cortex (`/cortex`)**: 
    -   The orchestration layer. 
    -   Runs FastAPI.
    -   Handles User Input and routes to Cells.
2.  **Cell (`/cell_fire_alarm`)**:
    -   The deterministic worker.
    -   Runs FastAPI (microservice).
    -   Contains pure Python logic for FBC/NFPA compliance.
3.  **Knowledge Base (`/knowledge_base`)**:
    -   Stores the "Truth" (HTML/MD files of codes).

## Running
```bash
docker-compose up --build
```

## Flow
User -> Cortex (8001) -> Cell (8002) -> Cortex -> User

## Deployment (Google Cloud)
The project includes a unified console pipeline for GCP.

### Prerequisites
-   Google Cloud CLI (`gcloud`) installed.
-   A GCP Project ID.

### Deploy Command
```bash
cd build_fire_alarm
./deploy_gcp.sh [YOUR_PROJECT_ID]
```

This will:
1.  Enable Cloud Run & Artifact Registry APIs.
2.  Create the `cicuma-fire` container repo.
3.  Build & Push Docker images for `cortex`, `cell`, and `web`.
4.  Deploy them to Cloud Run (Serverless).
5.  Link them automatically (Web -> Cortex -> Cell).

## GitHub
To upload:
```bash
git remote add origin https://github.com/YOUR_USER/business_total.git
git push -u origin main
```
