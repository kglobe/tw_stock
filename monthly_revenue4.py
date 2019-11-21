# -*- coding: utf-8 -*-
"""
Created on Sun Jul  1 01:50:22 2018

@author: User
"""
import numpy as np
import datetime
import pandas as pd
import requests
import xlrd
import urllib
from io import StringIO
import time
from log_tool import LogTool
from model import monthly_revenue
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from utility import getDbUrl, getLastMonth
from sqlalchemy.pool import NullPool

# def getYoYData(lastYearAccRevenue,thisMonthAccRevenue):
#     if float(lastYearAccRevenue) == 0:
#         yoyComp = 0
#     else:
#         yoyComp = (thisMonthAccRevenue-lastYearAccRevenue)/lastYearAccRevenue
    
#     return yoyDf

def getConvertData(convertType,input):
    try:
        getValue = eval(convertType)(input)
    except Exception:
        getValue = str(input)

    return getValue

def getCompLastMonth(mr):
    try:
        if float(mr.lastMonthRevenue) == 0:
            return 0
        else:
            return (mr.thisMonthRevenue-mr.lastMonthRevenue)*100/mr.lastMonthRevenue
    except Exception as e:
        print(str(e))
        return 0

def getCompLastYear(mr):
    try:
        if float(mr.lastYearRevenue) == 0:
            return 0
        else:
            return (mr.thisMonthRevenue-mr.lastYearRevenue)*100/mr.lastYearRevenue
    except Exception as e:
        print(str(e))
        return 0

def monthly_report(session, year, month, infoLog):
    
    if month<10:
        url = 'https://www.tpex.org.tw/storage/statistic/sales_revenue/O_'+str(year)+'0'+str(month)+'.xls'
    else:
        url = 'https://www.tpex.org.tw/storage/statistic/sales_revenue/O_'+str(year)+str(month)+'.xls'
    
    # 偽瀏覽器
    # headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36'}
    
    try:
        s = requests.Session()
        s.config = {'keep_alive': False}
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Connection': 'close',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36'
        }
        r = requests.get(url, headers=headers,  timeout=5, allow_redirects=True)
        r.encoding = 'BIG5'
        with open('D:/O_'+str(year)+str(month)+'.xls', 'wb') as f:
            f.write(r.content)
        
    except Exception as e:
        print(str(year)+str(month)+' 抓資料有問題：'+str(e)+' , '+url)
        infoLog.log_dataBase('requests '+str(year)+'_'+str(month)+' monthly report ratio Exception: '+str(e)+' , '+url)
    finally:
        s.close()
        print('Session closed!')
        # return

    workbook = xlrd.open_workbook('D:/O_'+str(year)+str(month)+'.xls')
    sheets = workbook.sheets()
    for sheet in sheets:
        num_rows = sheet.nrows
        curr_row = -1
        while curr_row < num_rows:
            curr_row += 1
            try:
                row = sheet.row(curr_row)
            except Exception :
                break
            cell_type = sheet.cell_type(curr_row, 0)
            if cell_type == 1:
                cell_value = sheet.cell_value(curr_row, 0)
                if cell_value[:4].isnumeric():
                    updatedate = datetime.datetime.now().strftime('%Y%m%d')
                    updatetime = datetime.datetime.now().strftime('%H%M%S')
                    
                    mr = monthly_revenue()
                    mr.revenueMonth = str(year)+str(month).zfill(2)
                    mr.stockCode = getConvertData('str',cell_value[:4])
                    mr.stockName = getConvertData('str',cell_value[5:])
                    cell_value = sheet.cell_value(curr_row, 2)
                    mr.lastMonthRevenue = getConvertData('float',cell_value)
                    cell_value = sheet.cell_value(curr_row, 3)
                    mr.thisMonthRevenue = getConvertData('float',cell_value)
                    cell_value = sheet.cell_value(curr_row, 5)
                    mr.lastYearRevenue = getConvertData('float',cell_value)
                    mr.compLastMonth = round(getCompLastMonth(mr),6)
                    mr.compLastYear = round(getCompLastYear(mr),6)
                    cell_value = sheet.cell_value(curr_row, 4)
                    mr.thisMonthAccRevenue = getConvertData('float',cell_value)
                    cell_value = sheet.cell_value(curr_row, 6)
                    mr.lastYearAccRevenue = getConvertData('float',cell_value)
                    cell_value = sheet.cell_value(curr_row, 8)
                    if cell_value == 'NA' or cell_value == '':
                        mr.yoy = None
                        mr.compLastMonth = None
                    else:
                        mr.yoy = round(getConvertData('float',cell_value),6)/100
                        mr.compLastMonth = round(getConvertData('float',cell_value),6)
                    mr.updateDate = updatedate
                    mr.updatTime = updatetime
                    session.merge(mr)

    session.commit()
    print('----insert '+str(year)+str(month)+' monthly revenue ok----')
    infoLog.log_dataBase(str(year)+str(month)+' monthly_revenue commit ok!')

def getAllMonthRevenue():
    start = input("請輸入起始年月(Ex:201901)：")
    before = int(input("請輸入往前抓幾個月？："))
    errorLog = LogTool('monthly_revenue','error')
    infoLog = LogTool('monthly_revenue','info')
    try:
        engine = create_engine(getDbUrl(), poolclass=NullPool)
        # create a configured "Session" class
        Session = sessionmaker(bind=engine)
        # create a Session
        session = Session()
        # runDay = datetime.date.today()
        # if runDay.day<10:
        #     runDay = getLastMonth(str(runDay.year)+str(runDay.month))
        #     runDay = getLastMonth(str(runDay.year)+str(runDay.month))
        # else:
        #     runDay = getLastMonth(str(runDay.year)+str(runDay.month))
        
        runDay = datetime.datetime.strptime(start+'01', '%Y%m%d')
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