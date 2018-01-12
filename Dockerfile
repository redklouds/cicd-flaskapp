#from alpine in theory because we are using an alpine distro, pip3 and python3
# SHOULD be included in this alpine package if we do not require other packages
# included in the apk-get ubuntu package manager, then the blow lines will be
# sufficent
FROM alpine:3.6
#because we are using an alpine distribution, apt-get is an ubuntu distribution
#to get it we need to run apk update/aspk add
RUN apk add --update python3
#RUN apk add --update python3 py-pip
#RUN apt-get update -y 
#RUN apt-get install python3-pip -y
COPY requirements.txt /src/requirements.txt
RUN pip3 install -U pip setuptools wheel
ADD /libs /libs
RUN pip3 install -r /src/requirements.txt
COPY app.py /src
COPY engines /src/engines
COPY docker-compose.yml /src
CMD python3 /src/app.py
