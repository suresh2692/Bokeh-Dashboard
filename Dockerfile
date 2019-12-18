FROM debian:stable-slim
RUN apt-get update
RUN apt-get -y install python3
RUN apt-get -y install curl
RUN apt install -y python3-pip

COPY . /app
WORKDIR /app/src
RUN pip3 install -r ../requirements.txt
EXPOSE 5959
CMD bokeh serve views.py --port=5959
