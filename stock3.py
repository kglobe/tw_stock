# -*- coding: utf-8 -*-
"""
Created on Wed Jun 27 00:45:38 2018

@author: User
"""

import requests
import json
import pandas as pd
resp = requests.get('http://www.twse.com.tw/exchangeReport/STOCK_DAY?response=json&date=201806&stockNo=2002')
data = resp.json()
jsonData = json.dumps(data, sort_keys=True, indent=4, separators=(',', ': '))
df = pd.Series(data)
print(df['data'])