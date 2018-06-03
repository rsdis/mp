import threading
import subprocess


class chrome:
    def __init__(self):
        self.woker_thread = threading.Thread(target=self.__chrome_woker)
        self.start_url = None

#--start-fullscreen
    def __chrome_woker(self):
        while True:
            try:
                subprocess.call(
                    ['chromium-browser', '', '--app=' + self.start_url])
            except Exception as err:
                print(err)

    def start(self, url):
        self.start_url = url
        subprocess.call(['pkill', 'chromium-browse'])
        self.woker_thread.start()


instance = chrome()
