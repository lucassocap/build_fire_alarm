from sqlalchemy import Column, String, Integer, JSON, DateTime, Boolean, Float
from sqlalchemy.dialects.postgresql import UUID
import uuid
from datetime import datetime
from database import Base

class Project(Base):
    __tablename__ = "projects"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, index=True)
    location_address = Column(String, nullable=True)
    status = Column(String, default="DRAFT") # DRAFT, ANALYZING, COMPLIANT
    
    # Store the entire intake form and result here
    data = Column(JSON, default={}) 
    
    created_at = Column(DateTime, default=datetime.utcnow)

class Component(Base):
    __tablename__ = "components"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    category = Column(String)
    part_number = Column(String)
    description = Column(String)
    price = Column(Float, nullable=True)
    metadata_info = Column(JSON, default={})
    
    # Vector embedding for semantic search (768 dimensions for Gemini 1.5/embedding-001)
    from pgvector.sqlalchemy import Vector
    embedding = Column(Vector(768))

class KnowledgeBase(Base):
    __tablename__ = "knowledge_base"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    source = Column(String) # NFPA 72, FBC, etc.
    section = Column(String)
    content = Column(String)
    
    from pgvector.sqlalchemy import Vector
    embedding = Column(Vector(768))

class AiAuditLog(Base):
    __tablename__ = "ai_audit_logs"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    workflow_id = Column(String, index=True) # Groups steps for a single request
    project_id = Column(String, nullable=True) # Optional link
    step_name = Column(String) # 'vision_analysis', 'rag_retrieval'
    input_data = Column(JSON, default={})
    output_data = Column(JSON, default={})
    model_name = Column(String, nullable=True)
    latency_ms = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
