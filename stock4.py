# -*- coding: utf-8 -*-
"""
Created on Sun Jul  1 01:30:35 2018

@author: User
"""

url = 'http://mops.twse.com.tw/mops/web/ajax_t146sb05'
r = requests.post(url, {
        'encodeURIComponent':1,
        'step':1,
        'firstin':1,
        'off':1,
        'TYPEK':'sii',
        'co_id':'2002',
    })