from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import httpx
import os

app = FastAPI(title="Cicuma Cortex", version="1.0.0")

CELL_URL = os.getenv("CELL_URL", "http://localhost:8002")

class BuildingInput(BaseModel):
    occupancy: str
    sqft: int
    ceiling_height: int
    occupants: int = 0

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
