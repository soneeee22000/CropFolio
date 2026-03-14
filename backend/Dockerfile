FROM python:3.10-slim

WORKDIR /app

COPY pyproject.toml .
RUN pip install --no-cache-dir .

COPY app/ app/
COPY data/ data/

ENV PORT=8000

CMD uvicorn app.main:app --host 0.0.0.0 --port $PORT
