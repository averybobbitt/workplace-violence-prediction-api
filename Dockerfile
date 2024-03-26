# To do: Find an image that already has a webserver
# This will change later. (ASGI or WSGI server)
FROM python:3.12

ENV DJANGO_DEBUG 1
# The OS sets
ENV PYTHONUNBUFFERED 1

# Set the working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt /app/
RUN pip install -r requirements.txt

# Copy the project code into the container
COPY . /app/
