
# Updating the HTTP Simple Server for Custom Usage

The following instructions will enable you to build a Docker container with a mock https server using [nginx](https://www.nginx.com/), [gunicorn](https://gunicorn.org/), [flask](https://github.com/pallets/flask), [runit](http://smarden.org/runit/), and [pillow](https://pillow.readthedocs.io/en/stable/index.html).

Note: References to third-party software in this repo are for informational and convenience purposes only. Microsoft does not endorse nor provide rights for the third-party software. For more information on third-party software please see the links provided above.

## Prerequisites

- ARM64v8 device upon which to build the image or method to build cross-platform docker images targeting ARM64 (if needed [Install Docker on Windows](http://docs.docker.com/docker-for-windows/install/) or [Install Docker on MacOS](https://docs.docker.com/docker-for-mac/install/))

## Building the Docker container

> IMPORTANT:  The docker container must be built on ARM64v8 device or with a cross-platform build tool targeting ARM64 as this is the Percept DK architecture.

To build the container image, run the following Docker command from a terminal. The process should take a few minutes to complete. 

```bash
    docker build -f simple-server.dockerfile . -t avaextension:http-simple-server-v1.0
```

## Upload Docker image to Azure container registry

Follow instructions in [Push and Pull Docker images - Azure Container Registry](http://docs.microsoft.com/azure/container-registry/container-registry-get-started-docker-cli) to save your image for later use on another machine.

## Deploy as an Azure IoT Edge module

Follow instruction in [Deploy module from Azure portal](https://docs.microsoft.com/azure/iot-edge/how-to-deploy-modules-portal) to deploy the container image as an IoT Edge module (use the IoT Edge module option).
