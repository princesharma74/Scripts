# Pull the official base image
FROM selenium/standalone-chrome:latest

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /code

# Install dependencies
COPY requirements.txt /code/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN apt-get update

# Copy project
COPY . /code/