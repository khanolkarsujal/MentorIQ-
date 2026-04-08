# ─── STAGE 1: Build Frontend ──────────────────────────────────────────
FROM node:20-alpine AS frontend-builder
WORKDIR /build/frontend
COPY frontend/package*.json ./
RUN npm install
COPY frontend/ ./
RUN npm run build

# ─── STAGE 2: Build Backend & Serve ───────────────────────────────────
FROM python:3.12-slim
WORKDIR /app

# Install backend dependencies
COPY backend/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend code
COPY backend/ ./

# Copy the built frontend from Stage 1 into the backend's expected path
COPY --from=frontend-builder /build/frontend/dist ./frontend/dist

# Expose port 8000 (FastAPI)
EXPOSE 8000

# Start the application
# The backend is already configured to serve frontend/dist/index.html automatically
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
