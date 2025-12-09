#!/bin/bash
set -e

echo "Build frontend"
cd frontend
npm install
npm run build

echo "Launch backend"
cd ../backend
uvicorn app.main:app --host 0.0.0.0 --port $PORT
