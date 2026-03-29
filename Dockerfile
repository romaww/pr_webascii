FROM python:3.12-alpine3.23

WORKDIR /app

COPY app/requirements.txt .
RUN apk add --no-cache curl ttf-dejavu \
    && pip install --no-cache-dir -r requirements.txt

COPY app/. .
EXPOSE 5000

CMD ["python3", "main.py"]
