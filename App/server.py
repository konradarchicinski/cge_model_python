#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

from bottle import Bottle, route, run, template, get, post, debug, static_file, request, redirect, response
import time
import random
import string
import logging
import logging.handlers

log = logging.getLogger('bottle')
log.setLevel('INFO')
h = logging.handlers.TimedRotatingFileHandler(
    'logs/nlog', when='midnight', backupCount=9999)
f = logging.Formatter('%(asctime)s %(levelname)-8s %(message)s')
h.setFormatter(f)
log.addHandler(h)


secretKey = "SDMDSIUDSFYODS&TTFS987f9ds7f8sd6DFOUFYWE&FY"


from users import users

app = Bottle()


@app.route('/static/:path#.+#', name='static')
def static(path):
    return static_file(path, root='./static')


def checkAuth():
    loginName = request.get_cookie("user", secret=secretKey)
    randStr = request.get_cookie("randStr", secret=secretKey)
    log.info(str(loginName) + ' ' + request.method + ' ' +
             request.url + ' ' + request.environ.get('REMOTE_ADDR'))
    if (loginName in users) and (users[loginName].get("randStr", "") == randStr) and (users[loginName]["loggedIn"] == True) and (time.time() - users[loginName]["lastSeen"] < 3600):
        users[loginName]["lastSeen"] = time.time()
        return loginName
    return redirect('/login')


@app.route('/login')
@app.route('/login/')
@app.route('/login', method='POST')
def login():
    loginName = request.forms.get('login_name', default=False)
    password = request.forms.get('password', default=False)
    randStr = ''.join(random.choice(
        string.ascii_uppercase + string.digits) for _ in range(18))
    log.info(str(loginName) + ' ' + request.method + ' ' +
             request.url + ' ' + request.environ.get('REMOTE_ADDR'))
    if (loginName in users) and users[loginName]["password"] == password:
        response.set_cookie("user", loginName, secret=secretKey)
        response.set_cookie("randStr", randStr, secret=secretKey)
        users[loginName]["loggedIn"] = True
        users[loginName]["randStr"] = randStr
        users[loginName]["lastSeen"] = time.time()
        
        redirect('/index')
        return True
    else:
        return template('login')
    return template('login')


@app.route('/')
@app.route('/index')
@app.route('/index/')
@app.route('/index/<message>')
def index(message=''):
    loginName = checkAuth()
    messDict = {'error': "Something went wrong",
                'ok': "Everything is ok."}
    return template('index', message=messDict.get(message, ""), loginName=loginName)

app.run(host='localhost', port=63700, reloader=False, debug=False)
