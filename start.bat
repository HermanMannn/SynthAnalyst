@echo off
echo Starting SynthAnalyst...

:: Start FastAPI in a new window
start "FastAPI" cmd /k "cd /d %~dp0 && python app.py"

:: Start ngrok in a new window
start "ngrok" cmd /k "cd /d %~dp0 && ngrok http 5678"

echo Done! Both services are running.
echo FastAPI: http://localhost:8000
echo ngrok dashboard: http://127.0.0.1:4040
