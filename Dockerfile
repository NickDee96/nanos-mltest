FROM ubuntu:latest
ENV DEBIAN_FRONTEND noninteractive



RUN  apt-get update -y &&\
    apt-get install -y python3.6 curl wget zip openssl python3-distutils lsb-release gnupg locales firefox python3-dev && \
    mkdir pip && cd pip && wget https://bootstrap.pypa.io/get-pip.py && \
    python3 get-pip.py
RUN echo "en_US.UTF-8 UTF-8" >> /etc/locale.gen \
	&& locale-gen en_US.utf8 \
	&& /usr/sbin/update-locale LANG=en_US.UTF-8
ENV LC_ALL C.UTF-8
ENV LANG C.UTF-8
RUN cd /usr/bin && ln -s python3 python && cd ~


#RUN mkdir /code
COPY ./ /
RUN pip install -r requirements.txt


RUN wget --load-cookies /tmp/cookies.txt "https://docs.google.com/uc?export=download&confirm=$(wget --quiet --save-cookies /tmp/cookies.txt --keep-session-cookies --no-check-certificate 'https://docs.google.com/uc?export=download&id=1U3CDLbGAZILU7J28nWX9dJZtb4Kehtoq' -O- | sed -rn 's/.*confirm=([0-9A-Za-z_]+).*/\1\n/p')&id=1U3CDLbGAZILU7J28nWX9dJZtb4Kehtoq" -O wiki_pretrained_model.zip && rm -rf /tmp/cookies.txt
RUN unzip -q wiki_pretrained_model.zip -d /model/

EXPOSE 8050
ENTRYPOINT ["gunicorn", "--config", "gunicorn_config.py", "app:server"]
