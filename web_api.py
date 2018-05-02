
from flask import Flask
from flask import request
from flask import abort, redirect, url_for
import json
from flask import make_response
import subprocess
web_app_api = Flask(__name__)
# /opt/rsdis/config
# /opt/rsdis/apps
# /opt/rsdis/download
# /opt/rsdis/
# check local envirment working folder, nginx status, wifi status

# web server


def check_env_working_folder():
    return


def check_env_nginx():
    return


def task_apps_update():
    return



@web_app_api.route("/api/test", methods=['GET'])
def get_srv_access_token():
    return 'success'


def task_web_api_service():
    # service.web_app.run(debug=False)
    subprocess.call('notepad.exe')
    print('process down')
