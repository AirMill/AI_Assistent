@echo off
title AI Assistant - STOP

echo Stopping AI Assistant...
cd /d %~dp0

docker compose down

echo.
echo ==============================
echo AI Assistant stopped
echo ==============================

pause