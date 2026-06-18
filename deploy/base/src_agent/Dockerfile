FROM python:3.13-slim
WORKDIR /app
RUN pip install --no-cache-dir networkx==3.3 python-docx python-pptx openpyxl lxml
COPY main.py .
EXPOSE 8080
CMD ["python3", "main.py"]
