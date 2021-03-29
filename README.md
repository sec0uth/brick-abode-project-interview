# brick-abode-project-interview

## Getting started
1. You must download/clone the project.

2. You must install [docker](https://docs.docker.com/get-docker/) and [docker-compose](https://docs.docker.com/compose/install/). If you use Linux distributions, you may use alternatives like [podman](https://podman.io/getting-started/installation) and [podman-compose](https://github.com/containers/podman-compose). During the whole section, you are presented the commands with both `podman` and `docker` altought them are CLI (Command Line Interface) compliants.

3. You must build the base image, using the following command:

**Note: the tag name is important to identify as base image**

```bash
$ podman build -t local-base:dev -f Dockerfile.base
```

with `docker` would be:

```bash
$ sudo docker build -t local-base:dev -f Dockerfile.base
```

4. You must create the `docker-compose.yaml`. You may use the example docker-compose file, like the folling command:

```
$ cp docker-compose.yaml.example docker-compose.yaml
```

5. You must build the development stack with the help of compose. The following command would build Juniper's and Ansible's development images.

```bash
$ podman-compose build
```

or with `docker`:

```bash
$ sudo docker-compose build
```

6. You can test Ansible running the command:

```bash
$ podman-compose run ansible-dev
```