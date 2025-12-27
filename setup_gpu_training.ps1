# GPU Training Setup Script for Infinite Helix
# Installs CUDA-enabled PyTorch and trains models with GPU acceleration

Write-Host "=" -ForegroundColor Cyan -NoNewline; Write-Host ("=" * 69) -ForegroundColor Cyan
Write-Host "🚀 INFINITE HELIX - GPU TRAINING SETUP" -ForegroundColor Green
Write-Host "=" -ForegroundColor Cyan -NoNewline; Write-Host ("=" * 69) -ForegroundColor Cyan
Write-Host ""

# Check if NVIDIA GPU is available
Write-Host "🔍 Checking for NVIDIA GPU..." -ForegroundColor Yellow
try {
    $gpuInfo = nvidia-smi --query-gpu=name,driver_version,memory.total --format=csv,noheader 2>$null
    if ($gpuInfo) {
        Write-Host "✅ NVIDIA GPU detected:" -ForegroundColor Green
        Write-Host "   $gpuInfo" -ForegroundColor Cyan
        $hasGPU = $true
    } else {
        Write-Host "⚠️  No NVIDIA GPU detected" -ForegroundColor Yellow
        $hasGPU = $false
    }
} catch {
    Write-Host "⚠️  nvidia-smi not found - no NVIDIA GPU or driver not installed" -ForegroundColor Yellow
    $hasGPU = $false
}

Write-Host ""

# Ask user if they want to install GPU version
if ($hasGPU) {
    $response = Read-Host "Do you want to install PyTorch with GPU support? (Y/n)"
    if ($response -eq "" -or $response -eq "Y" -or $response -eq "y") {
        Write-Host ""
        Write-Host "📦 Installing PyTorch with CUDA 11.8 support..." -ForegroundColor Yellow
        Write-Host "   This may take a few minutes..." -ForegroundColor Cyan
        Write-Host ""
        
        # Uninstall existing PyTorch
        pip uninstall -y torch torchvision torchaudio
        
        # Install CUDA-enabled PyTorch
        pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
        
        Write-Host ""
        Write-Host "✅ GPU-enabled PyTorch installed!" -ForegroundColor Green
        
        # Verify GPU availability
        Write-Host ""
        Write-Host "🔍 Verifying GPU availability..." -ForegroundColor Yellow
        python -c "import torch; print(f'✅ GPU Available: {torch.cuda.is_available()}'); print(f'GPU Name: {torch.cuda.get_device_name(0) if torch.cuda.is_available() else \"None\"}'); print(f'CUDA Version: {torch.version.cuda}')"
    }
} else {
    Write-Host "ℹ️  Installing CPU version of PyTorch..." -ForegroundColor Cyan
    pip install torch torchvision torchaudio
}

Write-Host ""
Write-Host "=" -ForegroundColor Cyan -NoNewline; Write-Host ("=" * 69) -ForegroundColor Cyan
Write-Host ""

# Install other required packages
Write-Host "📦 Installing additional packages..." -ForegroundColor Yellow
pip install datasets huggingface-hub dill xxhash multiprocess

Write-Host ""
Write-Host "=" -ForegroundColor Cyan -NoNewline; Write-Host ("=" * 69) -ForegroundColor Cyan
Write-Host ""

# Ask if user wants to train now
$trainNow = Read-Host "Do you want to train the models now? (Y/n)"
if ($trainNow -eq "" -or $trainNow -eq "Y" -or $trainNow -eq "y") {
    Write-Host ""
    Write-Host "🤖 Starting model training..." -ForegroundColor Green
    Write-Host ""
    
    # Change to backend directory and run training
    Set-Location "C:\infinite-helix\backend"
    python train_models.py
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host ""
        Write-Host "=" -ForegroundColor Cyan -NoNewline; Write-Host ("=" * 69) -ForegroundColor Cyan
        Write-Host "✅ TRAINING COMPLETE!" -ForegroundColor Green
        Write-Host "=" -ForegroundColor Cyan -NoNewline; Write-Host ("=" * 69) -ForegroundColor Cyan
        Write-Host ""
        Write-Host "📦 Models saved to: C:\infinite-helix\backend\models\" -ForegroundColor Cyan
        Write-Host ""
        Write-Host "🚀 Next steps:" -ForegroundColor Yellow
        Write-Host "   1. Start backend: python -m uvicorn app.main:app --reload --port 8000" -ForegroundColor White
        Write-Host "   2. Start frontend: cd ..\frontend; python -m http.server 3000" -ForegroundColor White
        Write-Host "   3. Open browser: http://localhost:3000" -ForegroundColor White
        Write-Host ""
    } else {
        Write-Host ""
        Write-Host "❌ Training failed. Check the error messages above." -ForegroundColor Red
        Write-Host ""
    }
} else {
    Write-Host ""
    Write-Host "✅ Setup complete!" -ForegroundColor Green
    Write-Host ""
    Write-Host "To train models later, run:" -ForegroundColor Yellow
    Write-Host "   cd C:\infinite-helix\backend" -ForegroundColor Cyan
    Write-Host "   python train_models.py" -ForegroundColor Cyan
    Write-Host ""
}

Write-Host "Press any key to exit..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
