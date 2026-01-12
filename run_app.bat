@echo off
TITLE GPT App Runner (Auto-VENV)
CLS

echo ======================================================
echo 1. Setting up Virtual Environment...
echo ======================================================

:: چک میکند اگر پوشه venv نیست، آن را میسازد
if not exist venv (
    echo [INFO] Virtual environment not found. Creating one...
    python -m venv venv
    echo [INFO] venv created successfully.
)

:: فعال کردن محیط مجازی
call venv\Scripts\activate

echo ======================================================
echo 2. Checking Dependencies...
echo ======================================================
:: نصب کتابخانه‌ها داخل محیط مجازی
pip install -r requirements.txt >nul 2>&1
pip install -e . >nul 2>&1

echo.
echo ======================================================
echo 3. Launching Application...
echo ======================================================

:: بستن برنامه‌های باز مانده قبلی
taskkill /F /IM uvicorn.exe >nul 2>&1
taskkill /F /IM streamlit.exe >nul 2>&1

echo Starting Backend API...
start "GPT Backend" cmd /k "venv\Scripts\activate && uvicorn backend.api:app --reload --port 8000"

echo Waiting for backend (5 seconds)...
timeout /t 5 >nul

echo Starting Frontend UI...
start "GPT Frontend" cmd /k "venv\Scripts\activate && streamlit run frontend/app.py"

echo.
echo ======================================================
echo System is Running inside Virtual Environment!
echo Backend: http://127.0.0.1:8000
echo Frontend: http://localhost:8501
echo ======================================================
pause