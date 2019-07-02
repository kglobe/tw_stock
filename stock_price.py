import requests
import datetime
import sys
import pandas as pd
from io import StringIO
import io
from model import stock_price
from db_session import dbSession
import math

def stockprice(stock_code,year,month,date):
    start = datetime.datetime(year, month, date, 0, 0, 0)
    nowTime = datetime.datetime.now()
    period2 = str(round(((nowTime-start).total_seconds())))
    site = "https://query1.finance.yahoo.com/v7/finance/download/"+stock_code+".TW?period1=0&period2="+period2+"&interval=1d&events=history&crumb=hP2rOschxO0"
    response = requests.post(site)
    urlData = response.text
    session = dbSession().getSession()
    rawData = pd.read_csv(io.StringIO(urlData))
    print(rawData.head())
    for index, row in rawData.iterrows():
        if math.isnan(row["Open"]) or pd.isnull(row["Date"]) or math.isnan(row["Volume"]):
            continue
        else:
            stockprice = stock_price()
            stockprice.stockCode = stock_code
            stockprice.priceDate = row["Date"]
            stockprice.openPrice = row["Open"]
            stockprice.highPrice = row["High"]
            stockprice.lowPrice = row["Low"]
            stockprice.closePrice = row["Close"]
            stockprice.adj_close = row["Adj Close"]
            stockprice.volume = row["Volume"]
            session.add(stockprice)
    session.commit()
    session.close()
#     with open(stock_code+'.csv', 'w') as f:
#         f.writelines(response.text)

if __name__ == '__main__':
    stockprice('1409',1970,1,1)