#!/bin/sh

# Alembic 마이그레이션 실행
poetry run alembic upgrade head

# FastAPI 애플리케이션 실행
exec poetry run uvicorn main:app --host 0.0.0.0 --port 8000
