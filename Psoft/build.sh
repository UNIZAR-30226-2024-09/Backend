#!/bin/bash

# Get the ID of the first container
container_id=$(docker ps --format '{{.ID}}' | head -n 1)

# Stop and remove the container if it exists
if [ ! -z "$container_id" ]; then
    docker stop "$container_id" && docker rm "$container_id"
fi

# Build the Docker image
docker build -t psoft-django .

# Remove dangling images
docker image prune -f

# Run a new container and start the Django server
docker run -p 8000:8000 -d psoft-django bash -c "nohup python manage.py runserver 172.17.0.2:8000 > django_server.log 2>&1"

# Get the ID of the newly created container
container_id2=$(docker ps --format '{{.ID}}' | head -n 1)

# Execute a command inside the newly created container
if [ ! -z "$container_id2" ]; then
    docker exec -it "$container_id2" /bin/bash
fi