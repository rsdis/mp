from urllib import request
import util
import config
import chrome
import subprocess



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
        cmd = subprocess.Popen(['nmcli','device','wifi','list'],stdout=subprocess.PIPE)
        output = cmd.communicate()[0].decode('utf-8')
        result = []
        is_header = True
        for item in output.split('\n'):
            if is_header is not True:
                    subitems = item.split()
                    if len(subitems) > 5:
                        if subitems[0] == '*':
                            wifi_object={
                                'SSID' : subitems[1],
                                'wlanSignalQuality' : subitems[7]
                            }
                            result.append(wifi_object)
                        else:
                            wifi_object={
                                'SSID' : subitems[0],
                                'wlanSignalQuality' : subitems[6]
                            }
                            result.append(wifi_object)
            else:
                is_header=False
        return result

    def connect_wifi(self, ssid, password):
        cmd = subprocess.Popen(['sudo','nmcli','device','wifi','connect',ssid,'password',password],stdout=subprocess.PIPE)
        output = cmd.communicate()[0].decode('utf-8')
        if 'Error' in output:
            return False
        else:
            return True

checker = wifi_checker()
checker.connect_wifi('ChinaNet-Cixb-5G','a4g2eqlw')