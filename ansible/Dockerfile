FROM local-base:dev

# install module dependencies in build-time
ADD ./requirements.txt /tmp/ansible-requirements.txt

RUN pip3 install -r /tmp/ansible-requirements.txt && \
        ansible-galaxy collection install cisco.ios

CMD ["ansible-playbook", "automate.yml"]
