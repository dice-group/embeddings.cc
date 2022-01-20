# syntax=docker/dockerfile:1

FROM ubuntu:18.04

WORKDIR /app
RUN apt-get update
RUN apt-get install -y python
RUN apt-get install -y build-essential
RUN apt-get install -y python-pip python-dev
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
ENV LC_ALL="en_US.utf-8"
ENV LANG="en_US.utf-8"
COPY . .

CMD [ "python", "-m" , "flask", "run", "--host=0.0.0.0"]
