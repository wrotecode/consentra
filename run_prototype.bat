@echo off
echo ====================================================
echo 🛡️  CONSENTRA - AI Image Protection Prototype
echo ====================================================
echo.
echo Starting both backend and frontend services...
echo.
echo Backend API will be available at: http://localhost:8000
echo Frontend will be available at: http://localhost:8080
echo.
echo Press Ctrl+C to stop both services
echo.
echo ====================================================
echo.

REM Start backend in background
start "Consentra Backend" cmd /c "cd Backend\consentra && python run_server.py"

REM Wait a moment for backend to start
timeout /t 3 /nobreak > nul

REM Start frontend in background
start "Consentra Frontend" cmd /c "cd Frontend\Consentra && npm run dev"

echo.
echo Services are starting up...
echo Check the console windows for any errors.
echo.
echo Once both services are running, open http://localhost:8080 in your browser
echo.
pause
