# -*- coding: utf-8 -*-
"""
Created on Sun Jul  1 18:50:40 2018

@author: User
"""
import requests
import pandas as pd
import numpy as np

#營業收入統計表
def OperatingIncomeReport(co_id):
    url = 'http://mops.twse.com.tw/mops/web/ajax_t146sb05'
    r = requests.post(url, {
            'encodeURIComponent':1,
            'step':2,
            'firstin':1,
            'off':1,
            'queryName': 'co_id',
            'inpuType': 'co_id',
            'TYPEK': 'all',
            'co_id': co_id,
        })
    r.encoding = 'utf8'
    dfs = pd.read_html(r.text)
    dfs = dfs[1]
    dfs = dfs.iloc[2:]
    dfs = dfs.reset_index(drop=True)
    dfs = dfs.rename(index=str, columns={0: '年度', 1: '月份', 2: '當月營收', 3: '去年當月營收', 4: '去年同月增減(%)', 5: '當月累計營收', 6: '去年累計營收', 7: '前期比較增減(%)'})
    return dfs
    
dfs = OperatingIncomeReport('2002')
dfs.to_excel('excel_output_營業收入統計表.xlsx')