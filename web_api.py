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
import serial_port
import wifi_checker
import time
instance = Flask(__name__)
# /opt/rsdis/config
# /opt/rsdis/apps
# /opt/rsdis/download
# /opt/rsdis/
# check local envirment working folder, nginx status, wifi status

# web server


@instance.route("/api/contentInfos", methods=['GET'])
def contentInfos():
    util.log_info('web_api_server','recieve call for contentInfos')
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
    util.log_info('web_api_server','recieve call for productInfos')
    return util.get_cached_version('product_info')


@instance.route("/api/getPowerSettingModel", methods=['GET'])
def getCurrentPowerSettingModel():
    util.log_info('web_api_server','recieve current mdoel of power setting')
    model = serial_port.instance.getMode()
    if model == "MODELD":
        openTime=serial_port.instance.getDailyOpenTime()
        closeTime=serial_port.instance.getDailyCloseTIme()
        ret_obj={
            model:"MODELD",
            "opemTime":openTime,
            "closeTime":closeTime,
        }
        return json.dumps(ret_obj)
    ret_obj={
        model:"MODEM"
    }
    return json.dumps(ret_obj)
    # ret_obj={
    #     "model":"MODED",
    #     "opemTime":"08:05",
    #     "closeTime":"22:05"
    # }
    # return json.dumps(ret_obj) 
    #MODEM/MODED
    #return 'MODED'

@instance.route("/api/qrByUnique/<unique>", methods=['GET'])
def qrByUnique(unique):
    util.log_info('web_api_server','recieve call for qrByUnique')
    ret_obj = {
        'Id': str(uuid.uuid1()),
        'FileName': unique,
        'FileUrl': '%s/Content/QrCodeResources/%s' % (config.const_client_root(), unique),
        'HostUrl': '%s/Content/QrCodeResources/%s' % (config.const_client_web_server_root, unique)
    }
    return json.dumps(ret_obj)


@instance.route("/api/qrInfos", methods=['GET'])
def qrInfos():
    util.log_info('web_api_server','recieve call for qrInfos')
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
    wifis=wifi_checker.instance.scan_wifi_list()
    return json.dumps(wifis)


@instance.route("/api/SetUpWifi/<ssid>/<pwd>", methods=['GET'])
def SetUpWifi(ssid, pwd):
    if wifi_checker.instance.connect_wifi(ssid,pwd):
        return '连接成功'
    return '连接失败'


@instance.route("/api/RegisterCode", methods=['GET'])
def RegisterCode():
    util.log_info('web_api_server','recieve call for register code')
    url = '%s/%s/WechatQrcode/CreateDeviceActivationQrcode'%(util.util_remote_service(config.const_api_name_wechat),config.const_api_name_wechat)
    data = util.get_cached_version('mc')
    rsp = requests.post(url,json=data)
    result ='data:image/png;base64,'+ rsp.json().replace('"','')
    return result

@instance.route("/api/post_msg", methods=['POST'])
def post_msg():
    util.log_info('web_api_server','recieve call for post message')
    ty=request.form['type']
    if ty == 'shutdown':
        subprocess.call('sudo','halt')

    if ty == 'reboot':
        subprocess.call('sudo','reboot')

    if ty == 'setVolumn':
        volumn=request.form['volumn']
        subprocess.Popen(['amixer','set','Master',volumn],stdout=subprocess.PIPE)

    if ty == 'setBootTimes':
        model=request.form['model']
        if model=='daily':
            openTime=request.form['openTime']+':00'
            closeTime=request.form['closeTime']+':00'
            if not serial_port.instance.setDailyTIme(openTime,closeTime):
                return 'fail'

        if model=='manual':
            return_val = serial_port.instance.setModeM()
            time.sleep(10)
            util.log_info("api return serial port", return_val)
            if return_val == False:
                return 'fail'
            else:
                return 'success'

    if ty == 'currAppId':
       config.current_app_id=request.form['appId']
    return 'ok'


def woker():
    instance.run()

stater = threading.Thread(target=woker)