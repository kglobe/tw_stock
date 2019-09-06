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
from model import price_book_ratio
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from utility import getDbUrl,getDataFrameData
from sqlalchemy.pool import NullPool

def getPriceEarningsRatio(session, dataDate, infoLog):
    nowTime = datetime.datetime.now()
    if dataDate > nowTime:
        return

    datestr = dataDate.strftime('%Y%m%d')
    s = requests.Session()
    s.config = {'keep_alive': False}
    headers = {
        'Content-Type': 'application/json',
        'Connection': 'close',
        'user-agent': 'Mozilla/5.0 (Macintosh Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36'
    }
    r = requests.get('https://www.twse.com.tw/exchangeReport/BWIBBU_d?response=csv&date='+datestr+'&selectType=ALL', headers=headers, timeout=5)
    r.encoding = 'big5'
    
    # aa = r.text.split('\n')
    # for idx, val in enumerate(aa):
    #     if idx == 50:
    #         print(idx,val)
    #         print(len(val.split('",')))
    # return

    # print(r.text)
    formateChangeDate = datetime.datetime.strptime('20170412', '%Y%m%d')
    try:
        if dataDate > formateChangeDate:
            df = pd.read_csv(StringIO("\n".join([i.translate({ord(c): None for c in ' '}) 
                                                for i in r.text.split('\n') 
                                                if len(i.split('",')) == 8 and i[0] != '='])), header=0)
        else:
            df = pd.read_csv(StringIO("\n".join([i.translate({ord(c): None for c in ' '}) 
                                                for i in r.text.split('\n') 
                                                if len(i.split('",')) == 6 and i[0] != '='])), header=0)
        #拿掉最後一欄Unnamed: 16
        df.drop(df.columns[df.shape[1]-1], axis=1, inplace=True)
        # print(df)
        
        print('----insert '+datestr+' price book ratio----')
        for i in range(0,df.shape[0]):

            updatedate = datetime.datetime.now().strftime('%Y%m%d')
            updatetime = datetime.datetime.now().strftime('%H%M%S')
            
            stockPER = df.iloc[i,:]
            
            pbr = price_book_ratio()
            pbr.priceDate = datestr
            pbr.stockCode = getDataFrameData('str',stockPER,'證券代號')
            pbr.stockName = getDataFrameData('str',stockPER,'證券名稱')
            pbr.dividendYield = getDataFrameData('float',stockPER,'殖利率(%)')
            if dataDate > formateChangeDate:
                pbr.yearOfDividend = getDataFrameData('str',stockPER,'股利年度')
            else:
                pbr.yearOfDividend = str(dataDate.year-1911-1)
            pbr.PER = getDataFrameData('float',stockPER,'本益比')
            if pbr.PER == '-':
                pbr.PER = None
            pbr.priceBookRatio = getDataFrameData('float',stockPER,'股價淨值比')
            if dataDate > formateChangeDate:
                pbr.financialReport = getDataFrameData('flostrat',stockPER,'財報年/季')
            else:
                pbr.financialReport = str(dataDate.year-1911-1)+'/'+str(dataDate.month)
            pbr.updateDate = updatedate
            pbr.updateTime = updatetime
            session.merge(pbr)
        session.commit()
        infoLog.log_dataBase(datestr+' price_book_ratio commit ok!')
        print('----insert '+datestr+' price book ratio ok----')
    except Exception as e:
        print('Exception : {0}'.format(e))
        infoLog.log_dataBase(datestr+' price book ratio Exception: '+str(e))
    finally:
        s.close()
        print('requests session closed!')
        return
    
def getAllPriceEarningsRatio():
    start = input("請輸入起始日期(Ex:20190101)：")
    before = int(input("請輸入往前抓幾天？："))+1
    dataDate = datetime.datetime.strptime(start, '%Y%m%d')
    errorLog = LogTool('price_book_ratio','error')
    infoLog = LogTool('price_book_ratio','info')
    datestr = ''
    try:
        engine = create_engine(getDbUrl(), poolclass=NullPool)
        # create a configured "Session" class
        Session = sessionmaker(bind=engine)
        # create a Session
        session = Session()
        # monthly_report(session,2011,1,infoLog)
        while before>0:
            datestr = dataDate.strftime('%Y%m%d')
            print('get '+datestr+' price book ratio')
            infoLog.log_dataBase('get '+datestr+' price book ratio start...')
            getPriceEarningsRatio(session,dataDate,infoLog)
            dataDate = dataDate + datetime.timedelta(days=-1)
            before = before - 1
            # 偽停頓
            time.sleep(5)
            infoLog.log_dataBase('get '+datestr+' price book ratio end...')
    except Exception as e:
        print(str(e))
        errorLog.log_dataBase(datestr+' price book ratio Exception: '+str(e))
    finally:
        try:
            session.close()
        except Exception as e:
            return

if __name__ == '__main__':
    getAllPriceEarningsRatio()