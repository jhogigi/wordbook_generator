FROM python:3.8

RUN apt-get update
RUN apt-get install -y vim less tmux
RUN pip install --upgrade pip
EXPOSE 8000

