import os
import getpass 
const_etcd_host = 'api.rsdis.meetingzen.cn'
const_etcd_port = 443
const_api_name_webcontent = 'rsdis-platform-web-content-management'
const_api_name_product = 'rsdis-platform-product-metadata'
const_api_name_resouce = 'rsdis-platform-system'
const_api_name_wechat = 'rsdis-platform-wechat'
const_client_web_server_root = 'http://127.0.0.1:8080'
const_service_id_name = 'service_id'
const_service_id = None
const_is_set_powerofboot_name="is_set_powerofboot"
const_is_set_powerofboot=None

current_app_id=None
def const_client_root():
    return os.getcwd()

def const_current_login_username():
    return getpass.getuser()
