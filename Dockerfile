FROM python:3.10
LABEL author='Label A'

WORKDIR /app

# Environment
RUN apt-get update
RUN pip install --upgrade pip

# Regular Python dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy our codebase into the container
COPY . /app/

# Ops Parameters
ENV PYTHONUNBUFFERED=1
