FROM python:3.11-slim

WORKDIR /app

COPY src/server/requirements.txt .
RUN pip install -r requirements.txt

COPY src/ /app/src/
COPY data/ /app/data/

EXPOSE 8000

CMD ["sh", "-c", "uvicorn src.server.app:app --host 0.0.0.0 --port ${PORT:-8000}"]
