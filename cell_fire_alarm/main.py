from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import os

app = FastAPI(title="Cicuma Cell: Fire Alarm", version="2.0.0")

# RAG Knowledge Path
PROTOCOL_PATH = "/app/knowledge_base/FIRE_ALARM_DESIGN_PROTOCOL.md"
if not os.path.exists(PROTOCOL_PATH):
    PROTOCOL_PATH = "../FIRE_ALARM_DESIGN_PROTOCOL.md"

class BuildingInput(BaseModel):
    occupancy: str  # e.g., "R-2", "Business", "Mercantile", "Assembly"
    sqft: int
    ceiling_height: int
    occupants: int = 0
    num_stories: int = 1
    num_units: int = 0  # Crucial for R-2
    sprinklered: bool = False
    ai_overrides: Optional[dict] = {}

class DesignOutput(BaseModel):
    status: str
    system_type: str
    compliance_notes: List[str]
    bom_tier_a: List[str]
    bom_tier_b: List[str]

@app.post("/analyze", response_model=DesignOutput)
def analyze(input_data: BuildingInput):
    """
    Deterministic Logic for Fire Alarm Design.
    implements NFPA 101 (Life Safety) and NFPA 72 (National Fire Alarm Code).
    """
    print(f"[CELL] Analyzing: {input_data}")
    
    notes = []
    bom_a = []
    bom_b = []
    system_type = "None Required"
    
    # --- LOGIC ENGINE ---
    
    # 1. Occupancy & Requirement Analysis (NFPA 101)
    is_required = False
    
    if "R-2" in input_data.occupancy.upper() or "RESIDENTIAL" in input_data.occupancy.upper():
        # NFPA 101 30.3.4.1: Manual fire alarm system required if > 4 stories OR > 16 dwelling units.
        if input_data.num_stories > 4 or input_data.num_units > 16:
            is_required = True
            notes.append("System REQUIRED: R-2 Occupancy > 16 Units or > 4 Stories (NFPA 101 30.3.4.1).")
        elif input_data.num_units > 11:
             # Often a gray area or local amendment, flagging for check.
             notes.append("Check Local Amendments: R-2 with 12-16 units often requires system in South FL.")
        else:
            notes.append("System may NOT be required (Below R-2 Thresholds). Verify Local Amendments.")

    elif input_data.occupancy.lower() == "assembly":
        # Previous logic kept for compatibility
        if input_data.occupants > 300:
             is_required = True
             notes.append("Voice Evacuation System REQUIRED (>300 occupants/Assembly).")
             system_type = "Voice/Evac"

    elif input_data.occupancy.lower() in ["mercantile", "business", "mixed-use"]:
         # NFPA 101 36.3.4.1 (Mercantile): Class A > 30,000 sqft or 3 stories.
         if input_data.sqft > 30000 or input_data.num_stories > 3:
             is_required = True
             notes.append("System REQUIRED: Mercantile/Business threshold met.")
    
    # 2. System Type Determination
    if is_required and system_type == "None Required":
        system_type = "Addressable Fire Alarm (Manual + Automatic)"
        if input_data.sprinklered:
            notes.append("Sprinkler Monitoring REQUIRED (NFPA 72 / FBC 903.4).")
    
    # 3. Notification Rules (NFPA 72)
    # Phase 5: System Architecture & Power (AI Driven)
    
    # 5.1 FACP Selection (Point Count)
    # Estimate Points: 1 per Unit + 2 per Corridor + Pull Stations
    est_points = input_data.num_units + (input_data.num_stories * 2) + (input_data.num_stories * 2 + 1)
    
    # Add AI Override points
    if input_data.ai_overrides:
        rooms = input_data.ai_overrides.get("rooms", [])
        for r in rooms:
            est_points += len(r.get("components", []))
            
    facp_model = "Kidde VS4-G-2 (250 pts)" if est_points > 64 else "Kidde VS1-G-2 (64 pts)"
    if is_required:
        notes.append(f"System Load: {est_points} Estimated Addressable Points. Selected Panel: {facp_model}.")
    
    # 5.2 Power Calculations (24VDC)
    # Standby: 24 Hours, Alarm: 5 Minutes
    # Avg load per strobe: 0.035A, per sounder: 0.035A
    # Est Load: (Units + Corridors) * 0.035
    alarm_load_amps = (input_data.num_units + (input_data.num_stories * 2)) * 0.035
    standby_load_amps = 0.150 # Base panel load
    
    battery_ah = ((standby_load_amps * 24) + (alarm_load_amps * 0.0833)) * 1.2 # 20% Safety
    batt_size = "7Ah"
    if battery_ah > 7: batt_size = "10Ah"
    if battery_ah > 10: batt_size = "18Ah" # Requires external box usually
    
    if is_required:
        notes.append(f"Power Analysis: {alarm_load_amps:.2f}A Alarm Load. Battery Required: {battery_ah:.2f}Ah -> Use (2) 12V {batt_size}.")
    
    # 3. Notification Rules (NFPA 72)
    if is_required:
        # Tier A: Headend (Updated with Sizing)
        bom_a = [
            f"Addressable FACP: {facp_model}",
            "Remote Annunciator (Lobby)", 
            "Cellular/IP Communicator", 
            "Surge Protection (120V)", 
            "Doc Box",
            f"Batteries: (2) 12V {batt_size}"
        ]
        
        # Check for Booster (BPS)
        if alarm_load_amps > 6.0:
             bom_a.append("Booster Power Supply (BPS-10A) - Load Exceeds 6A")
             
        # Tier B: Notification Logic
        if "R-2" in input_data.occupancy.upper():
            notes.append("Sleeping Areas: 520Hz Low Frequency Sounders REQUIRED (NFPA 72 18.4.5).")
            bom_b.append(f"{input_data.num_units} x LF Sounder Bases / Mini-Horns (520Hz) [One per unit minimum]")
            bom_b.append(f"{input_data.num_stories} x Notification Circuits (Risers estimate)")
        
        notes.append("Corridors/Common Areas: Visible Notification (Strobes) required per ADA/NFPA.")
        bom_b.append("Wall Strobes (15cd/30cd based on coverage)")
        
        # Initiation Logic
        if input_data.sprinklered:
             bom_b.append("Monitor Modules (Flow/Tamper per Riser)")
        else:
             notes.append("Full Smoke Detection likely required if NOT sprinklered (Check 101.30.3.4.4).")
        
        bom_b.append(f"{input_data.num_stories * 2 + 1} x Pull Stations (Exits + FACP)")

    # 4. Integrate AI Vision Overrides (Phase 3: Automated Layout)
    if input_data.ai_overrides:
        print("[CELL] Processing AI Overrides...")
        rooms = input_data.ai_overrides.get("rooms", [])
        if rooms:
             notes.append(f"AI Vision Analysis Integrated: {len(rooms)} Rooms Scanned.")
             
             for room in rooms:
                 room_name = room.get("name", "Unknown Room")
                 components = room.get("components", [])
                 for comp in components:
                     sku = comp.get("sku", "Generic")
                     desc = comp.get("generic", "Device")
                     
                     # Add to BOM
                     bom_b.append(f"[AI MATCH] {desc} in {room_name} -> Spec: {sku}")

    return {
        "status": "Design Generated",
        "system_type": system_type,
        "compliance_notes": notes,
        "bom_tier_a": bom_a,
        "bom_tier_b": bom_b
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
