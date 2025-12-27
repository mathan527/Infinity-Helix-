# Infinite Helix - Setup and Run Script
# This script helps you set up and run the application

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Infinite Helix - Setup & Run Script" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check Python installation
Write-Host "Checking Python installation..." -ForegroundColor Yellow
python --version
if ($LASTEXITCODE -ne 0) {
    Write-Host "Error: Python is not installed or not in PATH" -ForegroundColor Red
    exit 1
}

# Navigate to backend directory
Set-Location -Path "$PSScriptRoot\backend"

# Check .env file
if (-Not (Test-Path ".env")) {
    Write-Host "`nWarning: .env file not found!" -ForegroundColor Yellow
    Write-Host "Creating .env from template..." -ForegroundColor Yellow
    Copy-Item ".env.example" ".env"
    Write-Host ""
    Write-Host "IMPORTANT: Please edit backend/.env and add your Neon PostgreSQL connection string" -ForegroundColor Red
    Write-Host "Get your connection string from: https://neon.tech/" -ForegroundColor Cyan
    Write-Host ""
    $continue = Read-Host "Press Enter to continue after updating .env, or type 'exit' to quit"
    if ($continue -eq 'exit') {
        exit 0
    }
}

# Create necessary directories
if (-Not (Test-Path "uploads")) {
    New-Item -ItemType Directory -Path "uploads" | Out-Null
}

if (-Not (Test-Path "logs")) {
    New-Item -ItemType Directory -Path "logs" | Out-Null
}

# Initialize database
Write-Host "`nInitializing database..." -ForegroundColor Yellow
Write-Host "Database will be initialized on first run" -ForegroundColor Gray

# Start the server
Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "  Starting Infinite Helix Server" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Backend API: http://localhost:8000" -ForegroundColor Green
Write-Host "API Documentation: http://localhost:8000/docs" -ForegroundColor Green
Write-Host ""
Write-Host "To serve the frontend, open a new terminal and run:" -ForegroundColor Yellow
Write-Host "  cd frontend" -ForegroundColor Gray
Write-Host "  python -m http.server 3000" -ForegroundColor Gray
Write-Host ""
Write-Host "Then open: http://localhost:3000" -ForegroundColor Green
Write-Host ""
Write-Host "Press Ctrl+C to stop the server" -ForegroundColor Yellow
Write-Host ""

# Run the server
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
