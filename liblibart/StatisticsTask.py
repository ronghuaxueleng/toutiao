# -*- coding: utf-8 -*-
import calendar
import datetime

from peewee import fn

from UserInfo import Account as LiblibAccount
from Statistics import Statistics, DownLoadImageStatistics, DownloadModelStatistics, RunStatistics


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
