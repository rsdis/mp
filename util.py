import etcd
import config
import os
import subprocess
import uuid


def util_remote_service(service_name):
    ectd_client = etcd.Client(
        host=config.const_etcd_host, port=config.const_etcd_port, version_prefix='/v2')
    service_folder = ectd_client.get(
        '/product/runtime/webapi/external/'+service_name)
    if service_folder._children.__len__() > 0:
        return service_folder._children[0]['value']
    else:
        return None


def get_cached_version(resource):
    ver = '%s/buildin/vers/%s.ver' % (config.const_client_root, resource)
    if os.path.exists(ver):
        with open(ver, 'r') as content_file:
            content = content_file.read()
        return content
    else:
        return None


def set_cached_version(resource, value):
    ver = '%s/buildin/vers/%s.ver' % (config.const_client_root, resource)
    if os.path.exists(ver):
        os.remove(ver)
    with open(ver, 'w+') as content_file:
        content_file.write(str(value))


def download_extract_target(download_uri, target_dir, is_overwirte):
    tmp_file = '%s/buildin/tmp/%s' % (config.const_client_root,
                                      str(uuid.uuid1()))
    if is_overwirte == True:
        subprocess.call(['rm', '-f', target_dir + '*'])
    subprocess.call(['curl', '-o', tmp_file, download_uri])
    subprocess.call(['unzip', '-o', tmp_file, '-d', target_dir])
    subprocess.call(['rm', '-f', tmp_file])

def download_file_to_target(download_uri, target_dir, is_overwirte):
    tmp_file = '%s/buildin/tmp/%s' % (config.const_client_root,
                                      str(uuid.uuid1()))
    if is_overwirte == True:
        subprocess.call(['rm', '-f', target_dir + '*'])
    subprocess.call(['curl', '-o', tmp_file, download_uri])
    subprocess.call(['unzip', '-o', tmp_file, '-d', target_dir])
    subprocess.call(['rm', '-f', tmp_file])