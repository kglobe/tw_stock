# -*- coding: utf-8 -*-
"""
Created on Wed Jun 27 00:45:38 2018

@author: User
"""
import numpy as np
import requests
import json
import pandas as pd
resp = requests.get('http://www.twse.com.tw/exchangeReport/STOCK_DAY?response=json&date=20186&stockNo=2002')
resp_data = resp.json()
print(resp_data['stat'])
df = pd.DataFrame(np.array(resp_data['data']), columns=np.array(resp_data['fields']))
print(df['漲跌價差'])
# jsondf = pd.Series(data)
# for row in jsondf.data:

# print(jsondf)