FROM python:3.13-slim AS base
WORKDIR /usr/src/backend

COPY . /usr/src/backend/

RUN pip install --no-cache-dir -r requirements.txt

ENV RUNTIME=docker
ENV ENVIRONMENT=production
ENV DATABASE_URL=sqlite:///./sqlite.db

EXPOSE 8080/tcp
CMD ["python", "main.py"]
