FROM python:3.8

RUN mkdir -p /root/.streamlit
RUN bash -c 'echo -e "\
[general]\n\
email = \"\"\n\
" > /root/.streamlit/credentials.toml'
RUN bash -c 'echo -e "\
[server]\n\
enableCORS = false\n\
" > /root/.streamlit/config.toml'

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

ENV NAME stickers
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

RUN pip install --trusted-host pypi.python.org -r requirements.txt
RUN mkdir -p /root/.streamlit
RUN bash -c 'echo -e "\
[general]\n\
email = \"\"\n\
" > /root/.streamlit/credentials.toml'
RUN bash -c 'echo -e "\
[server]\n\
enableCORS = false\n\
" > /root/.streamlit/config.toml'

EXPOSE 8051
# copying everything over
COPY . .

CMD["screamlit","run","UI.py"]