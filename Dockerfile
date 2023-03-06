# The first instruction is what image we want to base our container on
# We Use an official Python runtime as a parent image
FROM python:3.8.10-slim-buster


# install psycopg2 dependencies
RUN apt-get update \
    && apt-get -y install libpq-dev gcc

# Allows docker to cache installed dependencies between builds
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Mounts the application code to the image
COPY . code
WORKDIR /code

EXPOSE 8000
# EXPOSE 587  # For Gmail port
# Local port for email
EXPOSE 1025


# runs the production server
ENTRYPOINT ["python", "manage.py"]
CMD ["runserver", "0.0.0.0:8000"]
