FROM ubuntu:bionic

RUN apt update -y && apt install -y \
        python3 python3-dev python3-pip build-essential git

ADD ./docker-scripts/entrypoint.sh /usr/local/bin/

ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]