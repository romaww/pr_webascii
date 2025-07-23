FROM python:3.9-slim

RUN apt-get update && apt-get install -y \
    fonts-dejavu-core \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

RUN pip install Flask==2.3.3 Pillow==10.0.1
#RUN pip install -r requiroments.txt

COPY app/. .
EXPOSE 5000

CMD ["python3", "main.py"]
