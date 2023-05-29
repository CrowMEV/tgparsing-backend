FROM python:3.11-alpine

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

CMD alembic upgrade head && \
    uvicorn server:app --host 0.0.0.0 --reload --forwarded-allow-ips='*' --proxy-headers && \
    gunicorn -k uvicorn.workers.UvicornWorker