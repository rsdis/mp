import os
import config
import subprocess


def nginx_config_init():
    content = ''
    with open('%s/buildin/nginx.template' % (config.const_client_root()), 'r') as template_file:
        content = template_file.read()
    content = content.replace('##CONTENT_ROOT##', config.const_client_root())
    with open('%s/buildin/nginx.conf' % (config.const_client_root()), 'w') as template_file:
        content = template_file.write(content)


def nginx_reload_start():
    subprocess.call(['sudo','nginx', '-s', 'stop'])
    subprocess.call(['sudo','nginx', '-c', '%s/buildin/nginx.conf' %
                    (config.const_client_root())])

nginx_config_init()
nginx_reload_start()
