import requests
import datetime
import sys
import pandas as pd
import numpy as np
from io import StringIO
import io
from model import stock_price
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from utility import getDbUrl, getLastMonth, getDataFrameData, toMinGuoYearByDatetime
from log_tool import LogTool
import math
import time
from sqlalchemy.pool import NullPool
import re

def stockprice(session,runDay,infoLog,errorLog):
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
        # resp = requests.get('https://www.twse.com.tw/exchangeReport/STOCK_DAY?response=json&date='+year_month+'&stockNo='+str(stock_code), headers=headers, timeout=5)
        # resp_data = resp.json()
        link = 'http://www.tpex.org.tw/web/stock/aftertrading/daily_close_quotes/stk_quote_download.php?l=zh-tw&d='+MinGuoYYMMDD+'&s=0,asc,0'
        infoLog.log_dataBase(link)
        r = requests.get(link, headers=headers, timeout=5)
        # if resp_data['stat'] != 'OK':
        #     print('stock('+stock_code+'): '+str(resp_data['stat']))
        #     infoLog.log_dataBase(stock_code+' : '+str(resp_data['stat']))
        #     return
    
        # rawData = pd.DataFrame(np.array(resp_data['data']), columns=np.array(resp_data['fields']))
        # lines = r.text.replace('\r', '').split('\n')
        # df = pd.read_csv(StringIO("\n".join(lines[3:])), header=None)
        # df.columns = list(map(lambda l: l.replace(' ',''), lines[2].split(',')))
        lines = r.text.replace('\r', '').split('\n')
        df = pd.read_csv(StringIO("\n".join(lines[3:])), header=None)
        print('----insert '+priceDate+' price----')
        for i in range(0,df.shape[0]):
            stockPrice = df.iloc[i]

            updatedate = datetime.datetime.now().strftime('%Y%m%d')
            updatetime = datetime.datetime.now().strftime('%H%M%S')
            
            stockprice = stock_price()
            stockprice.priceDate = priceDate
            if len(re.findall(r'[\u4e00-\u9fa5]', stockPrice[0]))>0:
                continue
            stockprice.stockCode = stockPrice[0]
            stockprice.stockName = stockPrice[1]
            stockprice.closePrice = getDataFrameData('float',stockPrice,2)
            stockprice.priceLimit = getDataFrameData('float',stockPrice,3)
            stockprice.openPrice = getDataFrameData('float',stockPrice,4)
            stockprice.highPrice = getDataFrameData('float',stockPrice,5)
            stockprice.lowPrice = getDataFrameData('float',stockPrice,6)
            stockprice.meanPrice = getDataFrameData('float',stockPrice,7)
            stockprice.tradingVolume = getDataFrameData('int',stockPrice,8)
            stockprice.turnover = getDataFrameData('int',stockPrice,9)
            stockprice.numOfTransactions = getDataFrameData('int',stockPrice,10)
            stockprice.lastSellPrice = getDataFrameData('float',stockPrice,11)
            stockprice.lastSellPrice = getDataFrameData('float',stockPrice,12)
            stockprice.publicNum = getDataFrameData('int',stockPrice,13)
            stockprice.nextDayPrice = getDataFrameData('float',stockPrice,14)
            stockprice.nextDayLimitUp = getDataFrameData('float',stockPrice,15)
            stockprice.nextDayLimitDown = getDataFrameData('float',stockPrice,16)
            stockprice.updateDate = updatedate
            stockprice.updatTime = updatetime
            session.merge(stockprice)
            
        session.commit()
        print('----insert '+priceDate+' price ok----')
        infoLog.log_dataBase(priceDate+' commit ok!')
    except Exception as e:
        print('Exception : {0}'.format(e))
        # print(resp_data)
    finally:
        s.close()
        print('requests session closed!')
        return
    
#     with open(stock_code+'.csv', 'w') as f:
#         f.writelines(response.text)

def getAllStock():
    start = input("請輸入起始日期(Ex:20190101)：")
    before = int(input("請輸入往前抓幾天？："))+1
    runDay = datetime.datetime.strptime(start, '%Y%m%d')
    errorLog = LogTool('stock_price','error')
    infoLog = LogTool('stock_price','info')
    try:
        engine = create_engine(getDbUrl(), poolclass=NullPool)
        # create a configured "Session" class
        Session = sessionmaker(bind=engine)
        # create a Session
        session = Session()
        while before>0:
                print('get {0} stock price ratio'.format(runDay))
                infoLog.log_dataBase('get {0} price stock price start...'.format(runDay))
                stockprice(session,runDay,infoLog,errorLog)
                runDay = runDay + datetime.timedelta(days=-1)
                before = before - 1
                # 偽停頓
                time.sleep(5)
                infoLog.log_dataBase('get {0} price stock price end...'.format(runDay))

        # for k in range(0,before+1):
            # runYYMM = str(runDay.year)+str(runDay.month)
            # for i in range(0,10000):
            #     stock_code = '{:04d}'.format(i)
            #     print('get '+runYYMMDD+' stock('+stock_code+') stock price start...')
            #     infoLog.log_dataBase('get '+runYYMMDD+' stock('+stock_code+') stock price start...')
            #     stockprice(session,stock_code,runYYMMDD,infoLog,errorLog)
            #     infoLog.log_dataBase('get '+runYYMMDD+' stock('+stock_code+') stock price end...')
            #     print('get '+runYYMMDD+' stock('+stock_code+') stock price end...')
            #     if i%10 == 0:
            #         print('sleep 20 seconds...')
            #         time.sleep(20)
            #     else:
            #         print('sleep 5 seconds...')
            #         time.sleep(5)
            # runDay = getLastMonth(runYYMM)
    except Exception as e:
        print(str(e))
        errorLog.log_dataBase('stock price Exception: '+str(e))
    finally:
        try:
            session.close()
        except Exception as e:
            return

if __name__ == '__main__':
    # stockprice('1409',1970,1,1)
    getAllStock()