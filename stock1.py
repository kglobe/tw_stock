# -*- coding: utf-8 -*-
"""
Created on Mon May 28 09:21:19 2018

@author: I26436
"""

import requests
from io import StringIO
import pandas as pd
import numpy as np
datestr = '20180525'
r = requests.post('http://www.twse.com.tw/exchangeReport/MI_INDEX?response=csv&date=' + datestr + '&type=ALL')
df = pd.read_csv(StringIO("\n".join([i.translate({ord(c): None for c in ' '}) 
                                     for i in r.text.split('\n') 
                                     if len(i.split('",')) == 17 and i[0] != '='])), header=0)

##本益比超過15的
df[pd.to_numeric(df['本益比'], errors='coerce') < 15]
	
df = df.set_index(['公司名稱'])
