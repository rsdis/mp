#!/bin/bash
#install software
running_folder=`pwd`
#sudo apt-get update
#sudo apt-get -y install curl
#sudo apt-get -y install zip
#sudo apt-get -y install nginx
#sudo apt-get -y install python3
#sudo apt-get -y install python3-pip
#pip3.6 install flask
#pip3.6 install websockets
#pip3.6 install python-etcd
#pip3.6 install requests
cd ~
current_folder=`pwd`
mkdir 'dis-program'
mkdir 'dis-tmp'
mkdir 'dis-update'
cp  $running_folder'/pre_install.sh' './dis-program/'
curl -o './dis-tmp/app.zip' 'http://www.baidu.com'
chmod +x $current_folder'/dis-program/pre_install.sh'
started=`grep "pre_install" "/home/ethan/.profile"`
echo $started
if $started == "" then
    cmd=$current_folder'/dis-program/pre_install.sh'
    echo $cmd >> '/home/ethan/.profile'
fi
