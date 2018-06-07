import threading
import subprocess
import config

class chrome:
    def __init__(self):
        self.woker_thread = threading.Thread(target=self.__chrome_woker)
        self.start_url = None

#--start-fullscreen
    def __chrome_woker(self):
        while True:
            try:
                subprocess.call(
                    ['sudo','-i', '-u', config.const_current_login_username(), 'chromium-browser','--start-fullscreen', "--disk-cache-dir=/dev/null --disk-cache-size=1", '--app=' + self.start_url, '--disable-pinch'])
            except Exception as err:
                print(err)

    def start(self, url):
        self.start_url = url
        subprocess.call(['killall', 'chromium-browser'])
        self.woker_thread.start()

    def url_change(self, url):
        self.start_url = url

instance = chrome()
