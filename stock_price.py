import requests
import datetime
import sys
import pandas as pd
from io import StringIO
import io
from model import stock_price
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from utility import getDbUrl
from log_tool import LogTool
import math
import time
from sqlalchemy.pool import NullPool

def stockprice(session,stock_code,year,month,date,infoLog,errorLog):
    start = datetime.datetime(year, month, date, 0, 0, 0)
    nowTime = datetime.datetime.now()
    period2 = str(round(((nowTime-start).total_seconds())))
    site = "https://query1.finance.yahoo.com/v7/finance/download/"+stock_code+".TW?period1=0&period2="+period2+"&interval=1d&events=history&crumb=hP2rOschxO0"
    response = requests.post(site)
    if response.status_code != '200':
        errorLog.log_dataBase(stock_code+' not found !')
    urlData = response.text
    rawData = pd.read_csv(io.StringIO(urlData))
    for index, row in rawData.iterrows():
        if math.isnan(row["Open"]) or pd.isnull(row["Date"]) or math.isnan(row["Volume"]):
            continue
        else:
            updatedate = datetime.datetime.now().strftime('%Y%m%d')
            updatetime = datetime.datetime.now().strftime('%H%M%S')
            
            stockprice = stock_price()
            stockprice.stockCode = stock_code
            stockprice.priceDate = row["Date"]
            stockprice.openPrice = row["Open"]
            stockprice.highPrice = row["High"]
            stockprice.lowPrice = row["Low"]
            stockprice.closePrice = row["Close"]
            stockprice.adj_close = row["Adj Close"]
            stockprice.volume = row["Volume"]
            stockprice.updateDate = updatedate
            stockprice.updatTime = updatetime
            session.merge(stockprice)
    session.commit()
    infoLog.log_dataBase(stock_code+' commit ok!')
#     with open(stock_code+'.csv', 'w') as f:
#         f.writelines(response.text)

def getAllStock():
    errorLog = LogTool('stock_price','error')
    infoLog = LogTool('stock_price','info')
    try:
        engine = create_engine(getDbUrl(), poolclass=NullPool)
        # create a configured "Session" class
        Session = sessionmaker(bind=engine)
        # create a Session
        session = Session()
        for i in range(1,9999):
            stock_code = '{:04d}'.format(i)
            print('get '+stock_code+' stock price')
            infoLog.log_dataBase('get '+stock_code+' stock price start...')
            stockprice(session,stock_code,2019,7,8,infoLog,errorLog)
            infoLog.log_dataBase('get '+stock_code+' stock price end...')
            time.sleep(2)
    except Exception as e:
        print(str(e))
        errorLog.log_dataBase(stock_code+' stock price Exception: '+str(e))
    finally:
        try:
            session.close()
        except Exception as e:
            return

if __name__ == '__main__':
    # stockprice('1409',1970,1,1)
    getAllStock()