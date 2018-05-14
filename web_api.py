from flask import *
import subprocess
import config
import uuid
import os
import threading
import util
import config
import requests
import json
instance = Flask(__name__)
# /opt/rsdis/config
# /opt/rsdis/apps
# /opt/rsdis/download
# /opt/rsdis/
# check local envirment working folder, nginx status, wifi status

# web server


@instance.route("/api/contentInfos", methods=['GET'])
def contentInfos():
    applist = []
    dr = '%s/buildin/vers'%(config.const_client_root())
    for root, dirs, files in os.walk(dr, topdown=False):
        for name in files:
            if name.startswith('rv_'):
                ver_name = name.replace('.ver','')
                applist.append(json.loads(util.get_cached_version(ver_name)))
    return jsonify(applist)

@instance.route("/api/productInfos", methods=['GET'])
def productInfos():
    return jsonify(util.get_cached_version('product_info'))


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

@instance.route("/api/post_msg", methods=['POST'])
def post_msg():
    form = request.get_json()
    if form is not None:
        ty = form['type']
        if ty == 'shutdown':
            subprocess.call('sudo','halt')
        if ty == 'reboot':
            subprocess.call('sudo','reboot')
    return None


def woker():
    instance.run()

stater = threading.Thread(target=woker)