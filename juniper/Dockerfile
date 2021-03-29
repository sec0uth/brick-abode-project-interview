FROM ubuntu:18.04

# install dependencies
RUN apt update -y && apt install -y \
        python3 python3-dev python3-pip git

# configure default entrypoint command
ADD ./juniper/docker-scripts/entrypoint.sh /usr/local/bin/
RUN chmod 755 /usr/local/bin/entrypoint.sh

# install module dependencies in build-time
## this saves bandwidth as dependencies are already present in image
ADD ./juniper/requirements.txt /tmp/juniper-requirements.txt
RUN pip3 install -U pip && \
        pip3 install -r /tmp/juniper-requirements.txt

CMD ["/usr/local/bin/entrypoint.sh"]