# WINDOWS need to install Xming X server for windowsls
# https://sourceforge.net/projects/xming/files/latest/download

#install usb utils


# Use the base Python 3.10 image
FROM python:3.10

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app/

# Install required packages and dependencies
RUN apt-get update && apt-get install -y \
    xvfb \
    xauth \
    x11-apps

RUN pip3 install --user fluigent_sdk-23.0.0.zip
RUN pip3 install -r requirements.txt
RUN pip3 install logic2-automation
RUN pip3 install sensirion-shdlc-driver
RUN pip3 install usb utils


# Set the DISPLAY environment variable
ENV DISPLAY=host.docker.internal:0.0

CMD ["python3", "/app/Modules/mp_ceci.py"]


# docker build -t my-python-app .do
# docker run -it --rm my-python-app
#docker run -it --rm image /bin/bash
# How to run docker with usb

#powershell
# echo $env:USERPROFILE\Desktop

# docker run -t -i --privileged -v /dev/bus/usb:/dev/bus/usb image bash

# docker run -t -i --privileged -v /dev/bus/usb:/dev/bus/usb -v $HOME/Desktop:/mnt/desktop image bash


