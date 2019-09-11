# -*- coding: utf-8 -*-
"""
Created on Sun Jul  1 01:50:22 2018

@author: User
"""
import requests
import datetime
import sys
import pandas as pd
import numpy as np
from io import StringIO
import io
from model import price_book_ratio
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from utility import getDbUrl, getLastMonth, getDataFrameData, toMinGuoYearByDatetime
from log_tool import LogTool
import math
import time
from sqlalchemy.pool import NullPool
import re

def getPriceEarningsRatio2(session,runDay,infoLog,errorLog):
    try:
        priceDate = (str(runDay.year)+'{:02d}'.format(runDay.month)+'{:02d}'.format(runDay.day))
        MinGuoYYMMDD = toMinGuoYearByDatetime(runDay)
        s = requests.Session()
        s.config = {'keep_alive': False}
        headers = {
            'Content-Type': 'application/json',
            'Connection': 'close',
            'user-agent': 'Mozilla/5.0 (Macintosh Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36'
        }
        link = 'https://www.tpex.org.tw/web/stock/aftertrading/peratio_analysis/pera_result.php?l=zh-tw&o=csv&d='+MinGuoYYMMDD+'&c=&s=0,asc'
        infoLog.log_dataBase(link)
        r = requests.get(link, headers=headers, timeout=5)
    
        lines = r.text.replace('\r', '').split('\n')
        df = pd.read_csv(StringIO("\n".join(lines[4:])), header=None)

        print('----insert '+priceDate+' pbr----')
        for i in range(0,df.shape[0]):
            stockPBR = df.iloc[i]

            updatedate = datetime.datetime.now().strftime('%Y%m%d')
            updatetime = datetime.datetime.now().strftime('%H%M%S')
            
            pbr = price_book_ratio()
            pbr.priceDate = priceDate
            if pd.isnull(stockPBR[0]):
                continue
            if len(re.findall(r'[\u4e00-\u9fa5]', stockPBR[0]))>0:
                continue
            pbr.stockCode = stockPBR[0] #股票代號
            pbr.stockName = stockPBR[1] #證券名稱
            pbr.PER = getDataFrameData('float',stockPBR,2) #本益比
            pbr.yearOfDividend = getDataFrameData('str',stockPBR,4) #股利年度
            pbr.dividendYield = getDataFrameData('float',stockPBR,5) #殖利率(%)
            pbr.priceBookRatio = getDataFrameData('float',stockPBR,6) #股價淨值比
            pbr.financialReport = str(runDay.year-1911-1)+'/'+str(runDay.month)
            pbr.updateDate = updatedate
            pbr.updatTime = updatetime
            session.merge(pbr)
            
        session.commit()
        print('----insert '+priceDate+' pbr ok----')
        infoLog.log_dataBase(priceDate+' commit ok!')
    except Exception as e:
        print('Exception : {0}'.format(e))
        # print(resp_data)
    finally:
        s.close()
        print('requests session closed!')
        return
    
def getAllPriceEarningsRatio2():
    start = input("請輸入起始日期(Ex:20190101)：")
    before = int(input("請輸入往前抓幾天？："))+1
    runDay = datetime.datetime.strptime(start, '%Y%m%d')
    errorLog = LogTool('price_book_ratio2','error')
    infoLog = LogTool('price_book_ratio2','info')
    try:
        engine = create_engine(getDbUrl(), poolclass=NullPool)
        # create a configured "Session" class
        Session = sessionmaker(bind=engine)
        # create a Session
        session = Session()
        while before>0:
                print('get {0} price_book_ratio2'.format(runDay))
                infoLog.log_dataBase('get {0} price_book_ratio2 start...'.format(runDay))
                getPriceEarningsRatio2(session,runDay,infoLog,errorLog)
                runDay = runDay + datetime.timedelta(days=-1)
                before = before - 1
                # 偽停頓
                time.sleep(5)
                infoLog.log_dataBase('get {0} price_book_ratio2 end...'.format(runDay))

    except Exception as e:
        print(str(e))
        errorLog.log_dataBase('price_book_ratio2 Exception: '+str(e))
    finally:
        try:
            session.close()
        except Exception as e:
            return

if __name__ == '__main__':
    # stockprice('1409',1970,1,1)
    getAllPriceEarningsRatio2()