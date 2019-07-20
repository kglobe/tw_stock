import pandas as pd

def getDbUrl():
    return 'mysql+pymysql://root:1111@127.0.0.1:3306/db?charset=UTF8MB4'

def getDataFrameData(convertType,df,key):
    getValue = None
    if pd.isnull(df[key]):
        return None
    else:
        try:
            getValue = df[key].replace(',', '')
        except Exception:
            getValue = df[key]

        try:
            getValue = eval(convertType)(getValue)
        except Exception:
            getValue = str(getValue)
    if getValue == '--':
        getValue = None

    return getValue