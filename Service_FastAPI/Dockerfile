FROM python:3.8

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update \
    && apt-get install -y netcat

EXPOSE 8080

# install dependencies
RUN pip install --upgrade pip


COPY ./requirements.txt .
RUN pip install -r requirements.txt

# copy fastapi_entrypoint.sh
COPY ./fastapi_entrypoint.sh .

# copy project
COPY . .

ENTRYPOINT ./fastapi_entrypoint.sh