import util
import subprocess
import config
import threading
import os
import time

class log_uploader:
    def __init__(self):
        self.thread = threading.Thread(target=self.__worker_thread)

    def __worker_thread(self):
        while True:
            try:
                dr = '%s/buildin/logs'%(config.const_client_root())
                current_log_prefix = 'service_log_' + util.current_log_file
                for root, dirs, files in os.walk(dr, topdown=False):
                    for name in files:
                        if name.startswith(current_log_prefix) == False:
                            self.upload_file(name)
                time.sleep(60)
            except Exception as err:
                util.log_error('downloader',err)
                time.sleep(60)

    def upload_file(self,file_name):
        full_log_path = "%s/buildin/logs/%s"%(config.const_client_root(),file_name)
        target_file_name = "%s_%s"%(config.const_service_id,file_name)
        cmd = "azcopy --source " + full_log_path + " --destination https://rsdisprd.blob.core.chinacloudapi.cn/dis-client-log/" + target_file_name + " --dest-key 'cPluFpf91Uw/C+8QtNNN8Y669tZrFDiAr3NQTEbe6aWdHvq7LgRXUThxjdbAyPr4C2IKbxr4WYd0/lsmnB751g==' --quiet"
        subprocess.call([cmd],shell=True)
        subprocess.call(['rm -f ' + full_log_path ],shell=True)

    def start(self):
        self.thread.start()


instance = log_uploader()