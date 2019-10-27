FROM ubuntu:17.10

# Install basic environment
ENV DEBIAN_FRONTEND noninteractive
RUN apt-get update && apt-get upgrade -y && apt-get install -y \
wget vim git iputils-ping python3 python3-pip unzip
RUN echo 'deb http://download.opensuse.org/repositories/isv:/ownCloud:/desktop/Ubuntu_17.04/ /' > /etc/apt/sources.list.d/owncloud-client.list
RUN wget -nv https://download.opensuse.org/repositories/isv:ownCloud:desktop/Ubuntu_17.04/Release.key -O Release.key
RUN apt-key add - < Release.key
RUN apt-get update && apt-get upgrade -y
RUN apt-get install -y \
owncloud-client \
scantailor libtiff-tools pdftk imagemagick
RUN python3 -m pip install python-dateutil
RUN wget https://github.com/BastiTee/bastis-python-toolbox/archive/master.zip
RUN unzip master.zip -d /bastis-python-toolbox

# Copy working files
RUN mkdir /workdir
COPY *.py /workdir/
COPY *.json /workdir/

# Finalize configuration
WORKDIR /workdir
ENV PYTHONPATH /bastis-python-toolbox/bastis-python-toolbox-master

ENTRYPOINT ["/workdir/scan2mail.py"]
