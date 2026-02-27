FROM python:3.11-slim

WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy app files
COPY api/ ./api/
COPY frontend/ ./frontend/
COPY models/ ./models/

# Expose port (HF Spaces uses 7860)
EXPOSE 7860

# Run the FastAPI app
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "7860"]

# Install minimal Python dependencies (fastapi + uvicorn)
RUN pip install --upgrade pip setuptools wheel
RUN pip install fastapi uvicorn[standard]

# Expose port for API and (optionally) static server
EXPOSE 8000

# Start uvicorn serving the FastAPI app. Note: we serve only the API here.
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]
