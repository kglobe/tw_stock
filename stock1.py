# -*- coding: utf-8 -*-
"""
Created on Mon May 28 09:21:19 2018

@author: I26436
"""

import requests
from io import StringIO
import pandas as pd
import numpy as np

datestr = '20180629'
r = requests.post('http://www.twse.com.tw/exchangeReport/MI_INDEX?response=csv&date=' + datestr + '&type=ALL')
df = pd.read_csv(StringIO("\n".join([i.translate({ord(c): None for c in ' '}) 
                                     for i in r.text.split('\n') 
                                     if len(i.split('",')) == 17 and i[0] != '='])), header=0)

#拿掉最後一欄Unnamed: 16
df.drop(df.columns[df.shape[1]-1], axis=1, inplace=True)
df.to_excel('excel_output_df.xlsx')

#轉成數字來做本益比條件的index
numIndex = pd.to_numeric(df['本益比'], errors='coerce')
aa = df[(numIndex < 4) & (numIndex > 0)]
aa.to_excel('excel_output_aa.xlsx')

#用名稱查詢單一股票
df2 = df[df['證券名稱'] == '中鋼']
df2.to_excel('excel_output_df2.xlsx')

#用代碼查詢股票
df3 = df[df['證券代號'] == '2002']
df3.to_excel('excel_output_df3.xlsx')