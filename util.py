import etcd
import config


def get_remote_service_addr_by_name(service_name):
    ectd_client = etcd.Client(
        host=config.const_etcd_host, port=config.const_etcd_port, version_prefix='/v2')
    service_folder = ectd_client.get(
        '/product/runtime/webapi/external/'+service_name)
    if service_folder._children.__len__() > 0:
        return service_folder._children[0]['value']
    else:
        return None


test = get_remote_service_addr_by_name(config.const_api_name_product)
