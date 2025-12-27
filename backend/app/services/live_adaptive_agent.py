"""
Live Adaptive Medical Agent - Post-Transformer Intelligence

This is the TRANSFORMED agent that demonstrates Track-1 "Agentic AI with Live Data" principles.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
ARCHITECTURAL TRANSFORMATION: From Stateless RAG to Live Cognitive Agent
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

BEFORE (Traditional RAG):
┌──────────────┐
│ User Query   │
└──────┬───────┘
       │
       v
┌──────────────┐     ┌─────────────┐
│  Vector DB   │────>│  LLM Reply  │
│  (Static)    │     │  (Stateless)│
└──────────────┘     └─────────────┘
   - No memory
   - No temporal awareness
   - One-shot analysis

AFTER (Live Adaptive Agent):
┌──────────────┐
│ User Query   │
└──────┬───────┘
       │
       v
┌──────────────────────────────────────────┐
│  LIVE MEDICAL INTELLIGENCE AGENT         │
│  ┌────────────────────────────────────┐  │
│  │ Step 1: Query Pathway Memory      │  │
│  │ ├─ Patient history (temporal)     │  │
│  │ ├─ Medical knowledge (live)       │  │
│  │ └─ Detect deltas since last time  │  │
│  └────────────────────────────────────┘  │
│  ┌────────────────────────────────────┐  │
│  │ Step 2: Temporal Reasoning        │  │
│  │ ├─ What changed?                  │  │
│  │ ├─ Risk progression?              │  │
│  │ └─ Trend analysis                 │  │
│  └────────────────────────────────────┘  │
│  ┌────────────────────────────────────┐  │
│  │ Step 3: Groq LLM Reasoning        │  │
│  │ ├─ Medical analysis               │  │
│  │ ├─ Context: Past + Present        │  │
│  │ └─ Explain temporal changes       │  │
│  └────────────────────────────────────┘  │
│  ┌────────────────────────────────────┐  │
│  │ Step 4: BioBERT + ML Models       │  │
│  │ ├─ Entity extraction              │  │
│  │ ├─ Anomaly detection              │  │
│  │ └─ Risk classification            │  │
│  └────────────────────────────────────┘  │
│  ┌────────────────────────────────────┐  │
│  │ Step 5: Generate Update           │  │
│  │ ├─ What changed and why           │  │
│  │ ├─ Confidence scores              │  │
│  │ └─ Temporal recommendations       │  │
│  └────────────────────────────────────┘  │
└──────────────────────────────────────────┘

KEY INNOVATIONS:
1. LIVE MEMORY: Pathway continuously indexes new documents
2. TEMPORAL COGNITION: Agent reasons over time, not just content
3. ADAPTIVE BEHAVIOR: Auto-updates when new data arrives
4. EXPLAINABLE: Explains what changed, when, and why

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""

import os
import logging
from typing import Dict, List, Any, Optional
from datetime import datetime
import json

# Import existing components
from .unified_ai_agent import UnifiedAIAgent

# Import new Pathway and temporal components
from .pathway_memory_service import PathwayMemoryService, get_pathway_memory
from .temporal_reasoning import TemporalReasoningEngine

# Import Groq for LLM reasoning
from groq import Groq

logger = logging.getLogger(__name__)


class LiveAdaptiveMedicalAgent:
    """
    Live Adaptive Medical Intelligence Agent
    
    This agent demonstrates post-transformer principles:
    - Continuous memory (Pathway)
    - Temporal reasoning (reasoning over time)
    - Live adaptation (auto-updates with new data)
    - Explainable insights (what changed, when, why)
    
    Architecture:
    - Pathway Memory Layer: Live document streaming + temporal query
    - Temporal Reasoning Engine: Change detection + trend analysis
    - Groq LLM: Medical reasoning + explanation generation
    - BioBERT + ML Models: Entity extraction + anomaly detection
    """
    
    def __init__(self,
                 pathway_memory: Optional[PathwayMemoryService] = None,
                 groq_api_key: Optional[str] = None):
        """
        Initialize Live Adaptive Agent
        
        Args:
            pathway_memory: Pathway memory service instance
            groq_api_key: Groq API key for LLM reasoning
        """
        # Core components
        self.pathway_memory = pathway_memory or get_pathway_memory()
        self.temporal_engine = TemporalReasoningEngine()
        self.base_agent = UnifiedAIAgent()  # Existing ML capabilities
        
        # Groq LLM for reasoning
        api_key = groq_api_key or os.getenv('GROQ_API_KEY', '')
        if api_key:
            self.groq_client = Groq(api_key=api_key)
            self.groq_model = "llama-3.3-70b-versatile"
            logger.info("Groq LLM initialized for temporal reasoning")
        else:
            self.groq_client = None
            logger.warning("Groq API key not set - LLM reasoning disabled")
        
        logger.info("Live Adaptive Medical Agent initialized")
    
    async def analyze_with_temporal_context(self,
                                           patient_id: int,
                                           document_type: str,
                                           extracted_text: str,
                                           detected_metrics: Optional[Dict[str, Any]] = None,
                                           metadata: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        MAIN AGENT FUNCTION - Analyze medical document with full temporal context
        
        This is the AGENTIC WORKFLOW that demonstrates live, adaptive intelligence:
        
        Step 1: Ingest document into Pathway live memory
        Step 2: Retrieve patient's temporal context (history + trends)
        Step 3: Perform temporal reasoning (what changed since last time)
        Step 4: Run base ML analysis (BioBERT, anomaly detection)
        Step 5: Cross-reference with live medical knowledge
        Step 6: Generate temporal insights with LLM reasoning
        Step 7: Return comprehensive analysis with "what changed and why"
        
        Args:
            patient_id: Unique patient identifier
            document_type: Type of document (lab_report, prescription, etc.)
            extracted_text: OCR-extracted text
            detected_metrics: Parsed medical metrics (glucose, BP, etc.)
            metadata: Additional metadata
        
        Returns:
            Comprehensive analysis with temporal context and live insights
        """
        
        logger.info(f"Starting live adaptive analysis for patient {patient_id}")
        
        # ═══════════════════════════════════════════════════════════════════════
        # STEP 1: Ingest into Pathway Live Memory
        # ═══════════════════════════════════════════════════════════════════════
        # This is NOT batch upload - Pathway detects this as a new event
        # and updates the temporal knowledge graph incrementally
        
        if self.pathway_memory:
            document_id = await self.pathway_memory.ingest_patient_document(
                patient_id=patient_id,
                document_type=document_type,
                extracted_text=extracted_text,
                metrics=detected_metrics,
                metadata=metadata
            )
            logger.info(f"Document ingested into Pathway memory: {document_id}")
        else:
            document_id = f"temp_{datetime.now().timestamp()}"
            logger.warning("Pathway memory not initialized - using temp ID")
        
        # ═══════════════════════════════════════════════════════════════════════
        # STEP 2: Retrieve Patient's Temporal Context
        # ═══════════════════════════════════════════════════════════════════════
        # Query Pathway for LIVE patient history
        # This includes all documents from the last 365 days, metric trends,
        # and detected changes
        
        temporal_context = {}
        historical_documents = []
        
        if self.pathway_memory:
            temporal_context = await self.pathway_memory.get_patient_temporal_context(
                patient_id=patient_id,
                lookback_days=365,
                include_deltas=True
            )
            historical_documents = temporal_context.get('documents', [])
            logger.info(f"Retrieved temporal context: {len(historical_documents)} historical documents")
        
        # ═══════════════════════════════════════════════════════════════════════
        # STEP 3: Temporal Reasoning - What Changed?
        # ═══════════════════════════════════════════════════════════════════════
        # Analyze CHANGES over time, not just current state
        # This is the key innovation that transforms static analysis into
        # continuous intelligence
        
        current_document = {
            'document_id': document_id,
            'patient_id': patient_id,
            'document_type': document_type,
            'timestamp': datetime.now().isoformat(),
            'content': extracted_text,
            'metrics': detected_metrics or {}
        }
        
        temporal_analysis = None
        if historical_documents:
            temporal_analysis = self.temporal_engine.analyze_temporal_context(
                current_document=current_document,
                historical_documents=historical_documents[:-1],  # Exclude current from history
                temporal_trends=temporal_context.get('metric_trends', {})
            )
            logger.info(f"Temporal analysis complete: {len(temporal_analysis.get('temporal_insights', []))} insights generated")
        
        # ═══════════════════════════════════════════════════════════════════════
        # STEP 4: Base ML Analysis (BioBERT, Anomaly Detection)
        # ═══════════════════════════════════════════════════════════════════════
        # Run existing ML models for entity extraction and anomaly detection
        
        base_analysis = self.base_agent.analyze_medical_report(
            report_text=extracted_text,
            lab_metrics=detected_metrics
        )
        logger.info("Base ML analysis complete")
        
        # ═══════════════════════════════════════════════════════════════════════
        # STEP 5: Cross-Reference with Live Medical Knowledge
        # ═══════════════════════════════════════════════════════════════════════
        # Query Pathway knowledge base for relevant clinical guidelines
        
        relevant_knowledge = []
        if self.pathway_memory and detected_metrics:
            # Query for relevant medical knowledge
            metric_names = list(detected_metrics.keys())
            for metric in metric_names[:3]:  # Top 3 metrics
                knowledge = await self.pathway_memory.query_knowledge_base(
                    query=metric,
                    limit=2
                )
                relevant_knowledge.extend(knowledge)
        
        # ═══════════════════════════════════════════════════════════════════════
        # STEP 6: LLM Temporal Reasoning
        # ═══════════════════════════════════════════════════════════════════════
        # Use Groq LLM to generate temporal insights and explanations
        
        llm_reasoning = None
        if self.groq_client and temporal_analysis:
            llm_reasoning = await self._generate_llm_temporal_reasoning(
                current_document=current_document,
                temporal_analysis=temporal_analysis,
                base_analysis=base_analysis,
                relevant_knowledge=relevant_knowledge
            )
            logger.info("LLM temporal reasoning generated")
        
        # ═══════════════════════════════════════════════════════════════════════
        # STEP 7: Compose Comprehensive Response
        # ═══════════════════════════════════════════════════════════════════════
        # Combine all analyses into a cohesive response that clearly shows:
        # - What was found (current state)
        # - What changed (temporal deltas)
        # - Why it changed (reasoning)
        # - What to do (recommendations)
        
        response = {
            # Core identification
            'document_id': document_id,
            'patient_id': patient_id,
            'analysis_timestamp': datetime.now().isoformat(),
            'agent_version': 'LiveAdaptive-v2.0',
            
            # Current analysis
            'current_analysis': {
                'document_type': document_type,
                'detected_metrics': detected_metrics or {},
                'entities_found': base_analysis.get('entities_found', []),
                'medications_detected': base_analysis.get('medications_detected', []),
                'lab_anomalies': base_analysis.get('lab_anomalies'),
                'risk_assessment': base_analysis.get('risk_assessment'),
                'base_recommendations': base_analysis.get('clinical_recommendations', [])
            },
            
            # Temporal context (THE KEY INNOVATION)
            'temporal_context': {
                'has_history': len(historical_documents) > 0,
                'historical_document_count': len(historical_documents),
                'lookback_period_days': 365,
                'timeline': temporal_context.get('timeline', []),
                'metric_trends': temporal_context.get('metric_trends', {}),
                'detected_deltas': temporal_context.get('deltas', {})
            },
            
            # Temporal reasoning (WHAT CHANGED)
            'temporal_reasoning': temporal_analysis if temporal_analysis else {
                'status': 'first_analysis',
                'message': 'This is the first analysis for this patient. No temporal comparison available.'
            },
            
            # LLM insights
            'llm_reasoning': llm_reasoning,
            
            # Medical knowledge context
            'relevant_knowledge': relevant_knowledge,
            
            # Final recommendations (combining static + temporal)
            'final_recommendations': self._generate_final_recommendations(
                base_analysis=base_analysis,
                temporal_analysis=temporal_analysis,
                llm_reasoning=llm_reasoning
            ),
            
            # Meta information
            'meta': {
                'pathway_enabled': self.pathway_memory is not None,
                'temporal_reasoning_enabled': temporal_analysis is not None,
                'llm_reasoning_enabled': llm_reasoning is not None,
                'analysis_mode': 'live_adaptive' if self.pathway_memory else 'static',
                'confidence_score': self._calculate_confidence(
                    base_analysis=base_analysis,
                    temporal_analysis=temporal_analysis,
                    llm_reasoning=llm_reasoning
                )
            }
        }
        
        logger.info(f"Live adaptive analysis complete for patient {patient_id}")
        
        return response
    
    async def _generate_llm_temporal_reasoning(self,
                                              current_document: Dict[str, Any],
                                              temporal_analysis: Dict[str, Any],
                                              base_analysis: Dict[str, Any],
                                              relevant_knowledge: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Use Groq LLM to generate temporal reasoning and explanations
        
        The LLM is prompted to:
        1. Explain what changed and why
        2. Assess risk progression
        3. Provide temporal recommendations
        4. Generate patient-friendly explanations
        """
        
        if not self.groq_client:
            return None
        
        try:
            # Build prompt for temporal reasoning
            prompt = self._build_temporal_reasoning_prompt(
                current_document=current_document,
                temporal_analysis=temporal_analysis,
                base_analysis=base_analysis,
                relevant_knowledge=relevant_knowledge
            )
            
            # Query Groq LLM
            response = self.groq_client.chat.completions.create(
                model=self.groq_model,
                messages=[
                    {
                        "role": "system",
                        "content": """You are an expert medical AI assistant specializing in TEMPORAL ANALYSIS.
                        
Your role is to explain how a patient's health has changed over time.

Focus on:
1. WHAT CHANGED: Specific metrics that increased/decreased
2. WHY IT MATTERS: Clinical significance of these changes
3. RISK PROGRESSION: Is the patient getting better or worse?
4. RECOMMENDATIONS: What should be done based on these temporal patterns

Always provide clear, evidence-based, temporal context in your explanations."""
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.7,
                max_tokens=1500
            )
            
            llm_output = response.choices[0].message.content
            
            return {
                'temporal_explanation': llm_output,
                'model_used': self.groq_model,
                'tokens_used': response.usage.total_tokens if hasattr(response, 'usage') else None,
                'generated_at': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"LLM temporal reasoning error: {e}")
            return None
    
    def _build_temporal_reasoning_prompt(self,
                                        current_document: Dict[str, Any],
                                        temporal_analysis: Dict[str, Any],
                                        base_analysis: Dict[str, Any],
                                        relevant_knowledge: List[Dict[str, Any]]) -> str:
        """Build prompt for LLM temporal reasoning"""
        
        # Extract key temporal information
        detected_changes = temporal_analysis.get('detected_changes', [])
        risk_progressions = temporal_analysis.get('risk_progressions', {})
        temporal_insights = temporal_analysis.get('temporal_insights', [])
        temporal_summary = temporal_analysis.get('temporal_summary', '')
        
        prompt = f"""TEMPORAL MEDICAL ANALYSIS REQUEST

CURRENT REPORT:
Document Type: {current_document.get('document_type')}
Timestamp: {current_document.get('timestamp')}
Metrics: {json.dumps(current_document.get('metrics', {}), indent=2)}

TEMPORAL ANALYSIS:
{temporal_summary}

DETECTED CHANGES:
{json.dumps(detected_changes, indent=2)}

RISK PROGRESSION:
Overall Trend: {risk_progressions.get('overall_trend', 'unknown')}
Metrics Worsened: {risk_progressions.get('worsened_count', 0)}
Metrics Improved: {risk_progressions.get('improved_count', 0)}

TEMPORAL INSIGHTS:
{json.dumps([{
    'title': i.get('title'),
    'description': i.get('description'),
    'temporal_context': i.get('temporal_context')
} for i in temporal_insights[:3]], indent=2)}

TASK:
Provide a clear, temporal explanation of this patient's health trajectory. Address:

1. What changed since the last assessment?
2. Are these changes concerning or encouraging?
3. What might be causing these changes?
4. What should the patient and doctor know?
5. What are the temporal recommendations?

Keep your response focused, evidence-based, and temporally contextualized."""
        
        return prompt
    
    def _generate_final_recommendations(self,
                                       base_analysis: Dict[str, Any],
                                       temporal_analysis: Optional[Dict[str, Any]],
                                       llm_reasoning: Optional[Dict[str, Any]]) -> List[str]:
        """Generate final recommendations combining all analyses"""
        
        recommendations = []
        
        # Priority 1: Temporal insights (if available)
        if temporal_analysis:
            temporal_insights = temporal_analysis.get('temporal_insights', [])
            for insight in temporal_insights[:3]:  # Top 3
                if insight.get('recommendation'):
                    recommendations.append(f"📈 {insight['recommendation']}")
        
        # Priority 2: Base clinical recommendations
        base_recs = base_analysis.get('clinical_recommendations', [])
        for rec in base_recs[:3]:
            if rec not in recommendations:
                recommendations.append(rec)
        
        # Priority 3: LLM-generated recommendations
        if llm_reasoning:
            # Extract recommendation from LLM response (simple parsing)
            llm_text = llm_reasoning.get('temporal_explanation', '')
            if 'recommend' in llm_text.lower():
                recommendations.append("🤖 See detailed LLM reasoning for additional context")
        
        # Always include temporal monitoring recommendation
        if temporal_analysis:
            recommendations.append("⏰ Continue temporal monitoring - next analysis will show further trends")
        
        return recommendations
    
    def _calculate_confidence(self,
                             base_analysis: Dict[str, Any],
                             temporal_analysis: Optional[Dict[str, Any]],
                             llm_reasoning: Optional[Dict[str, Any]]) -> float:
        """Calculate overall confidence score"""
        
        confidences = []
        
        # Base analysis confidence
        base_conf = base_analysis.get('confidence_score', 0.85)
        confidences.append(base_conf)
        
        # Temporal analysis confidence
        if temporal_analysis:
            temporal_insights = temporal_analysis.get('temporal_insights', [])
            if temporal_insights:
                avg_temporal_conf = sum(i.get('confidence', 0.8) for i in temporal_insights) / len(temporal_insights)
                confidences.append(avg_temporal_conf)
        
        # LLM reasoning adds confidence (structured reasoning)
        if llm_reasoning:
            confidences.append(0.9)
        
        return sum(confidences) / len(confidences) if confidences else 0.85
    
    async def detect_updates_and_reanalyze(self,
                                          patient_id: int,
                                          since_timestamp: str) -> Optional[Dict[str, Any]]:
        """
        Detect if new documents were added since timestamp and auto-reanalyze
        
        This demonstrates LIVE ADAPTATION:
        - Agent checks for new data
        - If found, automatically re-evaluates insights
        - Returns updated analysis without manual refresh
        
        Args:
            patient_id: Patient to check
            since_timestamp: ISO timestamp to compare against
        
        Returns:
            None if no updates, or updated analysis if new data found
        """
        
        if not self.pathway_memory:
            logger.warning("Pathway memory not initialized - cannot detect live updates")
            return None
        
        # Check for new documents
        update_check = await self.pathway_memory.detect_live_updates(
            patient_id=patient_id,
            since_timestamp=since_timestamp
        )
        
        if not update_check.get('requires_reanalysis'):
            logger.info(f"No new data for patient {patient_id} since {since_timestamp}")
            return None
        
        # New documents found - trigger re-analysis
        logger.info(f"New data detected for patient {patient_id}: {update_check['new_document_count']} documents")
        
        # Get the most recent document
        new_documents = update_check.get('new_documents', [])
        if not new_documents:
            return None
        
        latest_doc = sorted(new_documents, key=lambda x: x.get('timestamp', ''), reverse=True)[0]
        
        # Re-run analysis with new temporal context
        updated_analysis = await self.analyze_with_temporal_context(
            patient_id=patient_id,
            document_type=latest_doc.get('document_type'),
            extracted_text=latest_doc.get('content'),
            detected_metrics=latest_doc.get('metrics'),
            metadata={
                'auto_reanalysis': True,
                'trigger': 'live_update_detection',
                'new_document_count': update_check['new_document_count']
            }
        )
        
        # Add update metadata
        updated_analysis['update_info'] = {
            'was_auto_reanalyzed': True,
            'trigger_timestamp': since_timestamp,
            'new_documents_processed': update_check['new_document_count'],
            'reanalysis_timestamp': datetime.now().isoformat()
        }
        
        logger.info(f"Auto-reanalysis complete for patient {patient_id}")
        
        return updated_analysis
    
    def get_agent_status(self) -> Dict[str, Any]:
        """Get comprehensive agent status"""
        
        pathway_status = self.pathway_memory.get_service_status() if self.pathway_memory else {'status': 'disabled'}
        base_agent_status = self.base_agent.get_system_info()
        
        return {
            'agent_type': 'LiveAdaptiveMedicalAgent',
            'version': '2.0',
            'architecture': 'post_transformer_live_memory',
            'capabilities': [
                'live_document_streaming',
                'temporal_reasoning',
                'change_detection',
                'risk_progression_tracking',
                'auto_reanalysis',
                'llm_temporal_explanations',
                'biobert_entity_extraction',
                'anomaly_detection',
                'drug_interaction_checking',
                'knowledge_base_integration'
            ],
            'components': {
                'pathway_memory': pathway_status,
                'temporal_engine': {
                    'status': 'operational',
                    'capabilities': ['change_detection', 'trend_analysis', 'risk_progression']
                },
                'groq_llm': {
                    'status': 'operational' if self.groq_client else 'disabled',
                    'model': self.groq_model if self.groq_client else None
                },
                'base_ml_agent': base_agent_status
            },
            'post_transformer_features': {
                'continuous_memory': self.pathway_memory is not None,
                'temporal_cognition': True,
                'live_adaptation': self.pathway_memory is not None,
                'explainable_insights': self.groq_client is not None
            }
        }


# Global live agent instance
_live_agent: Optional[LiveAdaptiveMedicalAgent] = None


def initialize_live_agent(pathway_memory: Optional[PathwayMemoryService] = None,
                         groq_api_key: Optional[str] = None) -> LiveAdaptiveMedicalAgent:
    """Initialize global live adaptive agent"""
    global _live_agent
    
    _live_agent = LiveAdaptiveMedicalAgent(
        pathway_memory=pathway_memory,
        groq_api_key=groq_api_key
    )
    
    logger.info("Global Live Adaptive Agent initialized")
    return _live_agent


def get_live_agent() -> Optional[LiveAdaptiveMedicalAgent]:
    """Get global live adaptive agent instance"""
    return _live_agent
