FROM selenium/standalone-chrome:latest
WORKDIR /app
USER root
RUN apt-get update && apt-get install -y python3 python3-pip
COPY . /app
RUN pip install --no-cache-dir -r requirements.txt
ENV PYTHONUNBUFFERED=1