# Fire Alarm System Documentation

## Architecture
The system follows a Neuro-Symbolic architecture:
- **Web (`/web`)**: Next.js 16 frontend. User interface for inputting building parameters.
- **Cortex (`/cortex`)**: Python FastAPI orchestrator. Routes requests to specific cells.
- **Cell (`/cell_fire_alarm`)**: Python FastAPI worker. Contains deterministic logic for FBC/NFPA compliance.

## Running Locally

### Prerequisites
- Node.js (v18+)
- Python 3.9+
- Docker (optional but recommended for full stack)

### 1. Web (Frontend)
```bash
cd web
npm install
npm run dev
```

### 2. Cortex (Orchestrator)
```bash
cd cortex
pip install -r requirements.txt
python main.py
```

### 3. Cell (Worker)
```bash
cd cell_fire_alarm
pip install -r requirements.txt
python main.py
```

## Troubleshooting Log
*Tracing issues encountered during `2026-01-07` session.*

### Issue 1: [RESOLVED] Build Verification
- **Symptom**: Suspected code errors.
- **Investigation**: 
  - `web`: `npm run build` passed.
  - `cortex` & `cell`: `py_compile` passed.
- **Status**: Codebase seems syntactically correct.

### Issue 2: [RESOLVED] Deployment Prerequisites
- **Symptom**: Potential missing CLI tools.
- **Investigation**: 
  - `gcloud`: Installed (v550.0.0).
  - `docker`: Installed (v29.1.2).
- **Status**: Environment is ready for deployment.

### Issue 3: [RESOLVED] Local Runtime (Docker Compose)
- **Status**: **ACTIVE**. Docker is running.
- **Automation**: Created `run_local.sh` to auto-start Docker if missing.
- **Action**: Running `run_local.sh` now.

### Issue 4: [BLOCKED] Cloud Deployment
- **Project ID**: `cicuma-fire-1767585900`
- **Error**: `Reauthentication required` (happens on `repo create`, `build submit`, etc).
- **Diagnosis**: The `gcloud` session has lost write privileges or requires a refresh.
- **Action**: User MUST run `gcloud auth login` interactively.

## Verification Summary
### Local Deployment (ACTIVE)
- **Status**: ✅ **SUCCESS**
- **URLs**:
  - Web: [http://localhost:3000](http://localhost:3000)
  - Cortex: [http://localhost:8001](http://localhost:8001)
  - Cell: [http://localhost:8002/docs](http://localhost:8002/docs)
- **Fixes Applied**:
  - Corrected Backend Ports (8000 -> 8080).
  - Added `web` service to Docker Compose.
  - Created `run_local.sh` for one-click start.

### Cloud Deployment (ACTIVE)
- **Status**: ✅ **SUCCESS**
- **URLs**:
  - **Web**: [https://cicuma-web-yp7mw3rcmq-uc.a.run.app](https://cicuma-web-yp7mw3rcmq-uc.a.run.app)
  - **Cortex**: [https://cicuma-cortex-yp7mw3rcmq-uc.a.run.app](https://cicuma-cortex-yp7mw3rcmq-uc.a.run.app)
  - **Cell**: [https://cicuma-cell-fire-yp7mw3rcmq-uc.a.run.app/docs](https://cicuma-cell-fire-yp7mw3rcmq-uc.a.run.app/docs)

## System Capabilities (v2.0)
The system now supports **Residential (R-2)** and **Mixed-Use** logic:
- **Requirement Logic**: Checks NFPA 101 thresholds (>16 Units, >4 Stories).
- **Detection Logic**: Enforces 520Hz Low-Frequency sounders in sleeping areas (NFPA 72).
- **BOM Generation**: Auto-calculates quantities for units, risers, and common areas.
- **Smart Ingestion (New)**: Upload an Arch Set (PDF) to auto-detect Occupancy, SqFt, and Units using Heuristics.
