"""
FastAPI Router for Live Adaptive Agent - Pathway-Powered Temporal Intelligence

These endpoints expose the Live Adaptive Agent's capabilities:
- Live document ingestion
- Temporal analysis
- Auto-update detection
- Knowledge base management
"""

from fastapi import APIRouter, HTTPException, Depends, Body
from typing import Dict, List, Any, Optional
from pydantic import BaseModel, Field
from datetime import datetime
import logging

from ..services.live_adaptive_agent import get_live_agent, LiveAdaptiveMedicalAgent
from ..services.pathway_memory_service import get_pathway_memory, PathwayMemoryService
from ..database import get_db
from ..routers.auth import get_current_user

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/live-agent", tags=["Live Adaptive Agent"])


# ═══════════════════════════════════════════════════════════════════════════
# Request/Response Models
# ═══════════════════════════════════════════════════════════════════════════

class LiveAnalysisRequest(BaseModel):
    """Request for live adaptive analysis"""
    patient_id: int = Field(..., description="Patient identifier")
    document_type: str = Field(..., description="Document type (lab_report, prescription, etc.)")
    extracted_text: str = Field(..., description="OCR-extracted text content")
    detected_metrics: Optional[Dict[str, Any]] = Field(None, description="Parsed medical metrics")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Additional metadata")


class KnowledgeIngestionRequest(BaseModel):
    """Request to ingest medical knowledge"""
    document_type: str = Field(..., description="Type of knowledge (guideline, research, protocol)")
    title: str = Field(..., description="Document title")
    content: str = Field(..., description="Document content")
    source: str = Field(..., description="Source (WHO, NIH, etc.)")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Additional metadata")


class UpdateCheckRequest(BaseModel):
    """Request to check for live updates"""
    patient_id: int = Field(..., description="Patient identifier")
    since_timestamp: str = Field(..., description="ISO timestamp to compare against")


# ═══════════════════════════════════════════════════════════════════════════
# Endpoints
# ═══════════════════════════════════════════════════════════════════════════

@router.post("/analyze", response_model=Dict[str, Any])
async def analyze_with_temporal_context(
    request: LiveAnalysisRequest,
    current_user: dict = Depends(get_current_user)
):
    """
    🚀 CORE ENDPOINT: Analyze medical document with live temporal context
    
    This endpoint demonstrates the full power of live adaptive intelligence:
    1. Ingests document into Pathway live memory
    2. Retrieves patient's temporal context
    3. Performs temporal reasoning (what changed)
    4. Runs ML analysis (BioBERT, anomaly detection)
    5. Generates temporal insights with LLM
    6. Returns comprehensive analysis with temporal explanations
    
    Response includes:
    - Current analysis (entities, metrics, risk)
    - Temporal context (history, trends, deltas)
    - Temporal reasoning (what changed, why it matters)
    - LLM explanations (natural language insights)
    - Final recommendations (combining static + temporal)
    """
    try:
        live_agent = get_live_agent()
        if not live_agent:
            raise HTTPException(
                status_code=503,
                detail="Live Adaptive Agent not initialized. Please contact administrator."
            )
        
        logger.info(f"Live analysis requested by user {current_user.get('user_id')} for patient {request.patient_id}")
        
        # Run live adaptive analysis
        result = await live_agent.analyze_with_temporal_context(
            patient_id=request.patient_id,
            document_type=request.document_type,
            extracted_text=request.extracted_text,
            detected_metrics=request.detected_metrics,
            metadata=request.metadata or {}
        )
        
        return {
            "success": True,
            "message": "Live adaptive analysis completed successfully",
            "data": result
        }
    
    except Exception as e:
        logger.error(f"Live analysis error: {e}")
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")


@router.post("/check-updates", response_model=Dict[str, Any])
async def check_for_updates(
    request: UpdateCheckRequest,
    current_user: dict = Depends(get_current_user)
):
    """
    🔄 AUTO-UPDATE DETECTION: Check if new data arrived and auto-reanalyze
    
    This demonstrates LIVE ADAPTATION:
    - Checks Pathway memory for new documents since timestamp
    - If new data found, automatically triggers re-analysis
    - Returns updated insights without manual refresh
    
    This is a key post-transformer feature: the system actively monitors
    for changes and adapts without user intervention.
    """
    try:
        live_agent = get_live_agent()
        if not live_agent:
            raise HTTPException(
                status_code=503,
                detail="Live Adaptive Agent not initialized"
            )
        
        logger.info(f"Update check for patient {request.patient_id} since {request.since_timestamp}")
        
        # Check for updates and auto-reanalyze if found
        updated_analysis = await live_agent.detect_updates_and_reanalyze(
            patient_id=request.patient_id,
            since_timestamp=request.since_timestamp
        )
        
        if updated_analysis:
            return {
                "success": True,
                "has_updates": True,
                "message": "New data detected. Analysis automatically updated.",
                "data": updated_analysis
            }
        else:
            return {
                "success": True,
                "has_updates": False,
                "message": "No new data since specified timestamp",
                "data": None
            }
    
    except Exception as e:
        logger.error(f"Update check error: {e}")
        raise HTTPException(status_code=500, detail=f"Update check failed: {str(e)}")


@router.get("/patient/{patient_id}/temporal-context", response_model=Dict[str, Any])
async def get_patient_temporal_context(
    patient_id: int,
    lookback_days: int = 365,
    current_user: dict = Depends(get_current_user)
):
    """
    📊 TEMPORAL CONTEXT: Retrieve patient's temporal context from live memory
    
    Returns:
    - All documents in time window
    - Metric trends over time
    - Detected changes and deltas
    - Timeline of medical events
    
    This query hits Pathway's LIVE index, not a stale database.
    """
    try:
        pathway_memory = get_pathway_memory()
        if not pathway_memory:
            raise HTTPException(
                status_code=503,
                detail="Pathway memory not initialized"
            )
        
        logger.info(f"Temporal context request for patient {patient_id}")
        
        temporal_context = await pathway_memory.get_patient_temporal_context(
            patient_id=patient_id,
            lookback_days=lookback_days,
            include_deltas=True
        )
        
        return {
            "success": True,
            "data": temporal_context
        }
    
    except Exception as e:
        logger.error(f"Temporal context error: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to retrieve temporal context: {str(e)}")


@router.post("/knowledge/ingest", response_model=Dict[str, Any])
async def ingest_medical_knowledge(
    request: KnowledgeIngestionRequest,
    current_user: dict = Depends(get_current_user)
):
    """
    📚 KNOWLEDGE INGESTION: Add medical knowledge to live memory
    
    Examples of knowledge documents:
    - Clinical practice guidelines
    - Research paper summaries
    - Drug interaction databases
    - Treatment protocols
    
    Once ingested, the agent's reasoning automatically incorporates this knowledge.
    This demonstrates CONTINUOUS LEARNING without retraining.
    """
    try:
        pathway_memory = get_pathway_memory()
        if not pathway_memory:
            raise HTTPException(
                status_code=503,
                detail="Pathway memory not initialized"
            )
        
        logger.info(f"Knowledge ingestion: {request.title}")
        
        knowledge_id = await pathway_memory.ingest_knowledge_document(
            document_type=request.document_type,
            title=request.title,
            content=request.content,
            source=request.source,
            metadata=request.metadata
        )
        
        return {
            "success": True,
            "message": "Knowledge document ingested successfully",
            "data": {
                "knowledge_id": knowledge_id,
                "title": request.title,
                "timestamp": datetime.now().isoformat()
            }
        }
    
    except Exception as e:
        logger.error(f"Knowledge ingestion error: {e}")
        raise HTTPException(status_code=500, detail=f"Ingestion failed: {str(e)}")


@router.get("/knowledge/query", response_model=Dict[str, Any])
async def query_knowledge_base(
    query: str,
    document_types: Optional[str] = None,
    limit: int = 5,
    current_user: dict = Depends(get_current_user)
):
    """
    🔍 KNOWLEDGE QUERY: Search live medical knowledge base
    
    Returns relevant clinical guidelines, research, protocols.
    This is LIVE - new knowledge added 5 minutes ago is queryable now.
    """
    try:
        pathway_memory = get_pathway_memory()
        if not pathway_memory:
            raise HTTPException(
                status_code=503,
                detail="Pathway memory not initialized"
            )
        
        doc_types = document_types.split(',') if document_types else None
        
        results = await pathway_memory.query_knowledge_base(
            query=query,
            document_types=doc_types,
            limit=limit
        )
        
        return {
            "success": True,
            "query": query,
            "result_count": len(results),
            "data": results
        }
    
    except Exception as e:
        logger.error(f"Knowledge query error: {e}")
        raise HTTPException(status_code=500, detail=f"Query failed: {str(e)}")


@router.get("/status", response_model=Dict[str, Any])
async def get_live_agent_status(current_user: dict = Depends(get_current_user)):
    """
    ⚙️ AGENT STATUS: Get comprehensive status of live adaptive agent
    
    Returns:
    - Agent capabilities
    - Component status (Pathway, Temporal Engine, LLM, ML models)
    - Post-transformer features enabled
    - Memory statistics
    """
    try:
        live_agent = get_live_agent()
        pathway_memory = get_pathway_memory()
        
        if not live_agent:
            return {
                "success": False,
                "message": "Live Adaptive Agent not initialized",
                "status": "disabled"
            }
        
        agent_status = live_agent.get_agent_status()
        
        return {
            "success": True,
            "data": agent_status
        }
    
    except Exception as e:
        logger.error(f"Status check error: {e}")
        raise HTTPException(status_code=500, detail=f"Status check failed: {str(e)}")


@router.get("/health", response_model=Dict[str, Any])
async def health_check():
    """
    ❤️ HEALTH CHECK: Quick health check (no auth required)
    """
    live_agent = get_live_agent()
    pathway_memory = get_pathway_memory()
    
    return {
        "status": "operational",
        "timestamp": datetime.now().isoformat(),
        "components": {
            "live_agent": "initialized" if live_agent else "not_initialized",
            "pathway_memory": "initialized" if pathway_memory else "not_initialized"
        },
        "mode": "live_adaptive" if (live_agent and pathway_memory) else "static"
    }
