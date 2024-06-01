# Use an official Python runtime as a parent image
FROM python:3.10-buster

# Install AWS CLI
RUN apt-get update && \
    apt-get install -y unzip groff mandoc && \
    apt-get clean  && \
    rm -rf /var/lib/apt/lists/*  && \
    curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"  && \
    unzip awscliv2.zip  && \
    ./aws/install

RUN pip install pipenv

# Install any needed packages specified in pipifile
ADD Pipfile ./
ADD Pipfile.lock ./

RUN pipenv install

# Install glue kernel
RUN pipenv run install-glue-kernels

# Set the working directory in the container to /workdir
WORKDIR /workdir

# Start bash with pipenv environment loaded
ENTRYPOINT ["pipenv", "run"]