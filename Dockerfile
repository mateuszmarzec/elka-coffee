FROM python:3.7
ENV PYTHONUNBUFFERED 1

RUN apt-get update

COPY ./requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . code
WORKDIR code

EXPOSE 8000
