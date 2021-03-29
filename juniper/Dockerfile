FROM ubuntu:18.04

RUN apt update -y && apt install -y \
        python3 python3-dev python3-pip git

ADD ./juniper/docker-scripts/entrypoint.sh /usr/local/bin/

RUN chmod 755 /usr/local/bin/entrypoint.sh

ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]