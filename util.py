import etcd
import config
import os
import subprocess
import uuid
import requests
import logging


def util_remote_service(service_name):
    ectd_client = etcd.Client(
        host=config.const_etcd_host, port=config.const_etcd_port, version_prefix='/v2',protocol='https')
    service_folder = ectd_client.get(
        '/product/runtime/webapi/external/'+service_name)
    if service_folder._children.__len__() > 0:
        return service_folder._children[0]['value']
    else:
        return None


def get_cached_version(resource):
    ver = '%s/buildin/vers/%s.ver' % (config.const_client_root(), resource)
    if os.path.exists(ver):
        with open(ver, 'r') as content_file:
            content = content_file.read()
        return content
    else:
        return None


def set_cached_version(resource, value):
    ver = '%s/buildin/vers/%s.ver' % (config.const_client_root(), resource)
    if os.path.exists(ver):
        os.remove(ver)
    with open(ver, 'w+') as content_file:
        content_file.write(str(value))


def download_extract_target(download_uri, target_dir, is_overwirte):
    tmp_file = '%s/buildin/tmp/%s' % (config.const_client_root(),
                                      str(uuid.uuid1()))
    if is_overwirte == True:
        path = target_dir + '/*'
        subprocess.call(['rm', '-f',path])
    subprocess.call(['curl', '-o', tmp_file, download_uri])
    subprocess.call(['unzip', '-o', tmp_file, '-d', target_dir])
    subprocess.call(['rm', '-f', tmp_file])
    
def download_extract_target_cut(download_uri, target_dir, is_overwirte):
    tmp_file = '%s/buildin/tmp/%s' % (config.const_client_root(),
                                      str(uuid.uuid1()))
    subprocess.call(['curl', '-o', tmp_file, download_uri])
    subprocess.call(['rm -rf ' + target_dir+'/*'],shell=True)
    subprocess.call(['unzip', '-o', tmp_file, '-d', target_dir])
    subprocess.call(['mv ' + target_dir + '/*/*' + ' '+target_dir],shell=True)
    subprocess.call(['rm', '-f', tmp_file])

def download_file_to_target(download_uri, target_dir, is_overwirte):
    subprocess.call(['cd ' + target_dir + ' ; curl -O ' + download_uri],shell=True)


def find_file(name, path):
    for root, dirs, files in os.walk(path):
        if name in files:
            return os.path.join(root, name)

logging.basicConfig(level=logging.INFO,
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                datefmt='%a, %d %b %Y %H:%M:%S',
                filename='buildin/logs/service_log.log',
                filemode='w')

console = logging.StreamHandler()
console.setLevel(logging.INFO)
formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
console.setFormatter(formatter)
logging.getLogger('').addHandler(console)

def log_info(sender,message):
    logging.info('%s==>%s'%(sender,message))
def log_error(sender,message):
    logging.error('%s==>%s'%(sender,message))
    