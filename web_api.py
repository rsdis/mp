
from flask import Flask
from flask import request
from flask import abort, redirect, url_for
import json
from flask import make_response
import subprocess
import config
import uuid
import os
web_app_api = Flask(__name__)
# /opt/rsdis/config
# /opt/rsdis/apps
# /opt/rsdis/download
# /opt/rsdis/
# check local envirment working folder, nginx status, wifi status

# web server


@web_app_api.route("/api/contentInfos", methods=['GET'])
def contentInfos():
    data = json.load('%s/Content/AppContents/app_info.json' %
                     (config.const_client_root()))
    return data


@web_app_api.route("/api/productInfos", methods=['GET'])
def productInfos():
    data = json.load('%s/Content/ProductResources/data.js' %
                     (config.const_client_root()))
    return data


@web_app_api.route("/api/qrByUnique/<unique>", methods=['GET'])
def qrByUnique(unique):
    ret_obj = {
        'Id': str(uuid.uuid1()),
        'FileName': unique,
        'FileUrl': '%s/Content/QrCodeResources/%s' % (config.const_client_root(), unique),
        'HostUrl': '%s/Content/QrCodeResources/%s' % (config.const_client_web_server_root, unique)
    }
    return json.dumps(ret_obj)


@web_app_api.route("/api/qrInfos", methods=['GET'])
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


@web_app_api.route("/api/wifiSsids", methods=['GET'])
def wifiSsids():
    return


@web_app_api.route("/api/SetUpWifi/<ssid>/<pwd>", methods=['GET'])
def SetUpWifi(ssid, pwd):
    return


@web_app_api.route("/api/RegisterCode", methods=['GET'])
def RegisterCode():
    return
