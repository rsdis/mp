import chrome
import config
import downloader
import environment
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
# init machine code
machine_code = util.get_cached_version('mc')
if machine_code is None:
    util.set_cached_version('mc',str(uuid.uuid1()))
machine_code = util.get_cached_version('mc')

# start nginx service
nginx.nginx_config_init()
nginx.nginx_reload_start()

# start web api service
web_api.instance.run(threaded=True)

# start web socket service
web_socket.instance.start()

#check if service id is empty, and wifi is not available, ask to setup wifi
config.const_service_id = util.get_cached_version(config.const_service_id_name)
if config.const_service_id is None:
    if wifi_checker.checker.is_network_available() == False:
        chrome.instance.start('%s/Content/wifi.html'%(config.const_client_web_server_root))
        while wifi_checker.checker.is_network_available() == False:
            time.sleep(1)

#check is service id is empty, ask user to register with mc code
if config.const_service_id is None:
    chrome.chrome_instance.start('%s/Content/register.html'%(config.const_client_web_server_root))
    temp_serviceid = downloader.updater.get_service_id_from_remote(machine_code)
    while temp_serviceid is None or temp_serviceid == '':
        time.sleep(1)
        temp_serviceid = downloader.updater.get_service_id_from_remote(machine_code)
    config.const_service_id = temp_serviceid
    util.set_cached_version(config.const_service_id_name,temp_serviceid)

#start default page
chrome.instance.start('%s/Content/default.html'%(config.const_client_web_server_root))
#start content updater
downloader.instance.start()
time.sleep(5)

#reload for default start
default_app = downloader.updater_instance.get_default_start()
if default_app is not None
    msg = 
    {
        'MessageType':0,
        'MessageData':StartPath['StartPath']
    }
    web_socket.instance.send(json.dump(msg))

wait_event = threading.Event()
wait_event.wait()