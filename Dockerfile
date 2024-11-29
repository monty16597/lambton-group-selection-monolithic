FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN apt-get update && \
    apt-get install -y pkg-config python3-dev default-libmysqlclient-dev build-essential && \
    pip install -r requirements.txt && \
    rm -rf /var/lib/apt/lists/*
COPY . .
CMD ["python", "app.py"]
