
from flask import Flask
from flask import request
from flask import abort, redirect, url_for
import MySQLdb
from DBUtils.PooledDB import PooledDB
import json
from functools import wraps
from flask import make_response
import redis
# web server
web_app = Flask(__name__)
# database connection
db_pool = PooledDB(MySQLdb, 5, host="59.110.220.49", user="root",
                   passwd="Niuniu812", db="we_sell", charset="utf8")
redis_pool = redis.ConnectionPool(host='127.0.0.1', port=6379, db=0)
redis_client = redis.Redis(connection_pool=redis_pool)
# cross domin define


def allow_cross_domain(fun):
    @wraps(fun)
    def wrapper_fun(*args, **kwargs):
        ssid = request.cookies.get('ssid')
        if ssid == None:
            abort(401)
        else:
            rst = make_response(fun(*args, **kwargs))
            rst.headers['Access-Control-Allow-Origin'] = '*'
            rst.headers['Access-Control-Allow-Methods'] = 'PUT,GET,POST,DELETE'
            allow_headers = "Referer,Accept,Origin,User-Agent"
            rst.headers['Access-Control-Allow-Headers'] = allow_headers
            return rst
    return wrapper_fun


allow_cross_domain = allow_cross_domain
