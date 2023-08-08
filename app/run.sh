#!bin/sh
alembic upgrade head 
gunicorn server:app --workers 5 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0