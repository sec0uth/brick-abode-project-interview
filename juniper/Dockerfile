FROM local-base:dev

# install module dependencies in build-time
## this saves bandwidth as dependencies are already present in image
ADD ./requirements.txt /tmp/juniper-requirements.txt
RUN pip3 install -r /tmp/juniper-requirements.txt

CMD ["python3", "juno-console.py"]