# -*- coding: utf-8 -*-
"""
Created on Tue Jul  3 00:13:48 2018

@author: User
"""
import pandas as pd
import requests

#集保戶股權分散表
def getTdccData(qryDate,stockNo):
    headers = {'Content-type': 'application/x-www-form-urlencoded;charset=UTF8'}
    url = 'https://www.tdcc.com.tw/smWeb/QryStock.jsp'
    #url = 'https://www.tdcc.com.tw/smWeb/QryStockAjax.do'
    r = requests.post(url, headers=headers, data={
            'scaDates':str(qryDate),
            'scaDate':str(qryDate),
            'SqlMethod':'StockNo',
            'StockNo':str(stockNo),
            'StockName':'',
            'REQ_OPR': 'qryStockNo',
            'clkStockNo': str(stockNo),
            'clkStockName': '',
        })
    r.encoding = 'big5'
    print(r.text)
    #dfs = pd.read_html(r.text)
    #print(dfs)
    
getTdccData('201800629','2002')