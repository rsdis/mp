#!/bin/bash
started=`grep "auto-install-update.sh" "/home/ethan/.profile"`
if [$started == ""]; then
    echo 'start add auto start'
    echo '/home/ethan/dis/auto-install-update.sh' >> '/home/ethan/.profile'
    echo 'add start auto start'
fi
echo 'perform apt update'
sudo apt-get update
sudo apt-get -y curl
sudo apt-get -y install nginx
sudo apt-get -y install python3
sudo apt-get -y install python3-pip
pip3.6 install flask
pip3.6 install websockets
pip3.6 install python-etcd
pip3.6 install requests
mkdir '/home/ethan/dis'
curl -o '/home/ethan/dis/auto-install-update.sh' 'http://www.baidu.com'
chmod +x '/home/ethan/dis/auto-install-update.sh'

