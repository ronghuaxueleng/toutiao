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
from liblibart.SUserInfo import Account as ShakkerAccount
from liblibart.Statistics import DownLoadImageStatistics, DownloadModelStatistics, RunStatistics
from liblibart.SStatistics import DownLoadImageStatistics as SDownLoadImageStatistics, DownloadModelStatistics as SDownloadModelStatistics, RunStatistics as SRunStatistics


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
    this_period_start = datetime.datetime(now.year, now.month, 1).strftime('%Y%m%d')
    this_period_end = datetime.datetime(now.year, now.month, calendar.monthrange(now.year, now.month)[1]).strftime('%Y%m%d')
    for idx, account in enumerate(accounts):
        nickname = account.nickname
        user_uuid = account.user_uuid
        downloadImageCount = fn.SUM(DownLoadImageStatistics.downloadImageCount).alias('downloadImageCount')
        downLoadImages = (DownLoadImageStatistics.select(downloadImageCount)
                          .where(DownLoadImageStatistics.user_uuid == user_uuid, DownLoadImageStatistics.day >= this_period_start, DownLoadImageStatistics.day <= this_period_end).get())
        downloadImageCounts = downLoadImages.downloadImageCount
        downloadModelCount = fn.SUM(DownloadModelStatistics.downloadModelCount).alias('downloadModelCount')
        downloadModels = (DownloadModelStatistics.select(downloadModelCount)
                          .where(DownloadModelStatistics.user_uuid == user_uuid, DownloadModelStatistics.day >= this_period_start, DownloadModelStatistics.day <= this_period_end).get())
        downloadModelCounts = downloadModels.downloadModelCount
        runCount = fn.SUM(RunStatistics.runCount).alias('runCount')
        runs = (RunStatistics.select(runCount)
                .where(RunStatistics.user_uuid == user_uuid, RunStatistics.day >= this_period_start, RunStatistics.day <= this_period_end).get())
        runCounts = runs.runCount
        data = {
            'nickname': nickname,
            'runCounts': 0 if runCounts is None else runCounts,
            'downloadModelCounts': 0 if downloadModelCounts is None else downloadModelCounts,
            'downloadImageCounts': 0 if downloadImageCounts is None else downloadImageCounts
        }
        if (data.get('runCounts') != 0 and data.get('downloadImageCounts') != 0) or data.get('downloadModelCounts') != 0:
            datas.append(data)
    result = {
        'datas': datas,
        'month_start': this_period_start,
        'month_end': this_period_end
    }
    return jsonify(result)

@app.route('/getLastLiblib')
def getLastLiblib():
    datas = []
    accounts = LiblibAccount.select()
    now = datetime.datetime.now()
    last = now.replace(day=1)
    last_month = last.month - 1
    last_period_start = datetime.datetime(now.year, last_month, 1).strftime('%Y%m%d')
    last_period_end = datetime.datetime(now.year, last_month, calendar.monthrange(now.year, last_month)[1]).strftime('%Y%m%d')
    for idx, account in enumerate(accounts):
        nickname = account.nickname
        user_uuid = account.user_uuid
        downloadImageCount = fn.SUM(DownLoadImageStatistics.downloadImageCount).alias('downloadImageCount')
        downLoadImages = (DownLoadImageStatistics.select(downloadImageCount)
                          .where(DownLoadImageStatistics.user_uuid == user_uuid, DownLoadImageStatistics.day >= last_period_start, DownLoadImageStatistics.day <= last_period_end).get())
        downloadImageCounts = downLoadImages.downloadImageCount
        downloadModelCount = fn.SUM(DownloadModelStatistics.downloadModelCount).alias('downloadModelCount')
        downloadModels = (DownloadModelStatistics.select(downloadModelCount)
                          .where(DownloadModelStatistics.user_uuid == user_uuid, DownloadModelStatistics.day >= last_period_start, DownloadModelStatistics.day <= last_period_end).get())
        downloadModelCounts = downloadModels.downloadModelCount
        runCount = fn.SUM(RunStatistics.runCount).alias('runCount')
        runs = (RunStatistics.select(runCount)
                .where(RunStatistics.user_uuid == user_uuid, RunStatistics.day >= last_period_start, RunStatistics.day <= last_period_end).get())
        runCounts = runs.runCount
        data = {
            'nickname': nickname,
            'runCounts': 0 if runCounts is None else runCounts,
            'downloadModelCounts': 0 if downloadModelCounts is None else downloadModelCounts,
            'downloadImageCounts': 0 if downloadImageCounts is None else downloadImageCounts
        }
        if (data.get('runCounts') != 0 and data.get('downloadImageCounts') != 0) or data.get('downloadModelCounts') != 0:
            datas.append(data)
    result = {
        'datas': datas,
        'month_start': last_period_start,
        'month_end': last_period_end
    }
    return jsonify(result)

@app.route('/getShakker')
def getShakker():
    datas = []
    accounts = ShakkerAccount.select()
    now = datetime.datetime.now()
    this_period_start = datetime.datetime(now.year, now.month, 1).strftime('%Y%m%d')
    this_period_end = datetime.datetime(now.year, now.month, calendar.monthrange(now.year, now.month)[1]).strftime('%Y%m%d')
    for idx, account in enumerate(accounts):
        nickname = account.nickname
        user_uuid = account.user_uuid
        downloadImageCount = fn.SUM(SDownLoadImageStatistics.downloadImageCount).alias('downloadImageCount')
        downLoadImages = (SDownLoadImageStatistics.select(downloadImageCount)
                          .where(SDownLoadImageStatistics.user_uuid == user_uuid, SDownLoadImageStatistics.day >= this_period_start, SDownLoadImageStatistics.day <= this_period_end).get())
        downloadImageCounts = downLoadImages.downloadImageCount
        downloadModelCount = fn.SUM(SDownloadModelStatistics.downloadModelCount).alias('downloadModelCount')
        downloadModels = (SDownloadModelStatistics.select(downloadModelCount)
                          .where(SDownloadModelStatistics.user_uuid == user_uuid, SDownloadModelStatistics.day >= this_period_start, SDownloadModelStatistics.day <= this_period_end).get())
        downloadModelCounts = downloadModels.downloadModelCount
        runCount = fn.SUM(SRunStatistics.runCount).alias('runCount')
        runs = (SRunStatistics.select(runCount)
                .where(SRunStatistics.user_uuid == user_uuid, SRunStatistics.day >= this_period_start, SRunStatistics.day <= this_period_end).get())
        runCounts = runs.runCount
        data = {
            'nickname': nickname,
            'runCounts': 0 if runCounts is None else runCounts,
            'downloadModelCounts': 0 if downloadModelCounts is None else downloadModelCounts,
            'downloadImageCounts': 0 if downloadImageCounts is None else downloadImageCounts
        }
        if data.get('runCounts') != 0 or data.get('downloadModelCounts') != 0:
            datas.append(data)
    result = {
        'datas': datas,
        'month_start': this_period_start,
        'month_end': this_period_end
    }
    return jsonify(result)

@app.route('/getLastShakker')
def getLastShakker():
    datas = []
    accounts = ShakkerAccount.select()
    now = datetime.datetime.now()
    last = now.replace(day=1)
    last_month = last.month - 1
    last_period_start = datetime.datetime(now.year, last_month, 1).strftime('%Y%m%d')
    last_period_end = datetime.datetime(now.year, last_month, calendar.monthrange(now.year, last_month)[1]).strftime('%Y%m%d')
    for idx, account in enumerate(accounts):
        nickname = account.nickname
        user_uuid = account.user_uuid
        downloadImageCount = fn.SUM(SDownLoadImageStatistics.downloadImageCount).alias('downloadImageCount')
        downLoadImages = (SDownLoadImageStatistics.select(downloadImageCount)
                          .where(SDownLoadImageStatistics.user_uuid == user_uuid, SDownLoadImageStatistics.day >= last_period_start, SDownLoadImageStatistics.day <= last_period_end).get())
        downloadImageCounts = downLoadImages.downloadImageCount
        downloadModelCount = fn.SUM(SDownloadModelStatistics.downloadModelCount).alias('downloadModelCount')
        downloadModels = (SDownloadModelStatistics.select(downloadModelCount)
                          .where(SDownloadModelStatistics.user_uuid == user_uuid, SDownloadModelStatistics.day >= last_period_start, SDownloadModelStatistics.day <= last_period_end).get())
        downloadModelCounts = downloadModels.downloadModelCount
        runCount = fn.SUM(SRunStatistics.runCount).alias('runCount')
        runs = (SRunStatistics.select(runCount)
                .where(SRunStatistics.user_uuid == user_uuid, SRunStatistics.day >= last_period_start, SRunStatistics.day <= last_period_end).get())
        runCounts = runs.runCount
        data = {
            'nickname': nickname,
            'runCounts': 0 if runCounts is None else runCounts,
            'downloadModelCounts': 0 if downloadModelCounts is None else downloadModelCounts,
            'downloadImageCounts': 0 if downloadImageCounts is None else downloadImageCounts
        }
        if data.get('runCounts') != 0 or data.get('downloadModelCounts') != 0:
            datas.append(data)
    result = {
        'datas': datas,
        'month_start': last_period_start,
        'month_end': last_period_end
    }
    return jsonify(result)
