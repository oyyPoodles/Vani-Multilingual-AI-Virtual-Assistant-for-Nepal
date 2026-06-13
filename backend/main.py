"""
VANI — FastAPI Backend Server
Main application entry point with all API routes.
"""

import os
import logging
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
from datetime import date

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="VANI API",
    description="Voice Assistant for Nepal Intelligence — Backend API",
    version="1.0.0"
)

# CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ═══════════════════════════════════════════
# Database Connection (PostgreSQL)
# ═══════════════════════════════════════════

DB_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/vani")
db_connection = None  # Set up with psycopg2 or asyncpg in production


# ═══════════════════════════════════════════
# Request/Response Models
# ═══════════════════════════════════════════

class ChatRequest(BaseModel):
    text: str
    language: str = "auto"
    session_id: Optional[str] = None

class ChatResponse(BaseModel):
    text: str
    intent: Optional[str] = None
    confidence: Optional[float] = None
    language: Optional[str] = None
    data: Optional[dict] = None

class InvoiceCreateRequest(BaseModel):
    customer_id: int
    amount: float

class VoiceRequest(BaseModel):
    audio_base64: str
    language: str = "auto"


# ═══════════════════════════════════════════
# Core Chat Endpoint
# ═══════════════════════════════════════════

@app.post("/api/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """Main VANI chat endpoint — processes text and returns AI response."""
    try:
        from ai.asr.language_detect import detect_language
        from ai.nlp.intent_classifier import IntentClassifier
        from ai.nlp.entity_extractor import EntityExtractor
        from ai.agents.master_agent import MasterAgent

        # 1. Detect language
        lang_result = detect_language(request.text)

        # 2. Classify intent
        classifier = IntentClassifier()
        intent_result = classifier.classify(request.text)

        # 3. Extract entities
        extractor = EntityExtractor()
        entities = extractor.extract(request.text)

        # 4. Route to agent
        agent = MasterAgent(db_connection=db_connection)
        response = agent.route(intent_result["intent"], entities)

        return ChatResponse(
            text=response["text"],
            intent=intent_result["intent"],
            confidence=intent_result["confidence"],
            language=lang_result["language"],
            data=response.get("data")
        )
    except Exception as e:
        logger.error(f"Chat error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ═══════════════════════════════════════════
# Sales Endpoints
# ═══════════════════════════════════════════

@app.get("/sales")
async def get_sales(date: Optional[str] = Query("today"), limit: int = Query(100)):
    """Get sales data."""
    return {"endpoint": "sales", "date_filter": date, "message": "Sales endpoint ready. Connect PostgreSQL for live data."}


# ═══════════════════════════════════════════
# Customer Endpoints
# ═══════════════════════════════════════════

@app.get("/customers")
async def get_customers(name: Optional[str] = None, limit: int = Query(50)):
    """Search/list customers."""
    return {"endpoint": "customers", "search": name, "message": "Customer endpoint ready."}


# ═══════════════════════════════════════════
# Invoice Endpoints
# ═══════════════════════════════════════════

@app.post("/invoices/create")
async def create_invoice(request: InvoiceCreateRequest):
    """Create a new invoice."""
    tax = round(request.amount * 0.13, 2)
    total = round(request.amount + tax, 2)
    return {"customer_id": request.customer_id, "amount": request.amount, "tax": tax, "total": total, "status": "pending"}

@app.get("/invoices")
async def get_invoices(status: Optional[str] = None):
    return {"endpoint": "invoices", "filter": status, "message": "Invoice endpoint ready."}


# ═══════════════════════════════════════════
# Inventory Endpoints
# ═══════════════════════════════════════════

@app.get("/inventory")
async def get_inventory(product: Optional[str] = None, category: Optional[str] = None):
    return {"endpoint": "inventory", "product": product, "category": category, "message": "Inventory endpoint ready."}


# ═══════════════════════════════════════════
# Attendance Endpoints
# ═══════════════════════════════════════════

@app.get("/attendance")
async def get_attendance(date: Optional[str] = Query("today")):
    return {"endpoint": "attendance", "date": date, "message": "Attendance endpoint ready."}


# ═══════════════════════════════════════════
# Reports Endpoints
# ═══════════════════════════════════════════

@app.get("/reports")
async def get_reports(type: str = Query("monthly")):
    return {"endpoint": "reports", "type": type, "message": "Reports endpoint ready."}


# ═══════════════════════════════════════════
# Health Check
# ═══════════════════════════════════════════

@app.get("/health")
async def health():
    return {"status": "healthy", "service": "VANI API", "version": "1.0.0"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
