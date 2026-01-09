import os
import csv
import sqlalchemy
from sqlalchemy.orm import Session
from database import SessionLocal, engine, Base
from models import Component
import pandas as pd
from typing import List
from google.cloud import aiplatform
from vertexai.language_models import TextEmbeddingInput, TextEmbeddingModel

# Constants
PROJECT_ID = os.getenv("GCP_PROJECT", "cicuma-fire-1767585900")
LOCATION = "us-central1" 

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def generate_embedding(text: str) -> List[float]:
    """Generates a 768-dimensional embedding using Vertex AI."""
    try:
        # Initialize Vertex AI
        aiplatform.init(project=PROJECT_ID, location=LOCATION)
        
        # Load the model
        model = TextEmbeddingModel.from_pretrained("text-embedding-004")
        
        # Vertex AI expects a list of inputs
        inputs = [TextEmbeddingInput(text, "RETRIEVAL_DOCUMENT")]
        embeddings = model.get_embeddings(inputs)
        
        if embeddings:
            return embeddings[0].values
        return [0.0] * 768
        
    except Exception as e:
        print(f"Error generating embedding for '{text[:20]}...': {e}")
        return [0.0] * 768

def ingest_csv(csv_path: str):
    """Reads the CSV and ingests components into the Vector DB."""
    print("Creating database tables if they don't exist...")
    
    # Enable pgvector extension
    with engine.connect() as connection:
        connection.execute(sqlalchemy.text("CREATE EXTENSION IF NOT EXISTS vector"))
        connection.commit()
    
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    
    print(f"Reading CSV from {csv_path}...")
    try:
        df = pd.read_csv(csv_path)
    except Exception as e:
        print(f"Error reading CSV: {e}")
        return

    total = len(df)
    print(f"Found {total} components. Starting ingestion with Vertex AI...")

    count = 0
    # Process in batches to be efficient with API calls
    for index, row in df.iterrows():
        full_text = f"{row['Category']} {row['Part Number']} {row['Long Description']}"
        
        # Simple check to avoid duplicates (naive)
        exists = db.query(Component).filter(Component.part_number == row['Part Number']).first()
        if exists:
            continue

        embedding = generate_embedding(full_text)
        
        component = Component(
            category=row['Category'],
            part_number=row['Part Number'],
            description=row['Long Description'],
            price=float(row['MSRP/Trade Price'].replace('$','').replace(',','')) if pd.notna(row['MSRP/Trade Price']) else 0.0,
            metadata_info={
                "manufacturer": row['Parent Category'],
                "agency": row['Agency'] if pd.notna(row['Agency']) else None
            },
            embedding=embedding
        )
        
        db.add(component)
        count += 1
        
        if count % 10 == 0:
            print(f"Processed {count} items...")
            db.commit()

    db.commit()
    print(f"Successfully ingested {count} components into the Vector Database.")

if __name__ == "__main__":
    # Path mapped via Docker volume
    CSV_PATH = "/data/data_base.csv"
    ingest_csv(CSV_PATH)
