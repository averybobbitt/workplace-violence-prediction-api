FROM python:3.12

# Set environment variables
ENV PYTHONUNBUFFERED 1

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt /app/
RUN pip install -r requirements.txt

# Copy the project code into the container
COPY . /app/
