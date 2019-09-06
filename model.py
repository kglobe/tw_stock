from sqlalchemy import Column, Integer, String, Numeric
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

class stock_price(Base):
    __tablename__ = 'stock_price'
    priceDate = Column(String(8), primary_key=True, nullable=True)
    stockCode = Column(String(6), primary_key=True, nullable=True)
    tradingVolume = Column(Integer)
    turnover = Column(Integer)
    openPrice = Column(Numeric(precision=6, asdecimal=False, decimal_return_scale=None))
    highPrice = Column(Numeric(precision=6, asdecimal=False, decimal_return_scale=None))
    lowPrice = Column(Numeric(precision=6, asdecimal=False, decimal_return_scale=None))
    closePrice = Column(Numeric(precision=6, asdecimal=False, decimal_return_scale=None))
    priceLimit = Column(String(10))
    numOfTransactions = Column(Integer)
    meanPrice = Column(Numeric(precision=6, asdecimal=False, decimal_return_scale=None))
    lastBuyPrice = Column(Numeric(precision=6, asdecimal=False, decimal_return_scale=None))
    lastSellPrice = Column(Numeric(precision=6, asdecimal=False, decimal_return_scale=None))
    publicNum = Column(Integer)
    nextDayPrice = Column(Numeric(precision=6, asdecimal=False, decimal_return_scale=None))
    nextDayLimitUp = Column(Numeric(precision=6, asdecimal=False, decimal_return_scale=None))
    nextDayLimitDown = Column(Numeric(precision=6, asdecimal=False, decimal_return_scale=None))
    updateDate = Column(String(8))
    updatTime = Column(String(6))

class monthly_revenue(Base):
    __tablename__ = 'monthly_revenue'
    revenueMonth = Column(String(6), primary_key=True)
    stockCode = Column(String(6), primary_key=True)
    stockName = Column(String(500))
    thisMonthRevenue = Column(Integer)
    lastMonthRevenue = Column(Integer)
    lastYearRevenue = Column(Integer)
    compLastMonth = Column(Numeric(precision=2, asdecimal=False, decimal_return_scale=None))
    compLastYear = Column(Numeric(precision=2, asdecimal=False, decimal_return_scale=None))
    thisMonthAccRevenue = Column(Integer)
    lastYearAccRevenue = Column(Integer)
    compLastAccRevenue = Column(Integer)
    yoy = Column(Numeric(precision=6, asdecimal=False, decimal_return_scale=None))
    remarks = Column(String(500))
    updateDate = Column(String(8))
    updatTime = Column(String(6))
    
class price_earnings_ratio(Base):
    __tablename__ = 'price_earnings_ratio'
    priceDate = Column(String(8), primary_key=True, nullable=True)
    stockCode = Column(String(6), primary_key=True, nullable=True)
    stockName = Column(String(500))
    tradingVolume = Column(Integer)
    numOfTransactions = Column(Integer)
    turnover = Column(Integer)
    openPrice = Column(Numeric(precision=6, asdecimal=False, decimal_return_scale=None))
    highPrice = Column(Numeric(precision=6, asdecimal=False, decimal_return_scale=None))
    lowPrice = Column(Numeric(precision=6, asdecimal=False, decimal_return_scale=None))
    closePrice = Column(Numeric(precision=6, asdecimal=False, decimal_return_scale=None))
    upOrDown = Column(String(5))
    priceLimit = Column(Numeric(precision=6, asdecimal=False, decimal_return_scale=None))
    finalBuyPrice = Column(Numeric(precision=6, asdecimal=False, decimal_return_scale=None))
    finalBuyVolume = Column(Integer)
    finalSellPrice = Column(Numeric(precision=6, asdecimal=False, decimal_return_scale=None))
    finalSellVolume = Column(Integer)
    PER = Column(Numeric(precision=6, asdecimal=False, decimal_return_scale=None))
    updateDate = Column(String(8))
    updatTime = Column(String(6))

class check_stock_revenue(Base):
    __tablename__ = 'check_stock_revenue'
    priKey = Column(String(30), primary_key=True, nullable=True)
    stockCode = Column(String(6), primary_key=True, nullable=True)
    stockName = Column(String(500))
    updateDate = Column(String(8))
    updateTime = Column(String(6))

class price_book_ratio(Base):
    __tablename__ = 'price_book_ratio'
    priceDate = Column(String(8), primary_key=True, nullable=True)
    stockCode = Column(String(6), primary_key=True, nullable=True)
    stockName = Column(String(500))
    dividendYield = Column(Numeric(precision=6, asdecimal=False, decimal_return_scale=None))
    yearOfDividend = Column(String(10))
    PER = Column(Numeric(precision=6, asdecimal=False, decimal_return_scale=None))
    priceBookRatio = Column(Numeric(precision=6, asdecimal=False, decimal_return_scale=None))
    financialReport = Column(String(10))
    updateDate = Column(String(8))
    updateTime = Column(String(6))

class error_log(Base):
    __tablename__ = 'error_log'
    priKey = Column(String(30), primary_key=True, nullable=True)
    pyFile = Column(String(30))
    errorType = Column(String(6))
    msg = Column(String(500))
    updateDate = Column(String(8))
    updateTime = Column(String(6))