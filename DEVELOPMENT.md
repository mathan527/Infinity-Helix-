# Infinite Helix Development Guide

## Quick Start

### Prerequisites
1. **Python 3.9+** - [Download](https://www.python.org/downloads/)
2. **Tesseract OCR** - Installation instructions below
3. **Neon PostgreSQL** - Free tier available at [neon.tech](https://neon.tech/)

### Installation Steps

#### 1. Install Tesseract OCR

**Windows:**
```powershell
# Using Chocolatey
choco install tesseract

# Or download installer from:
# https://github.com/UB-Mannheim/tesseract/wiki
```

**macOS:**
```bash
brew install tesseract
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt-get update
sudo apt-get install tesseract-ocr
```

#### 2. Set Up Neon PostgreSQL Database

1. Go to [neon.tech](https://neon.tech/) and create a free account
2. Create a new project
3. Copy your connection string (looks like: `postgresql://user:pass@host/db`)
4. Save this for the `.env` file

#### 3. Configure Environment

1. Copy `.env.example` to `.env` in the `backend` directory
2. Update `DATABASE_URL` with your Neon PostgreSQL connection string
3. Update `TESSERACT_PATH` if tesseract is not in your PATH:
   - Windows: `C:/Program Files/Tesseract-OCR/tesseract.exe`
   - macOS: `/usr/local/bin/tesseract`
   - Linux: `/usr/bin/tesseract`

#### 4. Run Setup Script

**Windows:**
```powershell
.\run.ps1
```

**macOS/Linux:**
```bash
chmod +x run.sh
./run.sh
```

#### 5. Serve Frontend

Open a new terminal:

```bash
cd frontend
python -m http.server 3000
```

Or use any static file server:
```bash
# Using Node.js
npx http-server -p 3000

# Using Python 3
python -m http.server 3000
```

#### 6. Access Application

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

## Manual Setup (Alternative)

### Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Download spaCy model
python -m spacy download en_core_web_md

# Run server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend Setup

```bash
cd frontend

# Serve with Python
python -m http.server 3000

# Or with Node.js
npx http-server -p 3000
```

## Development

### Project Structure
```
infinite-helix/
├── backend/
│   ├── app/
│   │   ├── main.py              # FastAPI application
│   │   ├── config.py            # Configuration
│   │   ├── database.py          # Database setup
│   │   ├── models.py            # SQLAlchemy models
│   │   ├── schemas.py           # Pydantic schemas
│   │   ├── routers/             # API endpoints
│   │   ├── services/            # Business logic
│   │   └── utils/               # Utilities
│   ├── uploads/                 # Uploaded files
│   ├── requirements.txt
│   └── .env
└── frontend/
    ├── index.html
    ├── css/
    └── js/
```

### Testing the API

Using the interactive docs:
```
http://localhost:8000/docs
```

Using curl:
```bash
# Health check
curl http://localhost:8000/health

# Upload file
curl -X POST -F "file=@test.pdf" http://localhost:8000/api/v1/upload

# Analyze file
curl -X POST http://localhost:8000/api/v1/analyze/{file_id}

# Get results
curl http://localhost:8000/api/v1/results/{analysis_id}
```

### Database Management

View tables:
```python
python
>>> from app.database import engine
>>> from app.models import Base
>>> Base.metadata.tables.keys()
```

Reset database:
```python
from app.database import engine
from app.models import Base
Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)
```

## Troubleshooting

### Common Issues

**1. Tesseract not found**
```
Error: tesseract is not installed or it's not in your PATH
```
Solution: Install Tesseract and update `TESSERACT_PATH` in `.env`

**2. Database connection failed**
```
Error: could not connect to server
```
Solution: Check `DATABASE_URL` in `.env` and ensure Neon database is accessible

**3. spaCy model not found**
```
OSError: [E050] Can't find model 'en_core_web_md'
```
Solution: Run `python -m spacy download en_core_web_md`

**4. Port already in use**
```
Error: [Errno 48] Address already in use
```
Solution: Change port in `.env` or kill the process using the port

**5. CORS errors in browser**
```
Access to fetch has been blocked by CORS policy
```
Solution: Add your frontend URL to `ALLOWED_ORIGINS` in `.env`

## Production Deployment

### Environment Variables

Update these for production:
```env
DEBUG=False
ENVIRONMENT=production
SECRET_KEY=<generate-strong-key>
ALLOWED_ORIGINS=https://yourdomain.com
```

### Security Checklist

- [ ] Use strong `SECRET_KEY`
- [ ] Set `DEBUG=False`
- [ ] Use HTTPS
- [ ] Configure proper CORS origins
- [ ] Set up rate limiting
- [ ] Enable database SSL
- [ ] Regular security updates
- [ ] Implement authentication (future)

### Deployment Options

**Backend:**
- Railway
- Render
- Heroku
- AWS Elastic Beanstalk
- Google Cloud Run

**Frontend:**
- Vercel
- Netlify
- GitHub Pages
- AWS S3 + CloudFront

**Database:**
- Neon (PostgreSQL)
- Supabase
- AWS RDS

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## License

MIT License - See LICENSE file

## Support

For issues and questions:
- GitHub Issues
- Email: support@infinitehelix.com
