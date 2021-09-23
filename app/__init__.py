# -*- coding: utf-8 -*
import json
from urllib.parse import urlencode

from flask import Flask, jsonify
from flask import render_template

from abb import record
from run_task import profit_detail
from toutiao.db import Account, CommonParams, Abb

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
        header_json = json.loads(header)
        results.append(record(header_json, nick, True))
    return jsonify(results)
