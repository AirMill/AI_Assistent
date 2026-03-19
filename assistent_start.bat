@echo off
title AI Assistant - START

echo Starting AI Assistant...
cd /d %~dp0

echo.
echo Building and starting Docker containers...
docker compose up --build -d

echo.
echo ==============================
echo AI Assistant is starting...
echo Open in browser:
echo http://localhost:8000
echo ==============================

timeout /t 3 >nul

start http://localhost:8000

pause