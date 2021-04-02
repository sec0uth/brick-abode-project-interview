# brick-abode-project-interview

## Getting started
1. You must download/clone the project.

2. You must install [docker](https://docs.docker.com/get-docker/) and [docker-compose](https://docs.docker.com/compose/install/). If you use Linux distributions, you may use alternatives like [podman](https://podman.io/getting-started/installation) and [podman-compose](https://github.com/containers/podman-compose). During the whole section, you are presented the commands with `docker`, but if you are using `podman` do not worry, just replace `docker` with `podman` and all should be fine given that it follows docker's of CLI (Command Line Interface).

    **Note: if using podman, sudo is not required**

3. You must build the base image, using the following command:

**Note: the tag name is important to identify as base image**

```bash
$ sudo docker build -t local-base:dev -f Dockerfile.base
```

4. You must create the `docker-compose.yaml`. You may use the example docker-compose file, like the following command:

```
$ cp docker-compose.yaml.example docker-compose.yaml
```

5. You can build the whole stack with the help of compose. The following command would build Juniper's and Ansible's development and production images.

```bash
$ sudo docker-compose build
```

You can target a single environment though.
```bash
$ sudo docker-compose build juniper-dev
```