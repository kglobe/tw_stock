from sqlalchemy import Column, Integer, String, Numeric
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

class stock_price(Base):
    __tablename__ = 'stock_price'
    priceDate = Column(String(8), primary_key=True, nullable=True)
    stockCode = Column(String(6), primary_key=True, nullable=True)
    openPrice = Column(Numeric(precision=6, asdecimal=False, decimal_return_scale=None))
    highPrice = Column(Numeric(precision=6, asdecimal=False, decimal_return_scale=None))
    lowPrice = Column(Numeric(precision=6, asdecimal=False, decimal_return_scale=None))
    closePrice = Column(Numeric(precision=6, asdecimal=False, decimal_return_scale=None))
    adj_close = Column(Numeric(precision=6, asdecimal=False, decimal_return_scale=None))
    volume = Column(Integer)
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

class error_log(Base):
    __tablename__ = 'error_log'
    priKey = Column(String(30), primary_key=True, nullable=True)
    pyFile = Column(String(30))
    errorType = Column(String(6))
    msg = Column(String(500))
    updateDate = Column(String(8))
    updateTime = Column(String(6))