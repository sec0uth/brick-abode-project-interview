# brick-abode-project-interview
> Final test of the interview process.

# Table of contents
- [Building Docker Images](#building-docker-images)
- [Test & Run](#test--run)
  - [Juniper](#ansible)
  - [Ansible](#ansible)

# Building Docker Images
You can start testing or running with provided docker environment. Containers were the chosen method to achieve the requirement of testing and runing on a `Ubuntu 18.04` system.

## Requirements
 - [podman](https://podman.io/getting-started/installation) v3.0.1
 - [podman-compose](https://github.com/containers/podman-compose) v0.1.7dev

## Getting Started
Podman is the open source alternative to Docker, and one of it's features is rootless containers. You will see the commands without `sudo`, but off course you can run as root too.

1. You must download/clone the project.

2. You must build the base image, using the following command:

**Note: the tag name is important to identify as base image**

```bash
$ podman build -t local-base:dev -f Dockerfile.base
```

This base image is used both to test and run the application, so it should not be hard to make a different image using an operating system different than Ubuntu 18.04. 

3. You must create the `docker-compose.yaml`. You may use the example docker-compose file, with the following command:

```
$ cp docker-compose.yaml.example docker-compose.yaml
```

4. You can build the whole stack with the help of compose. The following command would build Juniper's and Ansible's development and production images.

```bash
$ podman-compose build
```

You can target a single environment though.
```bash
$ podman-compose build juniper-dev
```

Or even exactly what you really need.
```bash
$ podman-compose build ansible-dev juniper-prod
```

# Test & run

**You must have followed the steps to build the docker images before continuing.**

See issue [#14](https://github.com/sec0uth/brick-abode-project-interview/issues/14) for more details about docker environment strategy.

The very basic beggining is to get a shell on the image.

![image](https://user-images.githubusercontent.com/81310341/113460356-e184ac00-93ee-11eb-8ece-d8f9a93c765c.png)

Well done. 
You can now just run the `juniper-dev` image without the `bash` command, but with images' default command.

![image](https://user-images.githubusercontent.com/81310341/113460466-4f30d800-93ef-11eb-99ad-1e3d8caad21e.png)

You have just tested the image and hopefully the tests have passed. As one can see, the command accepts a custom script otherwise it uses the one provided by the developer.

## Juniper

What if you want to run Juniper production image? You may answer, just run `podman-compose run juniper-prod`.

But...

```
Traceback (most recent call last):
  File "juno-console.py", line 9, in <module>
    sys.exit(cli.main())
  File "/juniper/cli.py", line 31, in main
    configuration = config.read(config_file)
  File "/juniper/config.py", line 20, in read
    config = read_yaml(file_path)
  File "/juniper/config.py", line 33, in read_yaml
    with open(file_path, 'rb') as f_reader:
FileNotFoundError: [Errno 2] No such file or directory: '/config.yml'
1
```

It errors out with this traceback. It says that some `/config.yml` is not a file, or is missing. 

The Juniper application needs a configuration file with the user arguments like ssh host, banner message and so on. It can read this file from an environment variable called `JNPR_CONFIG_FILE`. So let's inspect the juniper service at `docker-compose.yml`.

```yml
...

juniper-prod:
    ...

    volumes:
        - ~/.ssh/config:/root/.ssh/config:Z,ro

        ## ssh public key authentication
        # - ~/.ssh/juniper_key:/root/.ssh/id_rsa:Z,ro

        ## Juniper configuration
        # - ./juniper-config.yml:/config.yml:Z,ro

    environment:
        JNPR_CONFIG_FILE: /config.yml
```

There it is. The compose file already set the environment variable, but the volume corresponding to the configuration file is commented out. You can copy the example configuration file to the expected file name and then uncomment that line.

```bash
$ cp juniper-config.yml.example juniper-config.yml
```

Now is the moment you take a deep breath, because before actually running Juniper, you must be aware of how the configuration file works.

### Configuration

You should read the speficiation in this issue [#11](https://github.com/sec0uth/brick-abode-project-interview/issues/11).

You may want just a quick configuration to test out if it works, and there it is:

```yml
## minimal configuration

ssh:
  host: juniper

changes:
  banner: "\\n\\n\\t\\t This is a Banner \\n\\n"

  user:
    name: anyone

  config: set system host-name juniper-router
```

You should note that when you do not specify a password for the `user`, the application will ask for one at runtime, as part of it's bootstraping process.

### SSH
The supported method to specify wich host to connect is using a [ssh_config](https://www.man7.org/linux/man-pages/man5/ssh_config.5.html) file. 

### Authentication
If you are connecting using a password, juniper-configuration file should look like this:

```yml
...

ssh:
  ...
  
  passwd: secret-password
```

Or you can provide a password at application runtime:

```yml
...

ssh:
  ...
  
  ask_passwd: true
```

The preferred authentication mechanism is public key. When using them, juniper-configuration file is not aware of such thing, the job is done by a [docker script](https://github.com/sec0uth/brick-abode-project-interview/blob/juniper-dev/docker-scripts/entrypoint.sh) that starts a ssh-agent and add the public key. You must then, edit the docker-compose file to reference your access private key in the volume:

```yml
...

juniper-prod:
    ...

    volumes:
      - ~/.ssh/config:/root/.ssh/config:Z,ro

      ## ssh public key authentication
      - ~/.ssh/your-juniper-private-key:/root/.ssh/id_rsa:Z,ro
```

You should note that `/root/.ssh/id_rsa` is hard-coded, so do not worry if you are not using RSA in your key. You just must ensure it mounts the private key at that path.

### Finally running juniper

After you have set ssh and juniper-configuration file, you may be able to run the Juniper production image with the discussed command:

```bash
$ podman-compose run juniper-prod
```

## Ansible

You can start to configure your inventory, for that you can use an example at `ansible/src/hosts.example`. This is a regular inventory, the only requirement in place is for the Cisco device to be part of the `ios` group, because there are already pre-configured `group_vars` adjusted for that group. 

For the purpose of explanation, imagine you named your inventory file `development-inventory`.

Now you must edit your docker-compose file to reflect this inventory you have just created.

```yml
...

ansible-dev:
    ...

    volumes:
      ... 

      - ./development-inventory:/inventory:Z,ro
```

This inventory configuration works in the same way on the `prod` environment.

Your next step is to configure the private key in the docker-compose file just like with `Juniper`. Uncomment the line corresponding to the ssh authentication and specify the path to the private key. In the end it should look like this:

```yml
...

ansible-dev:
    ...

    volumes:
      ## ssh public key authentication
      - ~/.ssh/your-cisco-private-key:/root/.ssh/id_rsa:Z,ro

      - ./development-inventory:/inventory:Z,ro
```

You can now successfully test Ansible using the command:

```bash
$ podman-compose run ansible-dev
```

For running the production image you need to configure an inventory and a configuration file. You can use the example configuration at `ansible-config.yml.example`.

As an example, the following configuration create two users:

```yml
banner:
  text: This is a Banner

user:
  name: little-cisco

config: 
  content: username test password 0 cisco
```

The password for user `little-cisco` is asked at runtime because it's missing in the file.

Docker-compose file would like this:

```yml
...

ansible-prod:
    ...

    volumes:
      ## ssh public key authentication
      - ~/.ssh/your-juniper-private-key:/root/.ssh/id_rsa:Z,ro

      - ./production-inventory:/inventory:Z,ro

      - ./ansible-config.yml:/config.yml:Z,ro
    environment:
      ANSIBLE_VARS_FILE: /config.yml
```

You are now able to run Ansible production image as expected:

```bash
$ podman-compose run ansible-prod
```

As result you get a banner a new user to login with:

![image](https://user-images.githubusercontent.com/81310341/113585017-04d37500-9602-11eb-84da-ebcd0f730b0e.png)
