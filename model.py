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
    revenueMonth = Column(String(6), primary_key=True, nullable=True)
    stockCode = Column(String(6), primary_key=True, nullable=True)
    stockName = Column(String(500))
    thisMonthRevenue = Column(String(21))
    lastMonthRevenue = Column(String(21))
    lastYearRevenue = Column(String(21))
    compLastMonth = Column(String(12))
    compLastYear = Column(String(12))
    thisMonthAccRevenue = Column(String(21))
    lastYearAccRevenue = Column(String(21))
    compLastAccRevenue = Column(String(21))
    yoy = Column(String(12))
    remarks = Column(String(500))
    updateDate = Column(String(8))
    updatTime = Column(String(6))

class error_log(Base):
    __tablename__ = 'error_log'
    prikey = Column(String(30), primary_key=True, nullable=True)
    pyFile = Column(String(30))
    errorType = Column(String(6))
    msg = Column(String(500))
    updateDate = Column(String(8))
    updatTime = Column(String(6))