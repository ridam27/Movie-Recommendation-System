@echo off
title Movie Recommendation Engine

echo Starting Backend...
start cmd /k "cd backend && python -m uvicorn app:app --reload"

timeout /t 3 > nul

echo Starting Frontend...
start cmd /k "cd frontend && npm run dev"

timeout /t 2 > nul

echo Opening VS Code...
code .

exit