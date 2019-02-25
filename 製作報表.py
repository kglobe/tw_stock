import datetime
import time
import requests
import datetime
import sys
import pandas as pd
from io import StringIO

def monthly_report(year, month):
    
    # 假如是西元，轉成民國
    if year > 1990:
        year -= 1911
    
    url = 'http://mops.twse.com.tw/nas/t21/sii/t21sc03_'+str(year)+'_'+str(month)+'_0.html'
    if year <= 98:
        url = 'http://mops.twse.com.tw/nas/t21/sii/t21sc03_'+str(year)+'_'+str(month)+'.html'
    
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
    df = df[~df['當月營收'].isnull()]
    df = df[df['公司代號'] != '合計']
    
    # 偽停頓
    time.sleep(6)
    return df

def price(stock_code):
    start = datetime.datetime(1970, 1, 1, 0, 0, 0)
    nowTime = datetime.datetime.now()
    period2 = str(round(((nowTime-start).total_seconds())))
    site = "https://query1.finance.yahoo.com/v7/finance/download/"+stock_code+".TW?period1=0&period2="+period2+"&interval=1d&events=history&crumb=hP2rOschxO0"
    response = requests.post(site)
    with open(stock_code+'.csv', 'w') as f:
        f.writelines("\n")
        f.writelines("\n")
        f.writelines(response.text)

# def main(stock_code):
stock_code = '2002'
data = 1
n_month = 3
now = datetime.datetime.now()

year = now.year
month = now.month-1

print('run month:', year, month)
df = monthly_report(year,month)
fliter = (df["公司代號"] == stock_code)
df = df[fliter]

while data < n_month:
    # 減一個月
    month -= 1
    if month == 0:
        month = 12
        year -= 1
    
    data = data + 1
    print('run month:', year, month)
    df2 = monthly_report(year,month)
    fliter2 = (df2["公司代號"] == stock_code)
    df2 = df2[fliter2]
    df = df.append(df2, ignore_index=True)

df.to_csv(stock_code+'.csv', encoding='utf8')
price(stock_code)

# if __name__ == '__main__':
#     main(sys.argv[1])