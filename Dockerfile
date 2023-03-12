FROM python:3.10.5-slim as base
WORKDIR /code
RUN python3 -m pip install --upgrade pip

FROM base as prod_build
COPY requirements.txt .
RUN pip3 install -r requirements.txt
COPY manage.py .
COPY templates/ ./templates/
COPY config/ ./config/
COPY apps/ ./apps/
CMD gunicorn config.wsgi:application -c /code/config/gunicorn.conf.py

FROM base as dev_build
COPY requirements_dev.txt .
RUN pip3 install -r requirements_dev.txt
COPY manage.py .
COPY templates/ ./templates/
COPY config/ ./config/
COPY apps/ ./apps/
CMD gunicorn config.wsgi:application -c /code/config/gunicorn.conf.py