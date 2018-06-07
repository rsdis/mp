#!/bin/bash


#a. auto login, config


#b. disable update, the solution is remove update manager
sudo apt-get -y remove update-manager

#c. set desktop background image

#d. install chrom,python,nginx and python dependency
sudo apt-get update
sudo apt-get -y install curl
sudo apt-get -y install zip
sudo apt-get -y install nginx
#install python
sudo apt-get -y install python3.6
sudo apt-get -y install python3-pip
#install python library
pip3.6 install flask
pip3.6 install websockets
pip3.6 install python-etcd
pip3.6 install requests
pip3.6 install pyserial

