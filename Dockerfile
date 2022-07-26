FROM python:3.8

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update \
    && apt-get install -y netcat


# install dependencies
RUN pip install --upgrade pip


#COPY ./../requirements.txt .
#RUN pip install -r requirements.txt

#copy entrypoint.sh
COPY ./Innotter\ (Django\)/celery_entrypoint.sh .

# copy project
COPY ./'Innotter (Django)'/ .

RUN chmod +x celery_entrypoint.sh
ENTRYPOINT ./celery_entrypoint.sh