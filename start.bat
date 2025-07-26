@echo off
echo Starting Mixtral Chat Application...
echo.

REM Check if Ollama is running
echo Checking Ollama status...
ollama list >nul 2>&1
if errorlevel 1 (
    echo Ollama is not running. Please start Ollama first.
    echo Run: ollama serve
    pause
    exit /b 1
)

REM Check if mixtral is available
ollama list | findstr /i "mixtral" >nul 2>&1
if errorlevel 1 (
    echo Mixtral model not found. Pulling mixtral...
    ollama pull mixtral
)

REM Set performance environment variables
set FLASK_ENV=development
set NUM_THREAD=8
set MAX_TOKENS=300
set NUM_CTX=2048

echo.
echo Starting Flask application...
echo Access the app at: http://localhost:5000
echo.
python app.py