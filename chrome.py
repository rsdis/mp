import threading
import subprocess


class chrome_demo:
    def __init__(self):
        self.woker_thread = threading.Thread(target=self.woker_thread)
        self.start_url = None

    def __chrome_woker(self):
        subprocess.call([''])

    def url(slef,url):
        slef.start_url = url
        t = threading.Thread(target=self.woker_thread)
        t.
        if self.woker_thread