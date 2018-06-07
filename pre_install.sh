#!/bin/bash
#------------------------------
# readme, execute follow command
# wget -O install.sh https://raw.githubusercontent.com/rsdis/mp/master/pre_install.sh && sh install.sh && rm -f install.sh
#
#-----------------------------
#read serviceid

#touch_device_name='ETPS/2 Elantech Touchpad'
#screen_id=`xinput list --id-only "$touch_device_name"`
#echo $screen_id

echo "============> input service id and then press enter"
read user_input_service_id
echo "============> your input service id is "$user_input_service_id

echo "============> route screen and touch input"
sudo xrandr -o left
xinput set-prop "Your Touchscreen's Name" --type=float "Coordinate Transformation Matrix" 0 -1 1 1 0 0 0 0 1

#a. auto login, config
#b. disable update, the solution is remove update manager
echo "============> remove ubuntu update manager"
sudo apt-get -y remove update-manager
#c. set desktop background image
#d. install chrom,python,nginx and python dependency
#install python
echo "============> install python 3.6 version"
sudo add-apt-repository -y ppa:deadsnakes/ppa
sudo apt-get update
sudo apt-get -y install python3.6

echo "============> install chrome browser"
sudo apt-get -y install chromium-browser
#menu config chrome


echo "============> install curl tool"
sudo apt-get -y install curl
echo "============> install zip tool"
sudo apt-get -y install zip
echo "============> install nginx service"
sudo apt-get -y install nginx
echo "============> install pip 3.6"
curl https://bootstrap.pypa.io/get-pip.py | sudo python3.6
#install python library
echo "============> install rsdis related python library"
sudo pip3.6 install flask
sudo pip3.6 install websockets
sudo pip3.6 install python-etcd

#donload default start up apps
echo "============> download default rsdis client, and unzip into fview folder"
cd ~ 
wget -O client.zip http://rsdisprd.blob.core.chinacloudapi.cn/install/default_install_package/dis.zip
unzip -o client.zip -d ./fview
rm -f client.zip
#write service id
echo "============> write service id into rsdis client"
rm -f  ./fview/dis/buildin/vers/service_id.ver
echo $user_input_service_id >> ./fview/dis/buildin/vers/service_id.ver
#start service

echo "============> first time mush open browser via browser, just close broswer, keep script going"
chromium-browser

cd ~/fview/dis/
echo "============> start dis application"
sh run.sh