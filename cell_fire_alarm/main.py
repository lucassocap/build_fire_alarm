from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os

app = FastAPI(title="Cicuma Cell: Fire Alarm", version="1.0.0")

# RAG: In a real container, this volume is mounted
PROTOCOL_PATH = "/app/knowledge_base/FIRE_ALARM_DESIGN_PROTOCOL.md"
# Local Fallback
if not os.path.exists(PROTOCOL_PATH):
    PROTOCOL_PATH = "../FIRE_ALARM_DESIGN_PROTOCOL.md"

class BuildingInput(BaseModel):
    occupancy: str
    sqft: int
    ceiling_height: int
    occupants: int = 0

@app.post("/analyze")
def analyze(input_data: BuildingInput):
    """
    Deterministic Logic for Fire Alarm Design.
    """
    print(f"[CELL] Analyzing: {input_data}")
    
    design_notes = []
    
    # 1. Occupancy Logic
    if input_data.occupancy.lower() == "assembly":
        if input_data.sqft > 10000 or input_data.occupants > 300: # NFPA 101 rule constraint
             design_notes.append("Voice Evacuation System REQUIRED (>300 occupants/Assembly).")
        else:
             design_notes.append("Horn/Strobe Notification sufficient.")
    
    # 2. Ceiling Logic
    if input_data.ceiling_height > 15:
        design_notes.append(f"High Ceiling ({input_data.ceiling_height}ft). Beam Detectors recommended to avoid stratification.")
    
    return {
        "status": "Design Generated",
        "cell": "CellFireAlarm",
        "compliance": design_notes,
        "source": "NFPA 72 / FBC (Simulated)"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
