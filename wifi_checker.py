import wifi
from urllib import request
import util
import config
import chrome


class wifi_checker:
    def start_check_wifi(self):
        if self.is_network_init == True:
            return
        if self.is_network_available == True:
            return
        chrome.chrome_instance.start(
            '%s/content/wifi.html' % (config.const_client_web_server_root))
        return

    def is_network_available(self):
        try:
            response = request.urlopen('http://www.baidu.com', timeout=20)
            return True
        except request.URLError as err:
            return False
        return False

    def is_network_init(self):
        ver = util.get_cached_version('wifi')
        if ver is None:
            return False
        else:
            return True

    def scan_wifi_list(self):
        wifi.Cell.all('wlan0')

    def connect_wifi(self, name, password):
        scheme = wifi.Scheme.for_cell('wlan0', name, '', password)
        scheme.save()
        scheme.activate()


c = wifi_checker()
f = c.is_network_available()
