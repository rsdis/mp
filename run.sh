#!/bin/bash

#set auto lock false
gsettings set org.gnome.desktop.screensaver lock-enabled false
gsettings set org.gnome.desktop.screensaver lock-delay 99999999
gsettings set org.gnome.desktop.screensaver idle-activation-enabled false
#disable power saving
sudo xset -dpms 

#perform update

service_id_path=~/fview/dis/buildin/vers/service_id.ver
client_ver_path=~/fview/dis/buildin/vers/client.ver

service_id=''
client_ver=''

if [ -f $service_id_path ]
then 
    echo 'service id existes'
    service_id=`cat ~/fview/dis/buildin/vers/service_id.ver`
else
    echo 'service id not existes'
    service_id='none'
fi


if [ -f $client_ver_path ]
then 
    echo 'client ver existes'
    client_ver=`cat ~/fview/dis/buildin/vers/client.ver`
else
    echo 'client ver not existes'
    client_ver='empty client ver'
fi

#pick up remote version line
query_version="curl -s http://rsdisprd.blob.core.chinacloudapi.cn/install/package_update_index/client_ver.txt | grep "$service_id
version_line=$(eval $query_version)

echo 'get remote line the version command is : '$version_line
i=0
for el in $version_line
do
    if [ $i -eq 1 ];then
        client_target_ver=$el
    fi

    if [ $i -eq 2 ];then
        target_version_download_url=$el
    fi
    i=$(( $i + 1 ))
done

echo 'target version is : '$client_target_ver
echo 'target download url is : '$target_version_download_url

#special url

if [ "$client_ver" != "$client_target_ver" ];then
echo 'perform updating'
cd ~ 
wget -O client.zip $target_version_download_url
unzip -o client.zip -d ./fview
rm -f client.zip
rm -f $client_ver_path
echo "$client_target_ver" >>  $client_ver_path
fi

#set auto start
started=`grep "fview" ~/.profile`
echo $started

if [ -z $started ];then
    cmd='sh ~/fview/dis/run.sh'
    echo $cmd >> ~/.profile
fi


#start application
cd ~/fview/dis/
nohup python3.6 run.py &