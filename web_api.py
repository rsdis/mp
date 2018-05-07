
from flask import Flask
from flask import request
from flask import abort, redirect, url_for
import json
from flask import make_response
import subprocess
import config
import uuid
import os
import threading
import util
import config
import requests

instance = Flask(__name__)
# /opt/rsdis/config
# /opt/rsdis/apps
# /opt/rsdis/download
# /opt/rsdis/
# check local envirment working folder, nginx status, wifi status

# web server


@instance.route("/api/contentInfos", methods=['GET'])
def contentInfos():
    data = json.load('%s/Content/AppContents/app_info.json' %
                     (config.const_client_root()))
    return data


@instance.route("/api/productInfos", methods=['GET'])
def productInfos():
    data = json.load('%s/Content/ProductResources/data.js' %
                     (config.const_client_root()))
    return data


@instance.route("/api/qrByUnique/<unique>", methods=['GET'])
def qrByUnique(unique):
    ret_obj = {
        'Id': str(uuid.uuid1()),
        'FileName': unique,
        'FileUrl': '%s/Content/QrCodeResources/%s' % (config.const_client_root(), unique),
        'HostUrl': '%s/Content/QrCodeResources/%s' % (config.const_client_web_server_root, unique)
    }
    return json.dumps(ret_obj)


@instance.route("/api/qrInfos", methods=['GET'])
def qrInfos():
    ret = []
    for root, dirs, files in os.walk('%s/content/QrCodeResources/'):
        for name in files:
            item = {
                'Id': str(uuid.uuid1()),
                'FileName': name,
                'FileUrl': '%s/Content/QrCodeResources/%s' % (config.const_client_root(), name),
                'HostUrl': '%s/Content/QrCodeResources/%s' % (config.const_client_web_server_root, name)
            }
            ret.append(item)

    return json.dumps(ret)


@instance.route("/api/wifiSsids", methods=['GET'])
def wifiSsids():
    return


@instance.route("/api/SetUpWifi/<ssid>/<pwd>", methods=['GET'])
def SetUpWifi(ssid, pwd):
    return


@instance.route("/api/RegisterCode", methods=['GET'])
def RegisterCode():
    url = '%s/%s/WechatQrcode/CreateDeviceActivationQrcode'%(util.util_remote_service(config.const_api_name_wechat),config.const_api_name_wechat)
    data = util.get_cached_version('mc')
    rsp = requests.post(url,json=data)
    result ='data:image/png;base64,'+ rsp.json().replace('"','')
    return result

def woker():
    instance.run(threaded=True)

stater = threading.Thread(target=woker)