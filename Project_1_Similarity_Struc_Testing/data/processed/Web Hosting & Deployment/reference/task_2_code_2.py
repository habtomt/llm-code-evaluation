`python

DEBUG =False

FROM python :3

ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY requirements .txt /app /

RUN pip install -r requirements .txt

COPY ./app /

{

"AWSEBDockerrunVersion":2 ,

"containerDefinitions":[{

"name":"django",

"image":"django_app",

"portMappings":[{

"hostPort":80 ,

"containerPort":8000

}]

}]

}