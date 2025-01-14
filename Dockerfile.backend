FROM python:3.11

WORKDIR /app

# poetry install
RUN pip install -U poetry

COPY poetry.lock pyproject.toml /app/

# Poetry을 이용하여 의존성 설치
RUN poetry config virtualenvs.create false \
	&& poetry install --no-root --no-interaction

# 로컬에 있는 소스코드를 컨테이너로 복사
COPY ./backend /app/backend

# Python 경로 설정
ENV PYTHONPATH=/usr/local/bin/python3.11

# Poetry 바이너리 권한 확인 및 설정
RUN chmod +x /usr/local/bin/poetry

# Poetry가 설치된 Python을 사용하도록 설정
RUN sed -i '1s|^.*$|#!/usr/local/bin/python3.11|' /usr/local/bin/poetry

COPY entrypoint.sh /app/backend/entrypoint.sh
RUN chmod +x /app/backend/entrypoint.sh

WORKDIR /app/backend

ENTRYPOINT ["/app/backend/entrypoint.sh"]

