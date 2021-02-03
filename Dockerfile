FROM ubuntu:focal-20210119

ENV PYTHONUNBUFFERED 1

RUN apt update -y
RUN apt install python3.8 -y
RUN update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.8 1
RUN apt install python3-pip -y
RUN pip3 install pipenv

COPY ./Pipfile /Pipfile
COPY ./Pipfile.lock /Pipfile.lock
RUN pipenv install --deploy --system

RUN mkdir /app
WORKDIR /app
COPY ./app .

RUN useradd --no-create-home restricted_user
RUN chown restricted_user:restricted_user /app
RUN chmod 755 /app
USER restricted_user