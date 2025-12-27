@echo off
echo ======================================================================
echo 🚀 INFINITE HELIX - GPU TRAINING SETUP
echo ======================================================================
echo.

REM Check for NVIDIA GPU
echo 🔍 Checking for NVIDIA GPU...
nvidia-smi --query-gpu=name --format=csv,noheader >nul 2>&1
if %errorlevel% == 0 (
    echo ✅ NVIDIA GPU detected!
    nvidia-smi --query-gpu=name,memory.total --format=csv,noheader
    set HAS_GPU=1
) else (
    echo ⚠️  No NVIDIA GPU detected - will use CPU
    set HAS_GPU=0
)
echo.

REM Ask about GPU installation
if %HAS_GPU%==1 (
    set /p GPU_INSTALL="Install PyTorch with GPU support? (Y/n): "
    if /i "%GPU_INSTALL%"=="n" goto CPU_INSTALL
    
    echo.
    echo 📦 Installing PyTorch with CUDA 11.8...
    pip uninstall -y torch torchvision torchaudio
    pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
    
    echo.
    echo 🔍 Verifying GPU...
    python -c "import torch; print('GPU Available:', torch.cuda.is_available()); print('GPU Name:', torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'None')"
    goto INSTALL_DEPS
)

:CPU_INSTALL
echo.
echo 📦 Installing CPU version of PyTorch...
pip install torch torchvision torchaudio

:INSTALL_DEPS
echo.
echo 📦 Installing additional packages...
pip install datasets huggingface-hub dill xxhash multiprocess

echo.
echo ======================================================================
echo.

REM Ask about training
set /p TRAIN_NOW="Train models now? (Y/n): "
if /i "%TRAIN_NOW%"=="n" goto END

echo.
echo 🤖 Starting model training...
echo.
cd C:\infinite-helix\backend
python train_models.py

if %errorlevel% == 0 (
    echo.
    echo ======================================================================
    echo ✅ TRAINING COMPLETE!
    echo ======================================================================
    echo.
    echo 📦 Models saved to: C:\infinite-helix\backend\models\
    echo.
    echo 🚀 Next steps:
    echo    1. Start backend: python -m uvicorn app.main:app --reload --port 8000
    echo    2. Start frontend: cd ..\frontend ^&^& python -m http.server 3000
    echo    3. Open browser: http://localhost:3000
    echo.
) else (
    echo.
    echo ❌ Training failed. Check error messages above.
    echo.
)
goto END

:END
echo.
echo To train later: cd C:\infinite-helix\backend ^&^& python train_models.py
echo.
pause
