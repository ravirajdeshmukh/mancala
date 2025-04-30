FROM python:3.11-slim

WORKDIR /app

COPY . .

ENV PYTHONPATH=/app

CMD ["python", "src/main.py"]
