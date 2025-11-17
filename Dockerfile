FROM python:3.11-slim

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt
RUN rm -rf /root/.cache/pip
RUN pip install --no-cache-dir -r /app/requirements.txt

COPY . /app

EXPOSE 8080
