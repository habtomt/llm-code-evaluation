
# Dockerfile

# Build:   docker build -t code-quality-classifier .
# Run  :   docker run -p 8000:8000 \
#              -v $(pwd)/data:/app/data \
#              -v $(pwd)/models:/app/models \
#              -v $(pwd)/results:/app/results \
#              code-quality-classifier

# Then open: http://localhost:8000
# API docs : http://localhost:8000/docs

FROM python:3.11-slim

#  System deps 
RUN apt-get update && apt-get install -y --no-install-recommends \
        build-essential \
        git \
    && rm -rf /var/lib/apt/lists/*

#  Working directory 
WORKDIR /app

#  Python dependencies (cached layer) 
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip \
 && pip install --no-cache-dir -r requirements.txt

#  Application code 
COPY features/ ./features/
COPY labeling/ ./labeling/
COPY models/ ./models/
COPY api/api.py ./api.py
COPY run_pipeline.py .
COPY ui/ ./ui/

#  Create persistent directories (overridden by volume mounts) 
RUN mkdir -p data/raw data/processed models results

#  Environment 
ENV PYTHONUNBUFFERED=1
ENV MODELS_DIR=/app/models
ENV UI_DIR=/app/ui

#  Expose port 
EXPOSE 8000

#  Default: start FastAPI 
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "1"]
