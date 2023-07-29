FROM python:3.11-bullseye
LABEL MAINTAINER="Lucas Calegario"

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN python -m pip install --upgrade pip
WORKDIR /app/
COPY requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt
COPY ./app /app/app/
COPY alembic.ini /app/alembic.ini

ENV PYTHONPATH="${PYTHONPATH}:/app/"

RUN adduser user
USER user