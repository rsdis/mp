import chrome
import config
import downloader
import util
import nginx
import web_api
from threading import Thread
import time
import subprocess
import web_socket
import wifi_checker
import time
import uuid
import threading
import json
import time

util.log_info("main",'service starting')
# init machine code
machine_code = util.get_cached_version('mc')
util.log_info("main",'get machine code')
if machine_code is None:
    util.log_info("main",'machine code is empty, create it.')
    util.set_cached_version('mc',str(uuid.uuid1()).replace('-',''))
machine_code = util.get_cached_version('mc')

# start nginx service
nginx.nginx_config_init()
nginx.nginx_reload_start()
util.log_info("main",'nginx web server started.')

# start web api service
web_api.stater.start()
util.log_info("main",'web api server started.')


# start web socket service
web_socket.instance.start()
util.log_info("main",'web socket server started.')


time.sleep(5)
util.log_info("main",'waiting 5 secs for server fullly inited.')



#check if service id is empty, and wifi is not available, ask to setup wifi
config.const_service_id = util.get_cached_version(config.const_service_id_name)
if config.const_service_id is None:
    if wifi_checker.instance.is_network_available() == False:
        chrome.instance.start('%s/Content/wifi.html'%(config.const_client_web_server_root))
        while wifi_checker.instance.is_network_available() == False:
            time.sleep(1)

#check is service id is empty, ask user to register with mc code
util.log_info("main",'checking service id existed')
if config.const_service_id is None:
    util.log_info("main",'service id is empty,will show register page and waiting user binding')
    chrome.instance.start('%s/Content/register.html'%(config.const_client_web_server_root))
    temp_serviceid = downloader.instance.get_service_id_from_remote(machine_code)
    while temp_serviceid is None:
        try:
            util.log_info("main",'check status if the machine code related device has been binded')
            time.sleep(1)
            temp_serviceid = downloader.instance.get_service_id_from_remote(machine_code)
            temp_serviceid='ct001'
        except Exception as err:
            util.log_error('main',err)
    util.log_info("main",'service id picked from server end, write it into local cache')
    config.const_service_id = temp_serviceid
    util.set_cached_version(config.const_service_id_name,temp_serviceid)

#start default page
util.log_info("main",'start chrom process with default page')
chrome.instance.start('%s/Content/default.html'%(config.const_client_web_server_root))
#start content updater

downloader.instance.start()
util.log_info("main",'started apps,products,qrcode download and updating process.')

#reload for default start
time.sleep(5)
default_app,start_path = downloader.instance.get_default_start()
util.log_info("main",'get default apps')
if default_app is not None:
    msg = {
        'MessageType':0,
        'MessageData':start_path
    }
    web_socket.instance.send(json.dumps(msg))
    
quite = ''
while quite != 'q':
    quite = input()