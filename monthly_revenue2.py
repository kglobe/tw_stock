# -*- coding: utf-8 -*-
"""
Created on Sun Jul  1 01:50:22 2018

@author: User
"""
import numpy as np
import datetime
import time
import pandas as pd
import requests
from bs4 import BeautifulSoup
from log_tool import LogTool
from model import monthly_revenue
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from utility import getDbUrl, getDataFrameData, getLastMonth
from sqlalchemy.pool import NullPool

def getYoYData(mr):
    try:
        if float(mr.lastYearAccRevenue) == 0:
            return 0
        else:
            return (mr.thisMonthAccRevenue-mr.lastYearAccRevenue)*100/mr.lastYearAccRevenue
    except Exception as e:
        print(str(e))
        return 0

def getCompLastMonth(mr):
    try:
        if float(mr.lastMonthRevenue) == 0:
            return 0
        else:
            return (mr.thisMonthRevenue-mr.lastMonthRevenue)*100/mr.lastMonthRevenue
    except Exception as e:
        print(str(e))
        return 0

def getPayload(stockCode, year, month):
    payload = {
        'encodeURIComponent': 1,
        'step': 1,
        'firstin': 1,
        'off': 1,
        'queryName': stockCode,
        'inpuType': stockCode,
        'TYPEK': 'all',
        'isnew': 'false',
        'co_id': stockCode,
        'year': year,
        'month': '{:02d}'.format(month)}
    return payload

def monthly_report(session, stockCode, year, month, infoLog):
    td_array = None
    # 假如是西元，轉成民國
    if year > 1990:
        year -= 1911
    #選歷史資料後按搜尋
    payload = getPayload(stockCode, year, month)

    headers = {'user-agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36'}
    
    try:
        s = requests.Session()
        s.config = {'keep_alive': False}
        r = requests.post('https://mops.twse.com.tw/mops/web/t05st10_ifrs', data=payload, headers=headers, timeout=5)
        r.encoding = 'utf8'
        soup = BeautifulSoup(r.text, 'html.parser')
        stockName = soup.select_one('td.compName b').text.strip()
        stockName = stockName[stockName.index('公司)')+3:stockName.index('公司提供')].strip()
        table = soup.select_one('table.hasBorder')
        trs = table.select('tr')
        th_array = []
        td_array = []
        for idx, t in enumerate(trs):
            # print(idx,':',t.th,',',t.td)
            if t.th == None:
                if idx > 1 and idx < 10:
                    tds = t.find_all('td')
                    if tds[0].text.strip() == '增減百分比' and idx==5:
                        th_array.append('單月年增率')
                        td_array.append(tds[1].text.strip())
                    elif tds[0].text.strip() == '增減百分比' and idx==9:
                        th_array.append('累積年增率')
                        td_array.append(tds[1].text.strip())
                    else:
                        th_array.append(tds[0].text.strip())
                        td_array.append(tds[1].text.strip())
            else:
                if idx != 0:
                    if t.th.text.strip() == '增減百分比' and idx==4:
                        th_array.append('單月年增率')
                        td_array.append(t.td.text.strip())
                    elif t.th.text.strip() == '增減百分比' and idx==8:
                        th_array.append('累積年增率')
                        td_array.append(t.td.text.strip())
                    else:
                        th_array.append(t.th.text.strip())
                        td_array.append(t.td.text.strip())
        
        if (month-1) == 0:
            payload = getPayload(stockCode, year-1, 12)
        else:
            payload = getPayload(stockCode, year, month-1)
        
        time.sleep(2)
        month = '{:02d}'.format(month)
        r = requests.post('https://mops.twse.com.tw/mops/web/t05st10_ifrs', data=payload, headers=headers, timeout=5)
        r.encoding = 'utf8'
        soup = BeautifulSoup(r.text, 'html.parser')
        table = soup.select_one('table.hasBorder')
        if table == None:
            th_array.append('上月營收')
            td_array.append(None)
        else:
            trs = table.select('tr')
            for t in trs:
                if t.th == None:
                    tds = t.find_all('td')
                    if tds[0].text.strip() == '本月':
                        th_array.append('上月營收')
                        td_array.append(tds[1].text.strip())
                else:
                    if t.th.text.strip() == '本月':
                        th_array.append('上月營收')
                        td_array.append(t.td.text.strip())

    except Exception as e:
        year += 1911
        print('stockCode:'+stockCode+', '+str(year)+str(month)+' 抓資料有問題：'+str(e))
        infoLog.log_dataBase('requests '+'stockCode:'+stockCode+', '+str(year)+'_'+str(month)+' monthly report ratio Exception: '+str(e))
    finally:
        s.close()
        print('Session closed!')
    
    if td_array == None:
        return
    df = pd.DataFrame(np.array([td_array]),columns=th_array)
    year = year+1911

    print('----insert '+stockName+' '+str(year)+str(month)+' monthly revenue 2----')
    updatedate = datetime.datetime.now().strftime('%Y%m%d')
    updatetime = datetime.datetime.now().strftime('%H%M%S')
    
    mr = monthly_revenue()
    mr.revenueMonth = str(year)+str(month)
    mr.stockCode = stockCode
    mr.stockName = stockName
    mr.thisMonthRevenue = getDataFrameData('float',df.iloc[0,:],'本月')
    mr.lastMonthRevenue = getDataFrameData('float',df.iloc[0,:],'上月營收')
    mr.lastYearRevenue = getDataFrameData('float',df.iloc[0,:],'去年同期')
    mr.compLastYear = getDataFrameData('float',df.iloc[0,:],'單月年增率')
    mr.thisMonthAccRevenue = getDataFrameData('float',df.iloc[0,:],'本年累計')
    mr.lastYearAccRevenue = getDataFrameData('float',df.iloc[0,:],'去年累計')
    mr.compLastAccRevenue = getDataFrameData('float',df.iloc[0,:],'累積年增率')
    mr.compLastMonth = round(getCompLastMonth(mr),6)
    mr.yoy = round(getYoYData(mr),6)
    mr.updateDate = updatedate
    mr.updatTime = updatetime
    session.merge(mr)
    session.commit()
    print('----insert '+stockName+' '+str(year)+str(month)+' monthly revenue 2 ok----')
    infoLog.log_dataBase(str(year)+str(month)+' monthly_revenue commit ok!')

def getAllMonthRevenue():
    start = input("請輸入起始年月(Ex:201901)：")
    before = int(input("請輸入往前抓幾個月？："))
    startCode = int(input("請輸入起始股票代碼？："))
    errorLog = LogTool('monthly_revenue2','error')
    infoLog = LogTool('monthly_revenue2','info')
    try:
        engine = create_engine(getDbUrl(), poolclass=NullPool)
        # create a configured "Session" class
        Session = sessionmaker(bind=engine)
        # create a Session
        session = Session()
        # runDay = datetime.date.today()
        runDay = datetime.datetime.strptime(start+'01', '%Y%m%d')
        # if runDay.day<10:
        #     runDay = getLastMonth(str(runDay.year)+str(runDay.month))
        #     runDay = getLastMonth(str(runDay.year)+str(runDay.month))
        # else:
        #     runDay = getLastMonth(str(runDay.year)+str(runDay.month))

        for i in range(0,before+1):
            for i in range(startCode,10000):
                stock_code = '{:04d}'.format(i)
                runYYMM = str(runDay.year)+str(runDay.month)
                print('get '+stock_code+' , '+runYYMM+' monthly revenue2')
                infoLog.log_dataBase('get '+stock_code+' , '+runYYMM+' monthly revenue start...')
                monthly_report(session,stock_code,runDay.year,runDay.month,infoLog)
                # 偽停頓
                time.sleep(2)
                infoLog.log_dataBase('get '+stock_code+' , '+runYYMM+' monthly revenue end...')
                print('get '+stock_code+' , '+runYYMM+' monthly revenue2 OK!!!')
            runDay = getLastMonth(runYYMM)
    except Exception as e:
        print(str(e))
        errorLog.log_dataBase('stock_code:'+stock_code+' , '+str(runDay.year)+str(runDay.month)+' monthly revenue Exception: '+str(e))
    finally:
        try:
            session.close()
        except Exception as e:
            return

if __name__ == "__main__":
    getAllMonthRevenue()