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
from utility import getDbUrl, getLastMonth, getDataFrameData
from log_tool import LogTool
import math
import time
from sqlalchemy.pool import NullPool

def stockprice(session,stock_code,year_month,infoLog,errorLog):
    try:
        s = requests.Session()
        s.config = {'keep_alive': False}
        headers = {
            'Content-Type': 'application/json',
            'Connection': 'close',
            'user-agent': 'Mozilla/5.0 (Macintosh Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36'
        }
        resp = requests.get('https://www.twse.com.tw/exchangeReport/STOCK_DAY?response=json&date='+year_month+'&stockNo='+str(stock_code), headers=headers, timeout=5)
        resp_data = resp.json()

        if resp_data['stat'] != 'OK':
            print('stock('+stock_code+'): '+str(resp_data['stat']))
            infoLog.log_dataBase(stock_code+' : '+str(resp_data['stat']))
            return
    
        rawData = pd.DataFrame(np.array(resp_data['data']), columns=np.array(resp_data['fields']))

        print('----insert '+str(year_month)+' stock('+stock_code+') price----')
        for i in range(0,rawData.shape[0]):
            stockPrice = rawData.iloc[i]

            updatedate = datetime.datetime.now().strftime('%Y%m%d')
            updatetime = datetime.datetime.now().strftime('%H%M%S')
            
            stockprice = stock_price()
            stockprice.stockCode = stock_code
            stockdate = getDataFrameData('str',stockPrice,'日期')
            year = int(stockdate[:3])+1911
            stockprice.priceDate = str(year)+stockdate[3:]
            stockprice.tradingVolume = getDataFrameData('int',stockPrice,'成交股數')
            stockprice.turnover = getDataFrameData('int',stockPrice,'成交金額')
            stockprice.openPrice = getDataFrameData('float',stockPrice,'開盤價')
            stockprice.highPrice = getDataFrameData('float',stockPrice,'最高價')
            stockprice.lowPrice = getDataFrameData('float',stockPrice,'最低價')
            stockprice.closePrice = getDataFrameData('float',stockPrice,'收盤價')
            stockprice.priceLimit = getDataFrameData('str',stockPrice,'漲跌價差')
            stockprice.numOfTransactions = getDataFrameData('int',stockPrice,'成交筆數')
            stockprice.updateDate = updatedate
            stockprice.updatTime = updatetime
            session.merge(stockprice)
            
        session.commit()
        print('----insert '+str(year_month)+' stock('+stock_code+') price ok----')
        infoLog.log_dataBase(stock_code+' commit ok!')
    except Exception as e:
        print(str(e))
        print(resp_data)
    finally:
        s.close()
    
#     with open(stock_code+'.csv', 'w') as f:
#         f.writelines(response.text)

def getAllStock():
    before = int(input("請輸入往前抓幾個月？："))
    errorLog = LogTool('stock_price','error')
    infoLog = LogTool('stock_price','info')
    try:
        engine = create_engine(getDbUrl(), poolclass=NullPool)
        # create a configured "Session" class
        Session = sessionmaker(bind=engine)
        # create a Session
        session = Session()
        runDay = datetime.date.today()
        for k in range(0,before+1):
            runYYMM = str(runDay.year)+str(runDay.month)
            for i in range(0,10000):
                stock_code = '{:04d}'.format(i)
                print('get '+runYYMM+' stock('+stock_code+') stock price start...')
                infoLog.log_dataBase('get '+runYYMM+' stock('+stock_code+') stock price start...')
                stockprice(session,stock_code,runYYMM,infoLog,errorLog)
                infoLog.log_dataBase('get '+runYYMM+' stock('+stock_code+') stock price end...')
                print('get '+runYYMM+' stock('+stock_code+') stock price end...')
                if i%10 == 0:
                    print('sleep 20 seconds...')
                    time.sleep(20)
                else:
                    print('sleep 5 seconds...')
                    time.sleep(5)
            runDay = getLastMonth(runYYMM)
    except Exception as e:
        print(str(e))
        errorLog.log_dataBase('stock('+stock_code+') price Exception: '+str(e))
    finally:
        try:
            session.close()
        except Exception as e:
            return

if __name__ == '__main__':
    # stockprice('1409',1970,1,1)
    getAllStock()