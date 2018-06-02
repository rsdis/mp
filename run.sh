#!/bin/bash

#go to the working folder
cd ~/dis

service_id_path=~/dis/buildin/vers/service_id.ver
client_ver_path=~/dis/buildin/vers/client.ver

service_id=''
client_ver=''

if [ -f $service_id_path ]
then 
    echo 'service id existes'
    service_id=`cat ~/dis/buildin/vers/service_id.ver`
else
    echo 'service id not existes'
    service_id='none'
fi


if [ -f $client_ver_path ]
then 
    echo 'client ver existes'
    client_ver=`cat ~/dis/buildin/vers/client.ver`
else
    echo 'client ver not existes'
    client_ver='empty client ver'
fi

tmp="curl -s http://localhost:8080/Content/content.json|grep  ct001"
echo $tmp
remote=`$tmp`

echo $remote
echo $service_id
echo $client_ver


#special url


#set auto start
running_folder=`pwd`
started=`grep "run.sh" ~/.profile`
echo $started
if [$started == ""]
then
    cmd='sh '$running_folder'/dis/run.sh'
    echo $cmd >> ~/.profile
fi

#start progra
#python3.6 run.py