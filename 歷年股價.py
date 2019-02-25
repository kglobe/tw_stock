import requests
import datetime
import sys

def main(stock_code):
    start = datetime.datetime(1970, 1, 1, 0, 0, 0)
    nowTime = datetime.datetime.now()
    period2 = str(round(((nowTime-start).total_seconds())))
    site = "https://query1.finance.yahoo.com/v7/finance/download/"+stock_code+".TW?period1=0&period2="+period2+"&interval=1d&events=history&crumb=hP2rOschxO0"
    response = requests.post(site)
    with open(stock_code+'.csv', 'w') as f:
        f.writelines(response.text)

if __name__ == '__main__':
#     main(sys.argv[1])
        main('1402')