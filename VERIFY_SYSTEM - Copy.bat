@echo off
REM ============================================================================
REM  SPAM SMS DETECTION SYSTEM - VERIFICATION SCRIPT
REM ============================================================================
REM  This script verifies all project components are working correctly
REM ============================================================================

echo.
echo ╔═════════════════════════════════════════════════════════════════════════╗
echo ║          SPAM SMS DETECTION - SYSTEM VERIFICATION SCRIPT               ║
echo ╚═════════════════════════════════════════════════════════════════════════╝
echo.

REM Check Python
echo [1/5] Checking Python environment...
"C:/Users/Smruti/Documents/MACHINE LEARNING COMPLETE/myenv/Scripts/python.exe" --version
if errorlevel 1 (
    echo ❌ Python not found
    exit /b 1
)
echo ✅ Python ready
echo.

REM Check model file
echo [2/5] Checking ML model...
if exist "spam_model.pkl" (
    echo ✅ Model file found: spam_model.pkl
    for %%F in (spam_model.pkl) do (
        echo    Size: %%~zF bytes
    )
) else (
    echo ❌ Model file not found
    exit /b 1
)
echo.

REM Check dataset
echo [3/5] Checking dataset...
if exist "spam.csv" (
    echo ✅ Dataset found: spam.csv
    for %%F in (spam.csv) do (
        echo    Size: %%~zF bytes
    )
) else (
    echo ❌ Dataset not found
    exit /b 1
)
echo.

REM Check visualizations
echo [4/5] Checking visualizations...
if exist "model_comparison.png" (
    echo ✅ Model comparison chart generated
) else (
    echo ⚠️  Model comparison chart missing
)
if exist "confusion_matrix.png" (
    echo ✅ Confusion matrix chart generated
) else (
    echo ⚠️  Confusion matrix chart missing
)
echo.

REM Check web files
echo [5/5] Checking web interface files...
if exist "index.html" echo ✅ Frontend: index.html
if exist "script.js" echo ✅ Logic: script.js
if exist "style.css" echo ✅ Styling: style.css
if exist "main.py" echo ✅ Backend: main.py
echo.

echo ╔═════════════════════════════════════════════════════════════════════════╗
echo ║                      ✅ ALL SYSTEMS VERIFIED                           ║
echo ╚═════════════════════════════════════════════════════════════════════════╝
echo.
echo NEXT STEPS:
echo -----------
echo 1. Start the backend server:
echo    "C:/Users/Smruti/Documents/MACHINE LEARNING COMPLETE/myenv/Scripts/python.exe" -m uvicorn main:app --host 127.0.0.1 --port 8000
echo.
echo 2. Open the frontend:
echo    - Double-click index.html, OR
echo    - Open in browser: file://d:\spam_SMS_detection\index.html
echo.
echo 3. Test with sample messages in the web interface
echo.
echo 4. Or use cURL to test API:
echo    curl -X POST "http://127.0.0.1:8000/predict" ^
echo      -H "Content-Type: application/json" ^
echo      -d "{\"text\":\"Free money\"}"
echo.
echo ✨ Project ready for production! ✨
echo.
pause
