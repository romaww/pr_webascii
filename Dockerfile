FROM python:3.9-slim

RUN apt-get update && apt-get install -y \
    fonts-dejavu-core \
    curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY app/requirements.txt .
RUN pip install -r requirements.txt

COPY app/. .
EXPOSE 80

CMD ["python3", "main.py"]
