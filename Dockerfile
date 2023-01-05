# TODO: use slim version later
FROM python:3.10.5
WORKDIR /app
COPY requirements.txt .
RUN python3 -m pip install --upgrade pip
RUN pip3 install -r requirements.txt
COPY manage.py .
COPY config/ ./config/
COPY apps/ ./apps/
CMD gunicorn config.wsgi:application -c /app/config/gunicorn.conf.py
