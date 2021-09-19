FROM python:3.8



WORKDIR /code
RUN apt-get update
RUN apt-get install ffmpeg libsm6 libxext6  -y
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt


# COPY mime.types /etc/mime.types

COPY . .