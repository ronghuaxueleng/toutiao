# -*- coding: utf-8 -*-
import calendar
import datetime

from peewee import fn

from liblibart.UserInfo import Account as LiblibAccount
from liblibart.Statistics import Statistics, DownLoadImageStatistics, DownloadModelStatistics, RunStatistics


def getLiblibStatisticsData(start_period, end_period):
    datas = []
    accounts = LiblibAccount.select()
    for idx, account in enumerate(accounts):
        nickname = account.nickname
        user_uuid = account.user_uuid
        downloadImageCount = fn.SUM(DownLoadImageStatistics.downloadImageCount).alias('downloadImageCount')
        downLoadImages = (DownLoadImageStatistics.select(downloadImageCount)
                          .where(DownLoadImageStatistics.user_uuid == user_uuid,
                                 DownLoadImageStatistics.day >= start_period,
                                 DownLoadImageStatistics.day <= end_period).get())
        downloadImageCounts = downLoadImages.downloadImageCount
        downloadModelCount = fn.SUM(DownloadModelStatistics.downloadModelCount).alias('downloadModelCount')
        downloadModels = (DownloadModelStatistics.select(downloadModelCount)
                          .where(DownloadModelStatistics.user_uuid == user_uuid,
                                 DownloadModelStatistics.day >= start_period,
                                 DownloadModelStatistics.day <= end_period).get())
        downloadModelCounts = downloadModels.downloadModelCount
        runCount = fn.SUM(RunStatistics.runCount).alias('runCount')
        runs = (RunStatistics.select(runCount)
                .where(RunStatistics.user_uuid == user_uuid, RunStatistics.day >= start_period,
                       RunStatistics.day <= end_period).get())
        runCounts = runs.runCount
        data = {
            'user_uuid': user_uuid,
            'period': f"{start_period}-{end_period}",
            'runCounts': 0 if runCounts is None else runCounts,
            'downloadModelCounts': 0 if downloadModelCounts is None else downloadModelCounts,
            'downloadImageCounts': 0 if downloadImageCounts is None else downloadImageCounts
        }
        if (data.get('runCounts') != 0 and data.get('downloadImageCounts') != 0) or data.get(
                'downloadModelCounts') != 0:
            datas.append(data)
    return datas


if __name__ == '__main__':
    now = datetime.datetime.now()
    last = now.replace(day=1)
    last_month = last.month - 2
    last_period_start = datetime.datetime(now.year, last_month, 1).strftime('%Y%m%d')
    last_period_end = datetime.datetime(now.year, last_month, calendar.monthrange(now.year, last_month)[1]).strftime(
        '%Y%m%d')
    datas = {}
    Statisticsdata = Statistics.select().where(Statistics.period >= f"{last_period_start}-{last_period_end}").order_by(Statistics.user_uuid, Statistics.period)
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
                'runCount': '/'.join(runCount_list),
                'downloadImageCount': '/'.join(downloadImageCount_list)
            })
    print(result)