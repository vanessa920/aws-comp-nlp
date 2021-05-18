FROM python:3.8

MAINTAINER shengxio@ualberta.ca
USER root

WORKDIR /app

ADD __init__.py /app
ADD engine.py /app
ADD FileControl.py /app
ADD nlp_engine.pkl /app
ADD README.md /app
ADD requirements.txt /app
ADD UI.py /app
ADD UI-control.js /app
ADD UI-style.js /app
ADD utilities.py /app
ADD Dockerfile /app
ADD city_SanJose_Minutes.csv /app

RUN pip install --trusted-host pypi.python.org -r requirements.txt

EXPOSE 8051
ENV NAME stickers

CMD["screamlit","run","UI.py"]