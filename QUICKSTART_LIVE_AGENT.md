# 🚀 Quick Start Guide: Live Adaptive Agent

## Installation & Setup

### 1. Install Pathway (NEW)

```bash
cd backend
pip install pathway>=0.7.0
```

Or reinstall all dependencies:
```bash
pip install -r requirements.txt
```

### 2. Start the System

```bash
# The system will automatically:
# ✓ Initialize PostgreSQL
# ✓ Initialize Pathway live memory
# ✓ Initialize Live Adaptive Agent

uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

**Expected console output:**
```
🧬 LIVE ADAPTIVE MEDICAL INTELLIGENCE - PATHWAY ENABLED
✓ PostgreSQL database initialized (durable storage layer)
✓ Pathway Live Memory initialized (cognitive memory layer)
  - Patient docs: pathway_memory/patient_docs
  - Knowledge docs: pathway_memory/knowledge_docs
  - Streaming: enabled
✓ Live Adaptive Agent initialized
  - Temporal reasoning: enabled
  - LLM reasoning: enabled
  - BioBERT NER: enabled
  - Anomaly detection: enabled
POST-TRANSFORMER INTELLIGENCE: Continuous Memory • Temporal Reasoning • Live Adaptation
```

---

## 📡 API Endpoints (NEW)

### **Base URL**: `http://localhost:8000`

### **1. Live Analysis with Temporal Context**
```bash
POST /api/v1/live-agent/analyze

curl -X POST http://localhost:8000/api/v1/live-agent/analyze \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{
    "patient_id": 123,
    "document_type": "lab_report",
    "extracted_text": "Blood Glucose: 180 mg/dL, BP: 140/90",
    "detected_metrics": {
      "glucose_fasting": 180,
      "blood_pressure_systolic": 140,
      "blood_pressure_diastolic": 90
    }
  }'
```

**Response includes:**
- `current_analysis`: Static analysis (entities, metrics, risk)
- `temporal_context`: History, trends, deltas
- `temporal_reasoning`: What changed, risk progression
- `llm_reasoning`: Natural language explanations
- `final_recommendations`: Temporal + static recommendations

### **2. Check for Live Updates**
```bash
POST /api/v1/live-agent/check-updates

curl -X POST http://localhost:8000/api/v1/live-agent/check-updates \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{
    "patient_id": 123,
    "since_timestamp": "2024-12-20T10:00:00"
  }'
```

**If new data found:**
- Agent auto-reanalyzes
- Returns updated insights
- No manual refresh needed

### **3. Get Temporal Context**
```bash
GET /api/v1/live-agent/patient/{patient_id}/temporal-context?lookback_days=365

curl http://localhost:8000/api/v1/live-agent/patient/123/temporal-context \
  -H "Authorization: Bearer YOUR_TOKEN"
```

**Returns:**
- All documents in time window
- Metric trends
- Timeline of medical events
- Detected deltas

### **4. Ingest Medical Knowledge**
```bash
POST /api/v1/live-agent/knowledge/ingest

curl -X POST http://localhost:8000/api/v1/live-agent/knowledge/ingest \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{
    "document_type": "clinical_guideline",
    "title": "ADA Diabetes Guidelines 2024",
    "content": "Target HbA1c <7% for most adults...",
    "source": "American Diabetes Association"
  }'
```

### **5. Query Knowledge Base**
```bash
GET /api/v1/live-agent/knowledge/query?query=diabetes&limit=5

curl "http://localhost:8000/api/v1/live-agent/knowledge/query?query=diabetes&limit=5" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### **6. Agent Status**
```bash
GET /api/v1/live-agent/status

curl http://localhost:8000/api/v1/live-agent/status \
  -H "Authorization: Bearer YOUR_TOKEN"
```

**Returns:**
- Agent capabilities
- Component status (Pathway, Temporal Engine, LLM, ML)
- Post-transformer features enabled

### **7. Health Check (No Auth)**
```bash
GET /api/v1/live-agent/health

curl http://localhost:8000/api/v1/live-agent/health
```

---

## 🧪 Testing the Live Agent

### **Test 1: First Analysis**
```python
import httpx

# First report for patient 123
response = httpx.post(
    "http://localhost:8000/api/v1/live-agent/analyze",
    json={
        "patient_id": 123,
        "document_type": "lab_report",
        "extracted_text": "Glucose: 165 mg/dL",
        "detected_metrics": {"glucose_fasting": 165}
    },
    headers={"Authorization": "Bearer YOUR_TOKEN"}
)

print(response.json())
# temporal_reasoning: "This is the first analysis for this patient"
```

### **Test 2: Follow-up (Shows Temporal Power)**
```python
# One month later, new report
response = httpx.post(
    "http://localhost:8000/api/v1/live-agent/analyze",
    json={
        "patient_id": 123,
        "document_type": "lab_report",
        "extracted_text": "Glucose: 180 mg/dL",
        "detected_metrics": {"glucose_fasting": 180}
    },
    headers={"Authorization": "Bearer YOUR_TOKEN"}
)

result = response.json()

# NOW you'll see:
# - detected_changes: [{"metric": "glucose_fasting", "change": +15}]
# - temporal_reasoning: "Glucose increased +15 since last month"
# - llm_reasoning: "Your glucose shows an upward trend..."
```

### **Test 3: Auto-Update Detection**
```python
import time

# Upload first document
httpx.post("http://localhost:8000/api/v1/live-agent/analyze", ...)

# Save timestamp
check_timestamp = "2024-12-25T10:00:00"

# Wait a bit, then upload another document
time.sleep(5)
httpx.post("http://localhost:8000/api/v1/live-agent/analyze", ...)

# Check for updates
response = httpx.post(
    "http://localhost:8000/api/v1/live-agent/check-updates",
    json={
        "patient_id": 123,
        "since_timestamp": check_timestamp
    },
    headers={"Authorization": "Bearer YOUR_TOKEN"}
)

# Agent auto-detected new document and re-analyzed!
print(response.json()["has_updates"])  # True
```

---

## 📂 Directory Structure

After starting the system, you'll see:

```
backend/
├── pathway_memory/           🆕 CREATED AUTOMATICALLY
│   ├── patient_docs/         🆕 Patient medical documents (JSON)
│   │   └── doc_123_*.json
│   ├── knowledge_docs/       🆕 Medical knowledge (JSON)
│   │   └── know_*.json
│   └── index/                🆕 Pathway index persistence
│
├── app/
│   ├── services/
│   │   ├── pathway_memory_service.py     🆕 Live memory layer
│   │   ├── temporal_reasoning.py          🆕 Temporal cognition
│   │   ├── live_adaptive_agent.py         🆕 Main agent
│   │   └── ...
│   └── routers/
│       ├── live_agent.py                  🆕 API endpoints
│       └── ...
```

---

## 🔍 Verify Installation

### **Check Pathway Memory Status**
```bash
curl http://localhost:8000/api/v1/live-agent/status \
  -H "Authorization: Bearer YOUR_TOKEN"
```

**Expected response:**
```json
{
  "success": true,
  "data": {
    "agent_type": "LiveAdaptiveMedicalAgent",
    "version": "2.0",
    "architecture": "post_transformer_live_memory",
    "capabilities": [
      "live_document_streaming",
      "temporal_reasoning",
      "change_detection",
      "risk_progression_tracking",
      "auto_reanalysis",
      "llm_temporal_explanations"
    ],
    "components": {
      "pathway_memory": {
        "status": "operational",
        "streaming_enabled": true,
        "patient_documents": 0,
        "knowledge_documents": 0
      },
      "temporal_engine": {
        "status": "operational"
      },
      "groq_llm": {
        "status": "operational",
        "model": "llama-3.3-70b-versatile"
      }
    },
    "post_transformer_features": {
      "continuous_memory": true,
      "temporal_cognition": true,
      "live_adaptation": true,
      "explainable_insights": true
    }
  }
}
```

---

## 🎯 Key Differences from Old System

| Feature | Old System | New System (Live Agent) |
|---------|-----------|------------------------|
| **Endpoint** | `/api/v1/unified-ai/analyze` | `/api/v1/live-agent/analyze` |
| **Response** | Static analysis only | Static + Temporal context |
| **Memory** | None (stateless) | Pathway (continuous) |
| **Temporal** | No | Full temporal reasoning |
| **Updates** | Manual | Auto-detect & re-analyze |
| **Explanations** | Basic | LLM-powered temporal insights |

---

## 💡 Pro Tips

1. **First Analysis**: Always returns "no history" - this is expected
2. **Second Analysis**: NOW you see temporal power (what changed)
3. **Knowledge Base**: Add guidelines ONCE, agent uses them forever
4. **Auto-Updates**: System actively monitors for changes
5. **Streaming**: Documents added to `pathway_memory/` are auto-detected

---

## ⚠️ Troubleshooting

### **Pathway not initializing**
```bash
# Check if Pathway installed
pip show pathway

# Reinstall if needed
pip install pathway>=0.7.0
```

### **No temporal context**
- First analysis will show "first_analysis" status
- Upload 2+ documents to see temporal reasoning

### **LLM reasoning disabled**
- Check `GROQ_API_KEY` in `.env`
- Agent works without LLM (just no natural language explanations)

---

## 📚 Additional Resources

- **Architecture Documentation**: `LIVE_ARCHITECTURE.md`
- **API Documentation**: http://localhost:8000/docs
- **Pathway Docs**: https://pathway.com/developers

---

**You're ready to demonstrate Track-1 "Agentic AI with Live Data"!** 🚀
