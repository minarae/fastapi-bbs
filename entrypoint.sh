export HOST=${HOST:-0.0.0.0}
export PORT=${PORT:-8000}

alembic upgrade head
uvicorn --reload --host $HOST --port $PORT app.main:app
