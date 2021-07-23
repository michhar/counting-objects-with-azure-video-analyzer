# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

FROM ubuntu:18.04

# Install python
RUN apt-get update -y && \
    apt-get install -y --no-install-recommends python3-pip python3-dev && \
    cd /usr/local/bin && \
    ln -s /usr/bin/python3 python && \
    pip3 install --upgrade pip==21.0.1 setuptools

# Install python packages
RUN pip install numpy flask==1.0.1 Pillow==8.2.0 gunicorn==19.9.0 requests==2.25.1 azure-iot-device==2.7.1 && \
    apt-get clean

# Install runit, nginx
RUN apt-get update -y && \
    apt-get install --no-install-recommends -y wget runit nginx

# Install Nchan module. For details goto http://nchan.io
RUN apt-get update -y && \
    apt-get install -y libnginx-mod-nchan

# Create app folder
RUN mkdir /app && \
    cd /app && \
    rm -rf /var/lib/apt/lists/* && \
    apt-get clean && \
    apt-get purge -y --auto-remove wget

COPY app/exception_handler.py /app

# Copy nginx config file
COPY simple-server-app.conf /etc/nginx/sites-available

# Setup runit file for nginx and gunicorn
RUN mkdir /var/runit && \
    mkdir /var/runit/nginx && \
    /bin/bash -c "echo -e '"'#!/bin/bash\nexec nginx -g "daemon off;"\n'"' > /var/runit/nginx/run" && \
    chmod +x /var/runit/nginx/run && \
    ln -s /etc/nginx/sites-available/simple-server-app.conf /etc/nginx/sites-enabled/ && \
    rm -rf /etc/nginx/sites-enabled/default && \
    mkdir /var/runit/gunicorn && \
    /bin/bash -c "echo -e '"'#!/bin/bash\nexec gunicorn -b 127.0.0.1:8000 --chdir /app simple-server-app:app\n'"' > /var/runit/gunicorn/run" && \
    chmod +x /var/runit/gunicorn/run

# Copy the app file and the tags file
COPY app/simple-server-app.py /app/

EXPOSE 80

# Start runsvdir
CMD ["runsvdir","/var/runit"]
