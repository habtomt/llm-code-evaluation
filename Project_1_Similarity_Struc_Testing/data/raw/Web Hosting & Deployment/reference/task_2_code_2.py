`python

# First, create 'settings.py' for production configuration

# settings.py

DEBUG = False



# Then use Docker to containerize the Django application



# Dockerfile

FROM python:3

ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY requirements.txt /app/

RUN pip install -r requirements.txt

COPY . /app/



# build the Docker container

# $ docker build -t django_app .



# Deploy the container behind a web server using AWS Elastic Beanstalk



# Create a file named 'Dockerrun.aws.json' in the project root with the following content:

{

  "AWSEBDockerrunVersion": 2,

  "containerDefinitions": [{

    "name": "django",

    "image": "django_app",

    "portMappings": [{

      "hostPort": 80,

      "containerPort": 8000

    }]

  }]

}



# $ eb create