import threading
import subprocess


class chrome:
    def __init__(self):
        self.woker_thread = threading.Thread(target=self.__chrome_woker)
        self.start_url = None

    def __chrome_woker(self):
        while True:
            subprocess.call(
                ['chromium-browser', '--start-fullscreen', '--app=' + self.start_url])

    def start(self, url):
        self.start_url = url
        subprocess.call(['pkill', 'chromium-browse'])
        self.woker_thread.start()


instance = chrome()
