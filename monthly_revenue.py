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
from model import monthly_revenue
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from utility import getDbUrl
from sqlalchemy.pool import NullPool

def monthly_report(session, year, month, infoLog):
    
    # 假如是西元，轉成民國
    if year > 1990:
        year -= 1911
    
    url = 'https://mops.twse.com.tw/nas/t21/sii/t21sc03_'+str(year)+'_'+str(month)+'_0.html'
    if year <= 98:
        url = 'https://mops.twse.com.tw/nas/t21/sii/t21sc03_'+str(year)+'_'+str(month)+'.html'
    
    # 偽瀏覽器
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    
    # 下載該年月的網站，並用pandas轉換成 dataframe
    r = requests.get(url, headers=headers)
    r.encoding = 'big5'
    html_df = pd.read_html(StringIO(r.text))
    # 處理一下資料
    if html_df[0].shape[0] > 500:
        df = html_df[0].copy()
    else:
        df = pd.concat([df for df in html_df if df.shape[1] <= 11])
    df = df[list(range(0,10))]
    column_index = df.index[(df[0] == '公司代號')][0]
    df.columns = df.iloc[column_index]
    df['當月營收'] = pd.to_numeric(df['當月營收'], 'coerce')
    df['上月營收'] = pd.to_numeric(df['上月營收'], 'coerce')
    df['去年當月營收'] = pd.to_numeric(df['去年當月營收'], 'coerce')
    df['上月比較增減(%)'] = pd.to_numeric(df['上月比較增減(%)'], 'coerce')
    df['去年同月增減(%)'] = pd.to_numeric(df['去年同月增減(%)'], 'coerce')
    df['當月累計營收'] = pd.to_numeric(df['當月累計營收'], 'coerce')
    df['去年累計營收'] = pd.to_numeric(df['去年累計營收'], 'coerce')
    df['前期比較增減(%)'] = pd.to_numeric(df['前期比較增減(%)'], 'coerce')
    df = df[~df['當月營收'].isnull()]
    df = df[df['公司代號'] != '合計']
    df['累積年增率'] = pd.Series((df['當月累計營收']-df['去年累計營收'])/df['當月累計營收'], index=df.index)
    year = year+1911
    month = '{:02d}'.format(month)
    # print(df.describe())
    # return
    print('----insert '+str(year)+str(month)+' monthly revenue----')
    for i in range(0,df.shape[0]):
        updatedate = datetime.datetime.now().strftime('%Y%m%d')
        updatetime = datetime.datetime.now().strftime('%H%M%S')
        
        mr = monthly_revenue()
        mr.revenueMonth = str(year)+str(month)
        mr.stockCode = df.iloc[i]['公司代號']
        mr.stockName = df.iloc[i]['公司名稱']
        mr.thisMonthRevenue = float(df.iloc[i]['當月營收']) if np.isnan(df.iloc[i]['當月營收'])==False else None
        mr.lastMonthRevenue = float(df.iloc[i]['上月營收']) if np.isnan(df.iloc[i]['上月營收'])==False else None
        mr.lastYearRevenue = float(df.iloc[i]['去年當月營收']) if np.isnan(df.iloc[i]['去年當月營收'])==False else None
        mr.compLastMonth = float(df.iloc[i]['上月比較增減(%)']) if np.isnan(df.iloc[i]['上月比較增減(%)'])==False else None
        mr.compLastYear = float(df.iloc[i]['去年同月增減(%)']) if np.isnan(df.iloc[i]['去年同月增減(%)'])==False else None
        mr.thisMonthAccRevenue = float(df.iloc[i]['當月累計營收']) if np.isnan(df.iloc[i]['當月累計營收'])==False else None
        mr.lastYearAccRevenue = float(df.iloc[i]['去年累計營收']) if np.isnan(df.iloc[i]['去年累計營收'])==False else None
        mr.compLastAccRevenue = float(df.iloc[i]['前期比較增減(%)']) if np.isnan(df.iloc[i]['前期比較增減(%)'])==False else None
        mr.yoy = float(round(df.iloc[i]['累積年增率'],6)) if np.isnan(df.iloc[i]['累積年增率'])==False else None
        mr.updateDate = updatedate
        mr.updatTime = updatetime
        session.merge(mr)
    session.commit()
    print('----insert '+str(year)+str(month)+' monthly revenue ok----')
    infoLog.log_dataBase(str(year)+str(month)+' monthly_revenue commit ok!')
    
    # return df

# 民國100年1月
#monthly_report(100,1)
# 西元2011年1月
# print(monthly_report(2011,1))
# df = monthly_report(2019,1)
# fliter = (df["公司代號"] == "2330")
# df = df[fliter]
# print(df)
# df2 = monthly_report(2019,2)
# fliter2 = (df2["公司代號"] == "2330")
# df2 = df2[fliter2]
# print(df2)
# df = df.append(df2, ignore_index=True)

# df3 = monthly_report(2019,3)
# fliter3 = (df3["公司代號"] == "2330")
# df3 = df3[fliter3]
# df = df.append(df3, ignore_index=True)
# print(df)
# with open('2330FILE.csv', 'w') as f:
#     f.writelines(df)

def getAllMonthRevenue():
    errorLog = LogTool('stock_price','error')
    infoLog = LogTool('stock_price','info')
    try:
        engine = create_engine(getDbUrl(), poolclass=NullPool)
        # create a configured "Session" class
        Session = sessionmaker(bind=engine)
        # create a Session
        session = Session()
        for yy in range(2010,2019):
            for mm in range(1,12):
                print('get '+str(yy)+str(mm)+' monthly revenue')
                infoLog.log_dataBase('get '+str(yy)+str(mm)+' monthly revenue start...')
                monthly_report(session,yy,mm,infoLog)
                # 偽停頓
                time.sleep(5)
                infoLog.log_dataBase('get '+str(yy)+str(mm)+' monthly revenue end...')
    except Exception as e:
        print(str(e))
        errorLog.log_dataBase(str(yy)+str(mm)+' monthly revenue Exception: '+str(e))
    finally:
        try:
            session.close()
        except Exception as e:
            return

if __name__ == '__main__':
    getAllMonthRevenue()