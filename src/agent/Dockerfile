FROM python:3.13-slim
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip install --no-cache-dir networkx==3.3 python-docx python-pptx openpyxl lxml

# Copy server files (ConfigMap provides the rest)
COPY server.py .

EXPOSE 8080
CMD ["python3", "server.py"]
