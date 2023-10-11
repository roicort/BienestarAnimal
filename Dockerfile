# Use an official Python runtime based on Debian 10 "buster" as a parent image.
FROM ubuntu:latest

# Define build argument.
ARG SA_KEY_BASE64

# Create a temp key file with the service account key.
RUN echo $SA_KEY_BASE64 | base64 --decode > /tmp/sa-artifact-registry.json

# Set the environment variable for the service account key.
ENV GOOGLE_APPLICATION_CREDENTIALS=/tmp/sa-artifact-registry.json

# Add user that will be used in the container.
RUN useradd django

# Port used by this container to serve HTTP.
EXPOSE 8080

# Set environment variables.
# 1. Force Python stdout and stderr streams to be unbuffered.
# 2. Set PORT variable that is used by Gunicorn. This should match "EXPOSE"
#    command.
ENV PYTHONUNBUFFERED=1 \
    PORT=8080

# Install system packages required by django and Django.
RUN apt-get update --yes --quiet

RUN apt-get install --yes --quiet --no-install-recommends \
    git \
    python-is-python3 \
    gdal-bin \
    libgdal-dev\
    ca-certificates \
    pkgconf \
    pip \
    && rm -rf /var/lib/apt/lists/*

# Install Python packages required by the project.
RUN python -m pip install --upgrade pip && pip install --no-cache-dir "gunicorn==20.0.4" "keyrings.google-artifactregistry-auth" "GDAL" "Pillow"

# Install MTY libs
RUN pip install --no-cache-dir -U \
    --extra-index-url=https://us-central1-python.pkg.dev/mty-god-webservices-qa/mty-libs/simple/ \
    mty-firebase-auth

# Install the project requirements.
COPY pip.conf /
COPY requirements.txt /
RUN pip install -r /requirements.txt

# Use /app folder as a directory where the source code is stored.
WORKDIR /app

# Set this directory to be owned by the "django" user. This django project
# uses SQLite, the folder needs to be owned by the user that
# will be writing to the database file.
RUN chown django:django /app

# Copy the source code of the project into the container.
COPY --chown=django:django . .

# Use user "django" to run the build commands below and the server itself.
USER root

# Collect static files.

RUN python manage.py collectstatic --noinput --clear

#RUN python manage.py makemigrations && python manage.py migrate;

CMD set -xe; gunicorn MTY_EMPLEO.wsgi:application