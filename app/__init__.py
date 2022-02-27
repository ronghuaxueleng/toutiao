# -*- coding: utf-8 -*
import json
from urllib.parse import urlencode

from flask import Flask, jsonify
from flask import render_template

import abb
import run_task
from abb import record
from run_task import profit_detail
from db.toutiao_jisu import Account, CommonParams, Abb

app = Flask(__name__)


@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html")


@app.route('/getToutiao')
def getToutiao():
    results = []
    accounts = Account.select()
    for idx, account in enumerate(accounts):
        headers = json.loads(account.headers)
        params = CommonParams.select().where(CommonParams.user_id == account.user_id).dicts().get()
        query = urlencode(params)
        result = profit_detail(headers, query, account, True)
        results.append(result)
    return jsonify(results)


@app.route('/getAbb')
def getAbb():
    items = Abb.select().dicts()
    results = []
    for item in items:
        nick = item.get('nick')
        header = item.get('header')
        phone = item.get('phone')
        money = item.get('money')
        header_json = json.loads(header)
        results.append(record(header_json, nick, money, phone, True))
    return jsonify(results)


@app.route('/pushabb')
def pushabb():
    abb.run_accout_task('record')
    return 'ok'


@app.route('/pushtoutiao')
def pushtoutiao():
    run_task.run_accout_task('profit_detail')
    return 'ok'


@app.route('/updateabb')
def updateabb():
    abb.run_accout_task('getperson')
    return 'ok'


@app.route('/updateabbstep')
def updateabbstep():
    abb.run_accout_task('updateabbstep')
    return 'ok'
