# -*- coding: utf-8 -*-
"""
Created on Sun Jul  1 01:50:22 2018

@author: User
"""
import numpy as np
import datetime
import pandas as pd
import requests
from io import StringIO
import time
from log_tool import LogTool
from model import monthly_revenue
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from utility import getDbUrl, getDataFrameData, getLastMonth
from sqlalchemy.pool import NullPool

def getYoYData(df):
    yoyDf = np.zeros(df.shape[0])
    for i in range(0,df.shape[0]):
        try:
            row = df.iloc[i]
            if float(row['當月累計營收']) == 0:
                np.append(yoyDf,0)
            else:
                yoyComp = (row['當月累計營收']-row['去年累計營收'])/row['當月累計營收']
                yoyDf[i] = yoyComp
        except Exception as e:
            print(str(e))
            np.append(yoyDf,0)
    
    return yoyDf

def monthly_report(session, year, month, infoLog):
    
    # 假如是西元，轉成民國
    if year > 1990:
        year -= 1911
    
    url = 'https://mops.twse.com.tw/nas/t21/sii/t21sc03_'+str(year)+'_'+str(month)+'_0.html'
    if year <= 98:
        url = 'https://mops.twse.com.tw/nas/t21/sii/t21sc03_'+str(year)+'_'+str(month)+'.html'
    
    # 偽瀏覽器
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    try:
        s = requests.Session()
        s.config = {'keep_alive': False}
        headers = {
            'Content-Type': 'application/json',
            'Connection': 'close',
            'user-agent': 'Mozilla/5.0 (Macintosh Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36'
        }
        # 下載該年月的網站，並用pandas轉換成 dataframe
        r = requests.get(url, headers=headers, timeout=5)
        # r = requests.get(url, headers=headers)
        r.encoding = 'big5'
        html_df = pd.read_html(StringIO(r.text))
    except Exception as e:
        year += 1911
        print(str(year)+str(month)+' 抓資料有問題：'+str(e))
        infoLog.log_dataBase('requests '+str(year)+'_'+str(month)+' monthly report ratio Exception: '+str(e))
    finally:
        s.close()
        print('Session closed!')
        return

    # 處理一下資料
    if html_df[0].shape[0] > 500:
        df = html_df[0].copy()
    else:
        df = pd.concat([df for df in html_df if df.shape[1] <= 11])
    df = df[list(range(0,10))]
    column_index = df.index[(df[0] == '公司代號')][0]
    df.columns = df.iloc[column_index]
    df['當月營收'] = pd.to_numeric(df['當月營收'], 'coerce')
    df['上月營收'] = pd.to_numeric(df['上月營收'], 'coerce')
    df['去年當月營收'] = pd.to_numeric(df['去年當月營收'], 'coerce')
    df['上月比較增減(%)'] = pd.to_numeric(df['上月比較增減(%)'], 'coerce')
    df['去年同月增減(%)'] = pd.to_numeric(df['去年同月增減(%)'], 'coerce')
    df['當月累計營收'] = pd.to_numeric(df['當月累計營收'], 'coerce')
    df['去年累計營收'] = pd.to_numeric(df['去年累計營收'], 'coerce')
    df['前期比較增減(%)'] = pd.to_numeric(df['前期比較增減(%)'], 'coerce')
    df = df[~df['當月營收'].isnull()]
    df = df[df['公司代號'] != '合計']
    df['累積年增率'] = getYoYData(df)
    year = year+1911
    month = '{:02d}'.format(month)
    # print(df.describe())
    # return
    print('----insert '+str(year)+str(month)+' monthly revenue----')
    for i in range(0,df.shape[0]):
        updatedate = datetime.datetime.now().strftime('%Y%m%d')
        updatetime = datetime.datetime.now().strftime('%H%M%S')
        
        mr = monthly_revenue()
        mr.revenueMonth = str(year)+str(month)
        mr.stockCode = getDataFrameData('str',df.iloc[i,:],'公司代號')
        mr.stockName = getDataFrameData('str',df.iloc[i,:],'公司名稱')
        mr.thisMonthRevenue = getDataFrameData('float',df.iloc[i,:],'當月營收')
        mr.lastMonthRevenue = getDataFrameData('float',df.iloc[i,:],'上月營收')
        mr.lastYearRevenue = getDataFrameData('float',df.iloc[i,:],'去年當月營收')
        mr.compLastMonth = getDataFrameData('float',df.iloc[i,:],'上月比較增減(%)')
        mr.compLastYear = getDataFrameData('float',df.iloc[i,:],'去年同月增減(%)')
        mr.thisMonthAccRevenue = getDataFrameData('float',df.iloc[i,:],'當月累計營收')
        mr.lastYearAccRevenue = getDataFrameData('float',df.iloc[i,:],'去年累計營收')
        mr.compLastAccRevenue = getDataFrameData('float',df.iloc[i,:],'前期比較增減(%)')
        mr.yoy = round(getDataFrameData('float',df.iloc[i,:],'累積年增率'),6)
        mr.updateDate = updatedate
        mr.updatTime = updatetime
        session.merge(mr)
    session.commit()
    print('----insert '+str(year)+str(month)+' monthly revenue ok----')
    infoLog.log_dataBase(str(year)+str(month)+' monthly_revenue commit ok!')
    
    # return df

def getAllMonthRevenue():
    before = int(input("請輸入往前抓幾個月？："))
    errorLog = LogTool('monthly_revenue','error')
    infoLog = LogTool('monthly_revenue','info')
    try:
        engine = create_engine(getDbUrl(), poolclass=NullPool)
        # create a configured "Session" class
        Session = sessionmaker(bind=engine)
        # create a Session
        session = Session()
        runDay = datetime.date.today()
        for i in range(0,before+1):
            runYYMM = str(runDay.year)+str(runDay.month)
            print('get '+runYYMM+' monthly revenue')
            infoLog.log_dataBase('get '+runYYMM+' monthly revenue start...')
            monthly_report(session,runDay.year,runDay.month,infoLog)
            # 偽停頓
            time.sleep(5)
            infoLog.log_dataBase('get '+runYYMM+' monthly revenue end...')
            print('get '+runYYMM+' monthly revenue OK!!!')
            runDay = getLastMonth(runYYMM)
        # for yy in range(2019,2020):
        #     for mm in range(1,13):
        #         print('get '+str(yy)+str(mm)+' monthly revenue')
        #         infoLog.log_dataBase('get '+str(yy)+str(mm)+' monthly revenue start...')
        #         monthly_report(session,yy,mm,infoLog)
        #         # 偽停頓
        #         time.sleep(5)
        #         infoLog.log_dataBase('get '+str(yy)+str(mm)+' monthly revenue end...')
    except Exception as e:
        print(str(e))
        errorLog.log_dataBase(str(runDay.year)+str(runDay.month)+' monthly revenue Exception: '+str(e))
    finally:
        try:
            session.close()
        except Exception as e:
            return

if __name__ == '__main__':
    getAllMonthRevenue()