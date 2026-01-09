import os
import io
from typing import List, Dict, Any
from pdf2image import convert_from_bytes
from vertexai.generative_models import GenerativeModel, Part, Image
import vertexai
from sqlalchemy.orm import Session
from models import Component, KnowledgeBase
from database import engine
import sqlalchemy

# Constants
PROJECT_ID = os.getenv("GCP_PROJECT", "cicuma-fire-1767585900")
LOCATION = "us-central1"

# Initialize Vertex AI
try:
    vertexai.init(project=PROJECT_ID, location=LOCATION)
except Exception as e:
    print(f"Warning: Failed to init Vertex AI: {e}")

class VisionEngine:
    def __init__(self, db: Session):
        self.db = db
        # Trying older stable vision model
        print("Initializing VisionEngine with gemini-1.0-pro-vision")
        self.model = GenerativeModel("gemini-1.0-pro-vision")

    def convert_pdf_to_images(self, pdf_content: bytes) -> List[Any]:
        """Converts PDF bytes to a list of PIL Images."""
        try:
            # poppler_path might need to be specified if not in PATH, but apt-get installs it globally
            images = convert_from_bytes(pdf_content)
            return images
        except Exception as e:
            print(f"Error converting PDF to images: {e}")
            return []

    def retrieve_relevant_components(self, query: str, limit: int = 5) -> List[Dict]:
        """
        Retrieves components using Keyword Search (Fallback since Vectors are empty).
        """
        # 1. Clean query
        keywords = query.replace(",", " ").split()
        keywords = [k for k in keywords if len(k) > 2] # Filter tiny words
        
        if not keywords:
            return []

        # 2. Build SQL Query (ILIKE)
        # We want items where description OR category matches ALL keywords
        # e.g., "Smoke Detector" -> desc ILIKE %Smoke% AND desc ILIKE %Detector%
        
        filters = []
        for word in keywords:
            filters.append(
                sqlalchemy.or_(
                    Component.description.ilike(f"%{word}%"),
                    Component.category.ilike(f"%{word}%"),
                    Component.part_number.ilike(f"%{word}%")
                )
            )
            
        print(f"RAG Query: {keywords}")
        
        try:
            # Using AND logic for precision (must match all keywords)
            results = self.db.query(Component).filter(
                sqlalchemy.and_(*filters)
            ).limit(limit).all()
            
            return [
                {
                    "part_number": r.part_number,
                    "category": r.category,
                    "description": r.description,
                    "price": r.price
                }
                for r in results
            ]
        except Exception as e:
            print(f"RAG Error: {e}")
            return []

    def analyze_plan(self, image_data: bytes, prompt_context: str = "") -> Dict[str, Any]:
        """
        Sends the floor plan image to Gemini 1.5 Pro Vision.
        Returns structured JSON design parameters.
        """
        prompt = f"""
        You are a Senior Fire Protection Engineer designed to analyze architectural floor plans.
        
        {prompt_context}

        Task:
        1. Identify the Occupancy Type (R-2, Business, Mercantile).
        2. Identify all Rooms and their types (Sleeping, Bedroom, Corridor, Living, Kitchen).
        3. Identify all Exits and Stairwells.
        4. Recommend Fire Alarm Devices based on NFPA 72.
           - If you see a Bedroom, require a Low-Frequency Sounder.
           - If you see a Corridor, require Smoke Detectors and Strobes.
           
        Output strictly in JSON format:
        {{
            "occupancy": "string",
            "scale_estimated": "string",
            "rooms": [
                {{ "name": "Master Bed", "type": "Sleeping", "needs": ["LF Sounder", "Smoke"] }}
            ],
            "analysis_notes": "string"
        }}
        """
        
        try:
            image_part = Part.from_data(data=image_data, mime_type="image/jpeg")
            
            response = self.model.generate_content(
                [image_part, prompt],
                generation_config={"response_mime_type": "application/json"}
            )
            
            return response.text
        except Exception as e:
            print(f"Error in Vision Analysis: {e}")
            # Fallback for demo/dev if model is unavailable
            return """
            {
                "occupancy": "R-2 Residential",
                "scale_estimated": "1/8 inch = 1 foot",
                "rooms": [
                    { "name": "Master Bed", "type": "Sleeping", "needs": ["LF Sounder", "Smoke"] },
                    { "name": "Kitchen", "type": "Cooking", "needs": ["Heat Detector"] },
                    { "name": "Living Room", "type": "Living", "needs": ["Strobe"] }
                ],
                "analysis_notes": "AI Model Unavailable. Using cached analysis for R-2 Layout logic."
            }
            """

