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
from model import price_earnings_ratio
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from utility import getDbUrl,getDataFrameData
from sqlalchemy.pool import NullPool

def getPriceEarningsRatio(session, datestr, infoLog):
    nowTime = datetime.datetime.now()
    if datestr > (str(nowTime.year)+'{:02d}'.format(nowTime.month)+'{:02d}'.format(nowTime.day)):
        return
    
    try:
        s = requests.Session()
        s.config = {'keep_alive': False}
        headers = {
            'Content-Type': 'application/json',
            'Connection': 'close',
            'user-agent': 'Mozilla/5.0 (Macintosh Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36'
        }
        r = requests.post('http://www.twse.com.tw/exchangeReport/MI_INDEX?response=csv&date=' + datestr + '&type=ALL', headers=headers, timeout=5)
        r.encoding = 'big5'
        df = pd.read_csv(StringIO("\n".join([i.translate({ord(c): None for c in ' '}) 
                                            for i in r.text.split('\n') 
                                            if len(i.split('",')) == 17 and i[0] != '='])), header=0)
    except Exception as e:
        print('Exception : {0}'.format(e))
        infoLog.log_dataBase(datestr+' price earnings ratio Exception: '+str(e))
    finally:
        s.close()
        print('Session closed!')
        return
    
    #拿掉最後一欄Unnamed: 16
    df.drop(df.columns[df.shape[1]-1], axis=1, inplace=True)
    print('----insert '+datestr+' price earnings ratio----')
    for i in range(0,df.shape[0]):

        updatedate = datetime.datetime.now().strftime('%Y%m%d')
        updatetime = datetime.datetime.now().strftime('%H%M%S')

        stockPER = df.iloc[i]

        per = price_earnings_ratio()
        per.priceDate = datestr
        per.stockCode = getDataFrameData('str',stockPER,'證券代號')
        per.stockName = getDataFrameData('str',stockPER,'證券名稱')
        per.tradingVolume = getDataFrameData('int',stockPER,'成交股數')
        per.numOfTransactions = getDataFrameData('int',stockPER,'成交筆數')
        per.turnover = getDataFrameData('int',stockPER,'成交金額')
        per.openPrice = getDataFrameData('float',stockPER,'開盤價')
        per.highPrice = getDataFrameData('float',stockPER,'最高價')
        per.lowPrice = getDataFrameData('float',stockPER,'最低價')
        per.closePrice = getDataFrameData('float',stockPER,'最低價')
        per.upOrDown = getDataFrameData('str',stockPER,'漲跌(+/-)')
        per.priceLimit = getDataFrameData('float',stockPER,'漲跌價差')
        per.finalBuyPrice = getDataFrameData('float',stockPER,'最後揭示買價')
        per.finalBuyVolume = getDataFrameData('int',stockPER,'最後揭示買量')
        per.finalSellPrice = getDataFrameData('float',stockPER,'最後揭示賣價')
        per.finalSellVolume = getDataFrameData('int',stockPER,'最後揭示賣量')
        per.PER = getDataFrameData('float',stockPER,'本益比')
        per.updateDate = updatedate
        per.updatTime = updatetime
        session.merge(per)
    session.commit()
    infoLog.log_dataBase(datestr+' price_earnings_ratio commit ok!')
    print('----insert '+datestr+' price earnings ratio ok----')

def getAllPriceEarningsRatio():
    start = input("請輸入起始日期(Ex:20190101)：")
    before = int(input("請輸入往前抓幾天？："))+1
    dataDate = datetime.datetime.strptime(start, '%Y%m%d')
    errorLog = LogTool('price_earnings_ratio','error')
    infoLog = LogTool('price_earnings_ratio','info')
    datestr = ''
    try:
        engine = create_engine(getDbUrl(), poolclass=NullPool)
        # create a configured "Session" class
        Session = sessionmaker(bind=engine)
        # create a Session
        session = Session()
        # monthly_report(session,2011,1,infoLog)
        while before>0:
            print('get '+datestr+' price earnings ratio')
            infoLog.log_dataBase('get '+datestr+' price earnings ratio start...')
            getPriceEarningsRatio(session,dataDate.strftime("%Y%m%d"),infoLog)
            dataDate = dataDate + datetime.timedelta(days=-1)
            before = before - 1
            # 偽停頓
            time.sleep(5)
            infoLog.log_dataBase('get '+datestr+' price earnings ratio end...')
    except Exception as e:
        print(str(e))
        errorLog.log_dataBase(datestr+' price earnings ratio Exception: '+str(e))
    finally:
        try:
            session.close()
        except Exception as e:
            return

if __name__ == '__main__':
    getAllPriceEarningsRatio()