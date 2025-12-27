# 🚀 Quick Setup Guide - Groq AI Integration

## Get Started in 3 Minutes!

### Step 1: Get FREE Groq API Key (30 seconds)

1. Go to: **https://console.groq.com/**
2. Click "Sign Up" (Google/GitHub OAuth available)
3. Navigate to "API Keys" in dashboard
4. Click "Create API Key"
5. Copy your key (starts with `gsk_...`)

### Step 2: Add API Key to Configuration (10 seconds)

Open `backend/.env` and add:

```bash
# Groq API Configuration
GROQ_API_KEY=gsk_paste_your_key_here
```

### Step 3: Start the Application (1 minute)

```bash
# Terminal 1 - Backend
cd C:\infinite-helix\backend
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Terminal 2 - Frontend
cd C:\infinite-helix\frontend
python -m http.server 3000
```

### Step 4: Test It! (1 minute)

1. Open browser: **http://localhost:3000**
2. Upload a medical report (PDF/image)
3. Watch the AI analyze it in real-time!

## ✅ What You Get

### Before Groq (Traditional Analysis)
```
✓ OCR text extraction
✓ Basic entity recognition
✓ Medical metric detection
✓ Simple insights (3-5 items)
⏱️ Processing time: 8-10 seconds
```

### After Groq (AI-Powered Analysis)
```
✓ Everything above PLUS:
✓ AI-generated medical summary
✓ Intelligent risk assessment
✓ Clinical reasoning & observations
✓ Personalized recommendations
✓ Follow-up care planning
✓ Patient education (easy-to-understand)
✓ Red flag detection (critical warnings)
✓ Priority-based insight sorting
⏱️ Processing time: 8-12 seconds (only +2s!)
```

## 📊 Example Output Comparison

### Traditional Output:
```
Insights: 3 items
- Overall Health Status: Good
- Blood Pressure: Normal
- Continue healthy lifestyle
```

### With Groq AI:
```
Insights: 12+ items (intelligently prioritized)

🤖 AI Medical Summary:
"Patient shows well-controlled blood pressure (118/78 mmHg) and normal 
fasting glucose (92 mg/dL). Current medication regimen appears effective. 
Continue current management with routine monitoring recommended."

⚠️ Risk Assessment:
- No significant immediate risks identified (Risk Level: Low)
- Long-term cardiovascular health: Good
- Diabetes risk: Low

💡 Clinical Insights:
1. Blood pressure within optimal range suggests good medication adherence
2. Glucose levels indicate effective metabolic control
3. No concerning trends in recent measurements

📋 Recommendations:
✓ High Priority:
  - Continue current medications as prescribed
  - Monitor BP weekly at home
  
✓ Medium Priority:
  - Maintain healthy diet and exercise routine
  - Schedule 3-month follow-up appointment
  
✓ Lifestyle:
  - Keep sodium intake <2g/day
  - Exercise 30 minutes daily, 5 days/week

📅 Follow-Up Plan:
- Next visit: 3 months
- Tests needed: Lipid panel, HbA1c
- Monitoring: Weekly BP, monthly weight
- Track: Blood pressure, medication adherence

📚 Patient Education:
• Your blood pressure is in a healthy range, which is great!
• Normal glucose levels show your body is processing sugar well
• Keep taking your medicines exactly as prescribed
• Regular monitoring helps catch problems early
```

## 🎯 Use Cases

### 1. Diabetes Management
**Upload**: Lab report with glucose readings  
**Get**: Detailed diabetes risk assessment, HbA1c interpretation, dietary recommendations, monitoring schedule

### 2. Hypertension Monitoring
**Upload**: BP measurement report  
**Get**: Cardiovascular risk analysis, medication effectiveness evaluation, lifestyle modification advice

### 3. General Health Checkup
**Upload**: Complete metabolic panel  
**Get**: Comprehensive health summary, organ function assessment, preventive care recommendations

### 4. Medication Review
**Upload**: Prescription list or discharge summary  
**Get**: Drug classification, interaction warnings, dosage verification, compliance tips

## 🔧 Troubleshooting

### "Groq agent not available" in logs

**Fix**: Check API key in `.env` file
```bash
# Verify it starts with 'gsk_'
cat backend/.env | grep GROQ_API_KEY
```

### API key not working

**Fix**: Make sure you copied the entire key
- Should look like: `gsk_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`
- No spaces or quotes around it
- Check for accidental line breaks

### Groq analysis skipped

**Fix**: Restart backend server after adding API key
```bash
cd C:\infinite-helix\backend
# Kill existing server (Ctrl+C)
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## 💰 Cost

**Groq Free Tier:**
- ✅ 30 requests/minute
- ✅ 6,000 requests/day
- ✅ All models included
- ✅ Cost: $0 (completely FREE!)

**Average Report Analysis:**
- Uses ~2,000 tokens
- Takes ~1-2 seconds
- Costs: $0.00

**You can analyze 100+ reports per day on the free tier!**

## 🚨 Important Notes

### Without Groq API Key
- System works normally
- Uses traditional ML analysis only
- Basic insights (3-5 items)
- No AI reasoning or summaries

### With Groq API Key
- Full AI-powered analysis
- Advanced insights (10-15+ items)
- Medical reasoning & explanations
- Priority-based recommendations
- **Highly recommended!**

## 📖 Documentation

- **Full Groq Guide**: See `GROQ_SETUP.md`
- **ML Features**: See `ML_FEATURES.md`
- **API Documentation**: http://localhost:8000/docs (after starting server)

## 🆘 Need Help?

### Check Logs
```bash
# Backend logs
tail -f backend/logs/app.log

# Look for:
"Groq Agent Service initialized successfully" ✓
"Starting Groq AI agent analysis" ✓
"Groq AI analysis completed" ✓
```

### Test API Key Manually
```bash
curl -H "Authorization: Bearer YOUR_API_KEY" \
  https://api.groq.com/openai/v1/models
```

### Common Issues
1. **No insights**: Check API key is set correctly
2. **Slow responses**: Check internet connection
3. **Rate limit**: Wait 60 seconds, then try again
4. **JSON errors**: Groq handles this automatically

## 🎉 You're All Set!

Your Infinite Helix installation is now powered by:
- ⚡ Groq's ultra-fast LLM inference
- 🧠 BioBERT medical entity extraction
- 🔬 PyTorch deep learning models
- 📊 Advanced medical analysis

**Start analyzing medical reports with AI superpowers!** 🚀

---

**Questions?** Check `GROQ_SETUP.md` for detailed documentation.  
**Issues?** See logs in `backend/logs/app.log`
