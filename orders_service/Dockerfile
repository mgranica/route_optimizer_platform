# Use an official Python runtime as a parent image
FROM python:3.10-buster

# Define a build argument
ARG AWS_ACCESS_KEY_ID
ARG AWS_SECRET_ACCESS_KEY
ARG AWS_SESSION_TOKEN

# Set the environment variable
ENV AWS_ACCESS_KEY_ID=${AWS_ACCESS_KEY_ID}
ENV AWS_SECRET_ACCESS_KEY=${AWS_SECRET_ACCESS_KEY}
ENV AWS_SESSION_TOKEN=${AWS_SESSION_TOKEN}

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