
FROM ubuntu:16.04

################################################################################
# Add the service build metadata                                               #
################################################################################

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        sudo \
        apt-utils \
        apt-transport-https \
        python3 \
        python3-dev \
        python3-pip \
        python3-setuptools \
        git

ENV HOME /opt/playground

RUN sudo useradd -ms /bin/bash -r -d ${HOME} mr

# install python dependencies
COPY requirements.txt /${HOME}
RUN pip3 install --upgrade pip \
    && sudo pip3 install -I -r /${HOME}/requirements.txt \
    && rm  /${HOME}/requirements.txt

RUN sudo chown -R mr:mr /opt/playground

USER mr

# copy in python project
COPY ./mmafighting ${HOME}

WORKDIR ${HOME}

#CMD ["python3", "main.py"]
