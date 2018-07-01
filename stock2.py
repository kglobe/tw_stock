# -*- coding: utf-8 -*-
"""
Created on Mon May 28 09:26:22 2018

@author: I26436
"""

import requests
import pandas as pd
import numpy as np
def financial_statement(year, season, reportType):
    if year >= 1000:
        year -= 1911
        
    if reportType == '綜合損益彙總表':
        url = 'http://mops.twse.com.tw/mops/web/ajax_t163sb04'
    elif reportType == '資產負債彙總表':
        url = 'http://mops.twse.com.tw/mops/web/ajax_t163sb05'
    elif reportType == '營益分析彙總表':
        url = 'http://mops.twse.com.tw/mops/web/ajax_t163sb06'
    else:
        print('type does not match')
    r = requests.post(url, {
        'encodeURIComponent':1,
        'step':1,
        'firstin':1,
        'off':1,
        'TYPEK':'sii',
        'year':str(year),
        'season':str(season),
    })
    
    r.encoding = 'utf8'
    dfs = pd.read_html(r.text)
    
    
    for i, df in enumerate(dfs):
        df.columns = df.iloc[0]
        dfs[i] = df.iloc[1:]
        
    df = pd.concat(dfs).applymap(lambda x: x if x != '--' else np.nan)
    df = df[df['公司代號'] != '公司代號']
    df = df[~df['公司代號'].isnull()]
    
    #拿掉D欄
    if reportType == '營益分析彙總表':
        df.drop(df.columns[2], axis=1, inplace=True)
        
    return df

def getCompByCompCode(df,compCode):
    return df[df['公司代號']==compCode]

#取得毛利率(%)(營業毛利)/(營業收入)
def getGrossMarginValue(df):
    Gross_Margin = pd.to_numeric(df['毛利率(%)(營業毛利)/(營業收入)'], errors='coerce')
    try:
        return float(Gross_Margin.values[0])
    except Exception as e:
        return float(0) 

#取得營業利益率(%)(營業利益)/(營業收入)
def getOperatingProfitMarginValue(df):
    Operating_Profit_Margin = pd.to_numeric(df['營業利益率(%)(營業利益)/(營業收入)'], errors='coerce')
    try:
        return float(Operating_Profit_Margin.values[0])
    except Exception as e:
        return float(0) 

#取得營業收入(百萬元)
def getOperatingIncomeValue(df):
    Operating_Income = pd.to_numeric(df['營業收入(百萬元)'], errors='coerce')
    try:
        return float(Operating_Income.values[0])
    except Exception as e:
        return float(0) 

#取得稅前純益率(%)(稅前純益)/(營業收入)
def getPreTaxProfitMarginValue(df):
    Pre_Tax_Profit_Margin = pd.to_numeric(df['稅前純益率(%)(稅前純益)/(營業收入)'], errors='coerce')
    try:
        return float(Pre_Tax_Profit_Margin.values[0])
    except Exception as e:
        return float(0)
    
#取得稅後純益率(%)(稅後純益)/(營業收入)
def getNetAfterTaxProfitMarginValue(df):
    Net_After_Tax_Profit_Margin = pd.to_numeric(df['稅後純益率(%)(稅後純益)/(營業收入)'], errors='coerce')
    try:
        return float(Net_After_Tax_Profit_Margin.values[0])
    except Exception as e:
        return float(0)

df_new = financial_statement(2018,1,'營益分析彙總表')
df_old = financial_statement(2017,1,'營益分析彙總表')
#df_new.to_excel('excel_output2_df_new.xlsx')
#df_old.to_excel('excel_output2_df_old.xlsx')

for compCode in df_new['公司代號']:
    compNew = getCompByCompCode(df_new,compCode)
    compOld = getCompByCompCode(df_old,compCode)
    Profit_After_Tax_new = getNetAfterTaxProfitMarginValue(compNew)
    Profit_After_Tax_old = getNetAfterTaxProfitMarginValue(compOld)
    if ((Profit_After_Tax_old > 0) & (Profit_After_Tax_new - Profit_After_Tax_old > 20)):
        print(compCode)
