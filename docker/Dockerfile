#
# Dockerfile for snn2spade/myscrapyd
#

FROM vimagick/scrapyd:py3
MAINTAINER Napat Paopongpaibul <napat.paopongpaibul@gmail.com>

RUN pip install selenium
RUN pip install pymongo

#WORKDIR /var/lib/scrapyd

RUN  apt-get update -y && \
     apt-get upgrade -y && \
     apt-get dist-upgrade -y && \
     apt-get -y autoremove && \
     apt-get clean
RUN apt-get install -y unzip \
    wget\
    && rm -rf /var/lib/apt/lists/*

# install chrome: using selenium remote instead
#RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
#RUN dpkg -i google-chrome-stable_current_amd64.deb; apt-get -fy install
#
#RUN wget -O /tmp/chromedriver.zip https://chromedriver.storage.googleapis.com/2.9/chromedriver_linux64.zip &&  unzip /tmp/chromedriver.zip chromedriver -d /usr/local/bin/;

