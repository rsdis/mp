import config
import requests
import util
import re
import json
import threading
import subprocess
import os
import time

class content_updater:
    def __init__(self):
        self.thread = threading.Thread(target=self.__worker_thread)

    def __worker_thread(self):
        while True:
            try:
                self.update_qr_code()
                self.update_product()
                self.update_apps()
                time.sleep(60*60)
            except Exception as err:
                print(err)
    def get_service_id_from_remote(self,session_key):
        url = '%s/%s/Device/IsActive?machineCode=%s'%(util.util_remote_service(config.const_api_name_resouce),config.const_api_name_resouce,session_key)
        print(url)
        resp = requests.get(url)
        if resp.status_code == 200:
            result = resp.json()
            return result
        else:
            return None

    def get_device_info(self):
        device_info_url = '%s/%s/Device/GetDetail?id=%s' % (util.util_remote_service(
            config.const_api_name_resouce), config.const_api_name_resouce, config.const_service_id)
        device_info = requests.get(device_info_url).json()
        return device_info

    def get_default_start(self):
        file_path = '%s/Content/AppContents/app_info.json' %(config.const_client_root())
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as data_file:
                return json.loads(data_file.read(file_path))
                #default
        else:
            return None

    def update_qr_code(self):
        if config.const_service_id is None:
            return
        # Qrcode
        device_info = self.get_device_info()
        # QR version
        device_info_version = int(re.findall(
            r'\b\d.*\d\b', device_info['wechat_qrcode_zip_url'])[0])
        cached_ver = -1
        if util.get_cached_version('QR') is not None:
            cached_ver = int(util.get_cached_version('QR'))
        # download to update
        if device_info_version > cached_ver:
            util.download_extract_target(
                device_info['wechat_qrcode_zip_url'], '%s/Content/QrCodeResources' % (config.const_client_root()), True)
            util.set_cached_version('QR', device_info_version)
            print(device_info)

    def update_product(self):
        device_info = self.get_device_info()
        if util.get_cached_version('product') is not None:
            if device_info.get('need_update_content') is None:
                return
            if device_info.get('need_update_content') == False:
                return

        product_info_url = '%s/%s/Product/GetAll' % (util.util_remote_service(
            config.const_api_name_product), config.const_api_name_product)
        print(product_info_url)
        product_info_json = requests.get(product_info_url).json()
        product_info_text = json.dumps(product_info_json)
        #print(product_info_json)
        # download image to target folder
        for image in product_info_json['DownloadList']:
            try:
                util.download_file_to_target(
                    image, '%s/Content/ProductResources/' % (config.const_client_root()), True)
            except Exception as err:
                print(err)
        # save data file to target folder
        with open('%s/Content/ProductResources/data.json' %
                  (config.const_client_root()), 'w+', encoding='utf-8') as data_file:
            data_file.write(product_info_text)

        # tell server product has been updated
        product_update_done_url = '%s/%s/Device/StopUpdateContent?deviceId=%s' % (util.util_remote_service(
            config.const_api_name_resouce), config.const_api_name_resouce, config.const_service_id)
        requests.post(product_update_done_url)

    def update_apps(self):
        #get app info url
        app_url_info = '%s/%s/AppContent/getNewestVersionOfZipBy?appKey=%s' % (util.util_remote_service(
            config.const_api_name_webcontent), config.const_api_name_webcontent, config.const_service_id)
        #get app entitys
        apps_info = requests.get(app_url_info).json()
        #check app is any version different
        for app in apps_info:
            local_ver = util.get_cached_version('app_'+str(app['appId']))
            if local_ver is None or local_ver != app['version']:
                target_dir = '%s/Content/AppContents/'%(config.const_client_root())
                target_dir = target_dir +str(app['appId'])
                subprocess.call(['mkdir',target_dir])
                # perform update
                util.download_extract_target(
                    app['zipPath'], target_dir, True)
                util.set_cached_version('app_'+str(app['appId']),str(app['version']))
        #save data file
        with open('%s/Content/AppContents/app_info.json' %
                  (config.const_client_root()), 'w+', encoding='utf-8') as data_file:
            data_file.write(json.dumps(apps_info))

    def start(self):
        self.thread.start()

instance = content_updater()