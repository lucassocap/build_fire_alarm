from fastapi import FastAPI, HTTPException, UploadFile, File, Depends, Response
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy.orm import Session
from typing import List, Optional
import httpx
import os
import re
from pypdf import PdfReader
import io

# DB Imports
from database import engine, get_db, Base
from models import Project, AiAuditLog
from report_service import PDFReportService

from vision_service import VisionEngine
import json
import io
import uuid
from datetime import datetime

app = FastAPI(title="Cicuma Cortex", version="2.1.0")

# Create Tables
Base.metadata.create_all(bind=engine)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

CELL_URL = os.getenv("CELL_URL", "http://localhost:8002")

class BuildingInput(BaseModel):
    occupancy: str
    sqft: int
    ceiling_height: int
    occupants: int = 0
    num_stories: int = 1
    num_units: int = 0
    sprinklered: bool = False
    ai_overrides: Optional[dict] = {}

from vision_service import VisionEngine
import json
import io

@app.post("/analyze-pdf")
async def analyze_pdf(file: UploadFile = File(...), db: Session = Depends(get_db)):
    """
    Ingests a PDF, visualizes it, and uses GenAI to extract building parameters.
    """
    print(f"[CORTEX] Analyzing PDF (Visual AI): {file.filename}")
    
    try:
        content = await file.read()
        
        # Initialize Vision Engine
        vision = VisionEngine(db)
        
        # 1. Convert PDF to Image (Analyze 1st Page for now)
        # In a real scenario, we'd        # 1. Convert PDF to Image (Analyze 1st Page for now)
        images = vision.convert_pdf_to_images(content)
        
        if not images:
            raise HTTPException(status_code=400, detail="Could not convert PDF to Image.")
            
        print(f"[CORTEX] Converted PDF to {len(images)} images. Analyzing Page 1...")
        
        # Convert first page to bytes
        img_byte_arr = io.BytesIO()
        images[0].save(img_byte_arr, format='JPEG')
        img_bytes = img_byte_arr.getvalue()
        
        # Start Workflow ID
        workflow_id = str(uuid.uuid4())
        
        # 2. Vision Analysis (RAG + Vision)
        print("Calling vision.analyze_plan...")
        ai_response = {}
        
        # Log Step 1: Vision Request
        log_vision = AiAuditLog(
            workflow_id=workflow_id,
            step_name="vision_analysis",
            input_data={"filename": file.filename, "file_size": len(content)},
            model_name="gemini-1.0-pro-vision" # Hardcoded for now as attribute access failed
        )
        db.add(log_vision)
        db.commit()
        
        start_time = datetime.utcnow()
        try:
            ai_response = vision.analyze_plan(img_bytes)
            print(f"Vision response received (type: {type(ai_response)})")
        except Exception as e:
            print(f"CRITICAL ERROR in analyze_plan call: {e}")
            ai_response = {"error": str(e)}
        
        # Log Step 1: Vision Response
        log_vision.output_data = ai_response if isinstance(ai_response, dict) else {"raw": str(ai_response)}
        log_vision.latency_ms = int((datetime.utcnow() - start_time).total_seconds() * 1000)
        db.commit()

        # 3. Parse JSON
        ai_data = {}
        if isinstance(ai_response, dict):
            # It's an error or pre-parsed dict
            if "error" in ai_response:
                print(f"[CORTEX] Vision Error: {ai_response['error']}")
            else:
                ai_data = ai_response
        else:
            try:
                # It's a string (JSON)
                clean_json = ai_response.replace("```json", "").replace("```", "")
                ai_data = json.loads(clean_json)
                # Update log if we parsed it successfully
                log_vision.output_data = ai_data
                db.commit()
            except json.JSONDecodeError:
                print(f"[CORTEX] Failed to parse AI JSON: {ai_response}")

        print(f"[CORTEX] Vision AI Result: {ai_data}")

        # 4. Map to Standard Output & RAG Enrichment
        enriched_rooms = []
        
        if "rooms" in ai_data and isinstance(ai_data["rooms"], list):
            for room in ai_data["rooms"]:
                if "needs" in room and isinstance(room["needs"], list):
                    # RAG Step: For each need, find a component
                    found_components = []
                    for need in room["needs"]:
                        
                        # Log Step 2: RAG Retrieval
                        log_rag = AiAuditLog(
                            workflow_id=workflow_id,
                            step_name="rag_retrieval",
                            input_data={"query": need},
                            model_name="keyword_search_ilike"
                        )
                        db.add(log_rag)
                        db.commit()
                        rag_start = datetime.utcnow()
                        
                        # e.g. need="Smoke" -> search DB
                        matches = vision.retrieve_relevant_components(need, limit=1)
                        
                        # Log Step 2: RAG Response
                        log_rag.output_data = {"matches": matches}
                        log_rag.latency_ms = int((datetime.utcnow() - rag_start).total_seconds() * 1000)
                        db.commit()
                        
                        if matches:
                            # Attach the top match
                            found_components.append({
                                "generic": need,
                                "sku": matches[0]["part_number"],
                                "desc": matches[0]["description"]
                            })
                        else:
                             found_components.append({"generic": need, "sku": "UNKNOWN", "desc": "No Match"})
                    
                    room["components"] = found_components
                enriched_rooms.append(room)
        
        # Update ai_data with enriched info
        ai_data["rooms"] = enriched_rooms

        extracted_data = {
            "occupancy": ai_data.get("occupancy", "Unknown"),
            "sqft": 0,
            "num_stories": 1,
            "num_units": 0,
            "sprinklered": False,
            "ai_analysis": ai_data
        }

        return extracted_data

    except Exception as e:
        print(f"Error processing PDF: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# --- Project Management Endpoints ---

class ProjectCreate(BaseModel):
    name: str = "Untitled Project"
    location: str = "Unknown"
    input_data: BuildingInput # The intake form
    result_data: Optional[dict] = {} # The output from Cell

class ProjectResponse(BaseModel):
    id: str
    name: str
    location: str
    status: str
    created_at: str
    
    class Config:
        orm_mode = True

@app.post("/projects")
def create_project(project: ProjectCreate, db: Session = Depends(get_db)):
    """
    Save a new project to the database.
    """
    new_project = Project(
        name=project.name,
        location_address=project.location,
        status="SAVED",
        data={
            "input": project.input_data.dict(),
            "result": project.result_data
        }
    )
    db.add(new_project)
    db.commit()
    db.refresh(new_project)
    print(f"[CORTEX] Project Saved: {new_project.id}")
    return {"id": new_project.id, "status": "Saved"}

@app.get("/projects")
def list_projects(db: Session = Depends(get_db)):
    """
    List all projects.
    """
    projects = db.query(Project).order_by(Project.created_at.desc()).all()
    # Simple serialization
    return [
        {
            "id": p.id, 
            "name": p.name, 
            "location": p.location_address, 
            "status": p.status,
            "created_at": p.created_at.isoformat()
        } 
        for p in projects
    ]

@app.get("/projects/{project_id}")
def get_project(project_id: str, db: Session = Depends(get_db)):
    """
    Get a single project by ID.
    """
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    return {
        "id": project.id,
        "name": project.name,
        "location": project.location_address,
        "status": project.status,
        "created_at": project.created_at.isoformat(),
        "input_data": project.data.get("input"),
        "result_data": project.data.get("result")
    }

@app.get("/projects/{project_id}/pdf")
def generate_project_pdf(project_id: str, db: Session = Depends(get_db)):
    """
    Generate and return a PDF report for the project.
    """
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
        
    # Serialize project data for the report service
    project_data = {
        "name": project.name,
        "location_address": project.location_address,
        "data": project.data
    }
    
    report_service = PDFReportService()
    pdf_buffer = report_service.generate_report(project_data)
    
    filename = f"{project.name.replace(' ', '_')}_Fire_Design.pdf"
    
    return Response(
        content=pdf_buffer.getvalue(),
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )

@app.get("/")
def health():
    return {"status": "Cortex Online", "mode": "Orchestrator"}

@app.post("/design/fire-alarm")
async def generate_design(input_data: BuildingInput):
    """
    Orchestrates the design process.
    1. Receives Input.
    2. (Future) Queries Knowledge Base for specific constraints.
    3. Forwards to Cell for deterministic calculation.
    """
    print(f"[CORTEX] Received Input: {input_data}")
    
    async with httpx.AsyncClient() as client:
        try:
            # Forwarding to the Cell
            response = await client.post(f"{CELL_URL}/analyze", json=input_data.dict())
            response.raise_for_status()
            return response.json()
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Cell Communication Failed: {e}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
