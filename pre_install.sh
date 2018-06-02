#!/bin/bash


#------------------------------
# readme, execute follow command
# # wget -O install.sh https://raw.githubusercontent.com/rsdis/mp/master/pre_install.sh && sh install.sh && rm -f install.sh
#
#-----------------------------



#read serviceid
echo "============> Please input service id and type enter <============"
read user_input_service_id
echo "your input service id is "$user_input_service_id
echo "=================================================================="


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

#donload default application
cd ~ 
wget -O client.zip http://localhost:8080/Content/mydis.zip
unzip -o client.zip -d ./fview
rm -f client.zip

#write service id
rm -f  ./fview/dis/buildin/vers/service_id.ver
echo $user_input_service_id >> ./fview/dis/buildin/vers/service_id.ver

#start service
cd ~/fview/dis/
sh run.sh