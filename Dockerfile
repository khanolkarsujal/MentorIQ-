FROM python:3.12-slim

WORKDIR /app

# Install backend dependencies
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend source (the 'app' package lives at /app/app)
COPY backend/ ./

EXPOSE 8000

# Run uvicorn from /app so 'app.main' resolves correctly
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
