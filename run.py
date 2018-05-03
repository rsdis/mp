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

# start nginx service
nginx.nginx_config_init()
nginx.nginx_reload_start()

# block to start web api
web_api.web_app_api.run(threaded=True)

# start web socket service
web_socket_service = web_socket.web_socket_server(9999)
web_socket_service.start()


# local wifi check
wifi_checker = wifi_checker.wifi_checker()
wifi_checker.start_check_wifi()

# content_update_thread start
cnt_update = downloader.content_updater()
# if local is empty, will block to download
cnt_update.start()

# lanuch chrome
chrome_instance = chrome.chrome()
chrome_instance.start('')
