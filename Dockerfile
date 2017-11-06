#base image
FROM resin/rpi-raspbian:jessie

# Install dependencies
RUN apt-get update && apt-get install -y \
    git-core \
    build-essential \
    gcc \
    python \
    python-dev \
    python-pip \
    python-virtualenv \
    ca-certificates \
    git \
    lsb-release \
    ssh \
    vim \ 
    curl \
    libssl-dev \
    libffi-dev \
    fswebcam \
    screen \
    python-picamera \
    cron

RUN echo "deb http://packages.cloud.google.com/apt cloud-sdk-$(lsb_release -c -s) main" >> /etc/apt/sources.list
RUN curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | apt-key add -
RUN apt-get update && \
    apt-get install -y google-cloud-sdk
#ENV PATH /google-cloud-sdk/bin:$PATH
#RUN curl https://sdk.cloud.google.com | bash
#RUN apt-get install -y wget
#RUN wget https://dl.google.com/dl/cloudsdk/channels/rapid/downloads/google-cloud-sdk-175.0.0-linux-x86_64.tar.gz

RUN git clone git://git.drogon.net/wiringPi
RUN cd wiringPi && ./build
RUN pip install wiringpi2

#ENV PATH /google-cloud-sdk/bin:$PATH
#RUN curl https://sdk.cloud.google.com | bash

# install python libraries through pip
COPY src/requirements.txt /root/
RUN pip install -r /root/requirements.txt

COPY src /root

# contab for the image capture every hour
COPY src/rasp_docker_cron /etc/cron.d/rasp_docker_cron
RUN chmod 0644 /etc/cron.d/rasp_docker_cron
RUN chmod 777 /root/bash_script.sh
RUN crontab /etc/cron.d/rasp_docker_cron

#install the temperature sensor library
WORKDIR root/MCP9808/
RUN sudo python setup.py install

EXPOSE 80

#Google Cloud authentication through credential file
ENV GOOGLE_APPLICATION_CREDENTIALS="/root/rootfarm-6e380be3a2cb.json"
RUN gcloud auth activate-service-account --key-file /root/rootfarm-6e380be3a2cb.json

WORKDIR /root
#ENTRYPOINT ["/root/entrypoint.sh"]
CMD ["cron","-f"]
VOLUME ["/root/.config"]
