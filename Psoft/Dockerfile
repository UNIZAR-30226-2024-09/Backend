FROM python:3.12.2

# Install GCC compiler and related build tools
RUN apt-get update \
    && apt-get install -y gcc libc-dev nano net-tools \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory in the Docker container
WORKDIR /Psoft

# Copy the requirements file into the container at /Psoft
COPY requirements.txt /Psoft/

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

# Copy the rest of the application code into the container at /Psoft
COPY . /Psoft
