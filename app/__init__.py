# -*- coding: utf-8 -*
import json
from urllib.parse import urlencode

from flask import Flask, jsonify
from flask import render_template

from db.toutiao_jisu import Account, CommonParams
from run_task import profit_detail

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