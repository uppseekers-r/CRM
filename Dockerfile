# Base environment
FROM python:3.11-slim

WORKDIR /app

# System utility configurations
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8501
EXPOSE 8000

# Start script running execution environments parameters pipeline concurrently
CMD ["sh", "-c", "uvicorn backend.api.main_api:app --host 0.0.0.0 --port 8000 & streamlit run frontend/main.py --server.port 8501 --server.address 0.0.0.0"]
