# Pull build image
FROM python:3.8

# Set environment varibles
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /code

# Install dependencies
COPY requirements.txt /code/

RUN apt-get update && apt-get install -y \
  postgresql-client \
  binutils \
  libproj-dev

RUN pip install -r requirements.txt

# Copy project content
COPY app/ /code

# Run server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
