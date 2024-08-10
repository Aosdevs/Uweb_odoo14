#!/bin/sh

# install PPA
apt install -y software-properties-common
add-apt-repository ppa:deadsnakes/ppa -y

# update and install
apt update
apt install python3.8 python3.8-dev python3.8-venv

# setup alternatives
update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3 1
update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.8 2

# show menu for selecting the version
update-alternatives --config python3

# or one command to set it
# update-alternatives --set python3 /usr/bin/python3.8