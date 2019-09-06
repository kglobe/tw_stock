# -*- coding: utf-8 -*-
"""
Created on Sun Jul  1 01:50:22 2018

@author: User
"""
import numpy
import pandas as pd
import datetime

def getDbUrl():
    return 'mysql+pymysql://root:1111@127.0.0.1:3306/db?charset=UTF8MB4'

def getDataFrameData(convertType,df,key):
    getValue = None
    try:
        getValue = df[key].replace(',', '')
    except Exception:
        getValue = df[key]

    try:
        getValue = eval(convertType)(getValue)
    except Exception:
        getValue = str(getValue)

    if pd.isnull(df[key]):
        return None
    
    if isinstance(df[key], str):
        if df[key].strip() == '-':
            return None
        elif df[key].strip() == '---':
            return None
        elif df[key].strip() == '----':
            return None

    return getValue

def getLastMonth(thisMonth):
    dataDate = datetime.datetime.strptime(thisMonth, '%Y%m')
    lastMonthYear = dataDate.year
    lastMonth = dataDate.month - 1
    if lastMonth == 0:
        lastMonth = 12
        lastMonthYear = lastMonthYear - 1
    last = datetime.datetime.strptime(str(lastMonthYear)+str(lastMonth), '%Y%m')
    return last

def toMinGuoYearByDatetime(fromDateTime):
    return toMinGuoYear(fromDateTime.year,fromDateTime.month,fromDateTime.day)

def toMinGuoYear(year,month,day):
    year = year - 1911
    if month < 10:
        month = '0'+str(month)
    if day < 10:
        day = '0'+str(day)
    return str(year)+'/'+str(month)+'/'+str(day)