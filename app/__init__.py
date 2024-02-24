# -*- coding: utf-8 -*
import calendar
import datetime
import json
from urllib.parse import urlencode

from flask import Flask, jsonify
from flask import render_template
from peewee import fn

from run_task import profit_detail
from db.toutiao_jisu import Account, CommonParams
from liblibart.UserInfo import Account as LiblibAccount
from liblibart.Statistics import DownLoadImageStatistics, DownloadModelStatistics, RunStatistics

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


@app.route('/getLiblib')
def getLiblib():
    datas = []
    accounts = LiblibAccount.select()
    now = datetime.datetime.now()
    day = now.strftime('%d')
    this_month_middle = datetime.datetime(now.year, now.month, 15).strftime('%Y%m%d')
    this_month_start = datetime.datetime(now.year, now.month, 1).strftime('%Y%m%d') if int(day) <= 15 else this_month_middle
    this_month_end = datetime.datetime(now.year, now.month, calendar.monthrange(now.year, now.month)[1]).strftime('%Y%m%d') if int(day) > 15 else this_month_middle
    for idx, account in enumerate(accounts):
        nickname = account.nickname
        user_uuid = account.user_uuid
        downloadImageCount = fn.SUM(DownLoadImageStatistics.downloadImageCount).alias('downloadImageCount')
        downLoadImages = (DownLoadImageStatistics.select(downloadImageCount)
                          .where(DownLoadImageStatistics.user_uuid == user_uuid, DownLoadImageStatistics.day >= this_month_start, DownLoadImageStatistics.day <= this_month_end).get())
        downloadImageCounts = downLoadImages.downloadImageCount
        downloadModelCount = fn.SUM(DownloadModelStatistics.downloadModelCount).alias('downloadModelCount')
        downloadModels = (DownloadModelStatistics.select(downloadModelCount)
                          .where(DownloadModelStatistics.user_uuid == user_uuid, DownloadModelStatistics.day >= this_month_start, DownloadModelStatistics.day <= this_month_end).get())
        downloadModelCounts = downloadModels.downloadModelCount
        runCount = fn.SUM(RunStatistics.runCount).alias('runCount')
        runs = (RunStatistics.select(runCount)
                .where(RunStatistics.user_uuid == user_uuid, RunStatistics.day >= this_month_start, RunStatistics.day <= this_month_end).get())
        runCounts = runs.runCount
        datas.append({
            'nickname': nickname,
            'runCounts': 0 if runCounts is None else runCounts,
            'downloadModelCounts': 0 if downloadModelCounts is None else downloadModelCounts,
            'downloadImageCounts': 0 if downloadImageCounts is None else downloadImageCounts
        })
    result = {
        'datas': datas,
        'month_start': this_month_start,
        'month_end': this_month_end
    }
    return jsonify(result)
