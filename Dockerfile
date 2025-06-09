FROM python:3.12.10-slim

WORKDIR /

COPY requirements.txt .

RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

COPY ./src ./src
COPY ./alembic.ini .

EXPOSE 3000

CMD ["/bin/sh", "-c", "alembic upgrade head && python -m src.main"]
