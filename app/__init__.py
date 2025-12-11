# -*- coding: utf-8 -*
import calendar
import datetime
import json
import time
from urllib.parse import urlencode

from flask import Flask, jsonify, request, Response
from flask import render_template
from peewee import fn

from app.ShakkerEmailLogin import ShakkerEmailLogin
from app.liblibQQLogin import liblibQQLogin
from app.liblibWXLogin import LiblibwxLogin
from app.liblibPhoneLogin import LiblibPhoneLogin
from outlook.TokenUtils import getToken
from run_task import profit_detail
from db.toutiao_jisu import Account, CommonParams
from liblibart.UserInfo import Account as LiblibAccount
from liblibart.SUserInfo import Account as ShakkerAccount
from liblibart.StatisticsTask import getLiblibStatisticsData
from liblibart.Statistics import Statistics
from liblibart.SStatistics import DownLoadImageStatistics as SDownLoadImageStatistics, \
    DownloadModelStatistics as SDownloadModelStatistics, RunStatistics as SRunStatistics

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
    now = datetime.datetime.now()
    this_period_start = datetime.datetime(now.year, now.month, 1).strftime('%Y%m%d')
    this_period_end = datetime.datetime(now.year, now.month, calendar.monthrange(now.year, now.month)[1]).strftime(
        '%Y%m%d')

    datas = getLiblibStatisticsData(this_period_start, this_period_end)
    for data in datas:
        query = Statistics.select().where(Statistics.user_uuid == data['user_uuid'],
                                          Statistics.period == data['period'])
        if query.exists():
            Statistics.update(
                runCount=data['runCounts'],
                downloadModelCount=data['downloadModelCounts'],
                downloadImageCount=data['downloadImageCounts']
            ).where(Statistics.user_uuid == data['user_uuid'],
                    Statistics.period == data['period']).execute()
        else:
            Statistics.insert(
                period=data['period'],
                user_uuid=data['user_uuid'],
                runCount=data['runCounts'],
                downloadModelCount=data['downloadModelCounts'],
                downloadImageCount=data['downloadImageCounts']
            ).execute()

    result = {
        'datas': datas,
        'month_start': this_period_start,
        'month_end': this_period_end
    }

    return jsonify(result)


@app.route('/getLastLiblib')
def getLastLiblib():
    now = datetime.datetime.now()
    last = now.replace(day=1)
    last_month = last.month - 2
    last_period_start = datetime.datetime(now.year, last_month, 1).strftime('%Y%m%d')
    last_period_end = datetime.datetime(now.year, last_month, calendar.monthrange(now.year, last_month)[1]).strftime(
        '%Y%m%d')
    datas = {}
    Statisticsdata = Statistics.select().where(Statistics.period >= f"{last_period_start}-{last_period_end}").order_by(
        Statistics.user_uuid, Statistics.period)
    for idx, data in enumerate(Statisticsdata):
        period = data.period
        runCount = data.runCount
        user_uuid = data.user_uuid
        downloadImageCount = data.downloadImageCount
        map = datas.setdefault(user_uuid, {})
        runCount_map = map.setdefault('runCount', {})
        runCount_map[period] = runCount
        map['runCount'] = runCount_map

        downloadImageCount_map = map.setdefault('downloadImageCount', {})
        downloadImageCount_map[period] = downloadImageCount
        map['downloadImageCount'] = downloadImageCount_map

        datas[user_uuid] = map

    result = []
    accounts = LiblibAccount.select()
    for idx, account in enumerate(accounts):
        if account.user_uuid in datas:
            profile = datas[account.user_uuid]
            runCounts = profile['runCount']
            runCount_list = []
            for period, runCount in runCounts.items():
                runCount_list.append(format(runCount, ','))

            downloadImageCounts = profile['downloadImageCount']
            downloadImageCount_list = []
            for period, downloadImageCount in downloadImageCounts.items():
                downloadImageCount_list.append(format(downloadImageCount, ','))
            result.append({
                'nickname': account.nickname,
                'runCounts': '/'.join(runCount_list),
                'downloadImageCounts': '/'.join(downloadImageCount_list)
            })
    result = {
        'datas': result,
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
    this_period_end = datetime.datetime(now.year, now.month, calendar.monthrange(now.year, now.month)[1]).strftime(
        '%Y%m%d')
    for idx, account in enumerate(accounts):
        nickname = account.nickname
        user_uuid = account.user_uuid
        downloadImageCount = fn.SUM(SDownLoadImageStatistics.downloadImageCount).alias('downloadImageCount')
        downLoadImages = (SDownLoadImageStatistics.select(downloadImageCount)
                          .where(SDownLoadImageStatistics.user_uuid == user_uuid,
                                 SDownLoadImageStatistics.day >= this_period_start,
                                 SDownLoadImageStatistics.day <= this_period_end).get())
        downloadImageCounts = downLoadImages.downloadImageCount
        downloadModelCount = fn.SUM(SDownloadModelStatistics.downloadModelCount).alias('downloadModelCount')
        downloadModels = (SDownloadModelStatistics.select(downloadModelCount)
                          .where(SDownloadModelStatistics.user_uuid == user_uuid,
                                 SDownloadModelStatistics.day >= this_period_start,
                                 SDownloadModelStatistics.day <= this_period_end).get())
        downloadModelCounts = downloadModels.downloadModelCount
        runCount = fn.SUM(SRunStatistics.runCount).alias('runCount')
        runs = (SRunStatistics.select(runCount)
                .where(SRunStatistics.user_uuid == user_uuid, SRunStatistics.day >= this_period_start,
                       SRunStatistics.day <= this_period_end).get())
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
    last_period_end = datetime.datetime(now.year, last_month, calendar.monthrange(now.year, last_month)[1]).strftime(
        '%Y%m%d')
    for idx, account in enumerate(accounts):
        nickname = account.nickname
        user_uuid = account.user_uuid
        downloadImageCount = fn.SUM(SDownLoadImageStatistics.downloadImageCount).alias('downloadImageCount')
        downLoadImages = (SDownLoadImageStatistics.select(downloadImageCount)
                          .where(SDownLoadImageStatistics.user_uuid == user_uuid,
                                 SDownLoadImageStatistics.day >= last_period_start,
                                 SDownLoadImageStatistics.day <= last_period_end).get())
        downloadImageCounts = downLoadImages.downloadImageCount
        downloadModelCount = fn.SUM(SDownloadModelStatistics.downloadModelCount).alias('downloadModelCount')
        downloadModels = (SDownloadModelStatistics.select(downloadModelCount)
                          .where(SDownloadModelStatistics.user_uuid == user_uuid,
                                 SDownloadModelStatistics.day >= last_period_start,
                                 SDownloadModelStatistics.day <= last_period_end).get())
        downloadModelCounts = downloadModels.downloadModelCount
        runCount = fn.SUM(SRunStatistics.runCount).alias('runCount')
        runs = (SRunStatistics.select(runCount)
                .where(SRunStatistics.user_uuid == user_uuid, SRunStatistics.day >= last_period_start,
                       SRunStatistics.day <= last_period_end).get())
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


@app.route('/outlook-callBack')
def outlookCallBack():
    code = request.args.get("code")
    client_id = request.args.get("client_id")
    return getToken(client_id, code)


@app.route('/outlook-refresh_token')
def outlookRefreshToken():
    code = request.args.get("code")
    client_id = request.args.get("client_id")
    return getToken(client_id, code)


@app.route('/email-login')
def emailLogin():
    id = request.args.get("id")
    email = request.args.get("email")
    shakkerEmailLogin = ShakkerEmailLogin()
    shakkerEmailLogin.sendLoginEmail(email)
    return shakkerEmailLogin.login(id)


@app.route('/bindwx')
def wxQrcodeShow():
    id = request.args.get("id")
    login = LiblibwxLogin()
    login.get_qrcode()
    ticket = login.ticket
    qrCodeUrl = login.qrCodeUrl
    return render_template('bindwx.html',
                           id=id,
                           qrCodeUrl=qrCodeUrl,
                           ticket=ticket,
                           starttime=int(time.time())
                           )


@app.route('/bindwx-check')
def wxQrcodeCheck():
    id = request.args.get("id")
    ticket = request.args.get("ticket")
    starttime = request.args.get("starttime")
    login = LiblibwxLogin(starttime)
    login.qrcode(ticket, id)
    return 'ok'


@app.route('/bindqq')
def qqQrcodeShow():
    id = request.args.get("id")
    login = liblibQQLogin()
    img = login.qrShow()
    session_id = login.session_id
    qrsig = login.sess.cookies.get_dict().get('qrsig', '')
    login_sig = login.sess.cookies.get_dict().get('pt_login_sig', '')
    return render_template('bindqq.html',
                           id=id,
                           qrsig=qrsig,
                           login_sig=login_sig,
                           session_id=session_id,
                           # img_stream=base64.b64encode(img.content).decode('utf-8'),
                           img_url=img
                           )


@app.route('/bindqq-check', methods=['POST'])
def qqQrcodeCheck():
    data = request.form
    id = data.get('id')
    qrsig = data.get('qrsig')
    img_url = data.get('img_url')
    login_sig = data.get('login_sig')
    session_id = data.get('session_id')
    login = liblibQQLogin(session_id)
    login.qrLogin(qrsig, login_sig, img_url, id)
    return 'ok'


@app.route("/api/pic/<file_name>", methods=['GET'])
def get_img(file_name):
    path = f'/mitmproxy/logs/{file_name}'
    resp = Response(open(path, 'rb'), mimetype="image/jpeg")
    return resp


@app.route('/phone-login')
def phoneLogin():
    """手机验证码登录页面"""
    id = request.args.get("id")
    return render_template('phoneLogin.html', id=id)


@app.route('/send-phone-code', methods=['POST'])
def sendPhoneCode():
    """发送手机验证码接口"""
    try:
        data = request.get_json()
        phone = data.get('phone')
        
        if not phone:
            return jsonify({'status': 'error', 'message': '请输入手机号'})
        
        phone_login = LiblibPhoneLogin()
        result = phone_login.sendLoginPhoneCode(phone)
        return jsonify(result)
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})


@app.route('/phone-login-verify', methods=['POST'])
def phoneLoginVerify():
    """手机验证码登录接口"""
    try:
        data = request.get_json()
        phone = data.get('phone')
        code = data.get('code')
        id = data.get('id')

        if not phone or not code:
            return jsonify({'status': 'error', 'message': '请输入手机号和验证码'})

        phone_login = LiblibPhoneLogin()
        result = phone_login.loginByPhoneCode(phone, code, id)
        return jsonify(result)
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})


@app.route('/tencent17995076833674810104.txt')
def tencent_verify():
    """腾讯域名验证文件"""
    return '15102954905091242189'
