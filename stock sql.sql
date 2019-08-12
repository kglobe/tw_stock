CREATE TABLE db.stock_price (
  priceDate date not null, /*交易日期*/
  stockCode varchar(6) not null, /*股票代碼*/
  tradingVolume DECIMAL(56,6), /*成交股數*/
  turnover DECIMAL(21,6), /*成交金額*/
  openPrice DECIMAL(12,6), /*開盤價*/
  highPrice DECIMAL(12,6), /*最高價*/
  lowPrice DECIMAL(12,6), /*最低價*/
  closePrice DECIMAL(12,6), /*收盤價*/
  priceLimit varchar(10), /*漲跌價差*/
  numOfTransactions DECIMAL(21,6), /*成交筆數*/
  updateDate varchar(8), /*更新日期*/
  updatTime varchar(6), /*更新時間*/
  PRIMARY KEY (priceDate,stockCode)
);

CREATE TABLE db.monthly_revenue (
  revenueMonth varchar(6) not null, /*營收年月*/
  stockCode varchar(6) not null, /*公司代號(證券代號)*/
  stockName varchar(500) COLLATE utf8mb4_unicode_ci , /*公司名稱(證券名稱)*/
  thisMonthRevenue DECIMAL(21,6), /*當月營收*/
  lastMonthRevenue DECIMAL(21,6), /*上月營收*/
  lastYearRevenue DECIMAL(21,6), /*去年當月營收*/
  compLastMonth DECIMAL(21,6), /*上月比較增減(%)*/
  compLastYear DECIMAL(21,6), /*去年同月增減(%)*/
  thisMonthAccRevenue DECIMAL(21,6), /*當月累計營收*/
  lastYearAccRevenue DECIMAL(21,6), /*去年累計營收*/
  compLastAccRevenue DECIMAL(21,6), /*前期比較增減(%)*/
  yoy DECIMAL(21,6), /*累積年增率*/
  remarks varchar(500) COLLATE utf8mb4_unicode_ci , /*註解*/
  updateDate varchar(8), /*更新日期*/
  updatTime varchar(6), /*更新時間*/
  PRIMARY KEY (revenueMonth,stockCode)
);

CREATE TABLE db.price_earnings_ratio (
  priceDate date not null, /*交易日期*/
  stockCode varchar(6) not null, /*證券代號*/
  stockName varchar(500) COLLATE utf8mb4_unicode_ci , /*證券名稱*/
  tradingVolume DECIMAL(21,6), /*成交股數*/
  numOfTransactions DECIMAL(21,6), /*成交筆數*/
  turnover DECIMAL(21,6), /*成交金額*/
  openPrice DECIMAL(12,6), /*開盤價*/
  highPrice DECIMAL(12,6), /*最高價*/
  lowPrice DECIMAL(12,6), /*最低價*/
  closePrice DECIMAL(12,6), /*最低價*/
  upOrDown varchar(5), /*漲跌(+/-)*/
  priceLimit DECIMAL(12,6), /*漲跌價差*/
  finalBuyPrice DECIMAL(12,6), /*最後揭示買價*/
  finalBuyVolume DECIMAL(21,6), /*最後揭示買量*/
  finalSellPrice DECIMAL(21,6), /*最後揭示賣價*/
  finalSellVolume DECIMAL(21,6), /*最後揭示賣量*/
  PER DECIMAL(21,6), /*本益比*/
  updateDate varchar(8), /*更新日期*/
  updatTime varchar(6), /*更新時間*/
  PRIMARY KEY (priceDate,stockCode)
);

CREATE TABLE db.check_stock_revenue( /*用來記錄抓出來的每檔股票紀錄*/
  priKey varchar(30) not null,
  stockCode varchar(6) not null, /*證券代號*/
  stockName varchar(500) COLLATE utf8mb4_unicode_ci , /*證券名稱*/
  updateDate varchar(8),
  updateTime varchar(6),
  PRIMARY KEY (prikey,stockCode)
);

CREATE TABLE db.price_book_ratio (
  priceDate date not null, /*交易日期*/
  stockCode varchar(6) not null, /*證券代號*/
  stockName varchar(500) COLLATE utf8mb4_unicode_ci , /*證券名稱*/
  dividendYield DECIMAL(21,6), /*殖利率(%)*/
  yearOfDividend varchar(10), /*股利年度*/
  PER DECIMAL(21,6), /*本益比*/
  priceBookRatio DECIMAL(21,6), /*股價淨值比*/
  financialReport varchar(10), /*財報年/季*/
  updateDate varchar(8), /*更新日期*/
  updateTime varchar(6), /*更新時間*/
  PRIMARY KEY (priceDate,stockCode)
);

CREATE TABLE db.error_log (
  priKey varchar(30) not null,
  pyFile varchar(30),
  errorType varchar(6),
  msg varchar(500),
  updateDate varchar(8),
  updateTime varchar(6),
  PRIMARY KEY (prikey)
);

CREATE TABLE db.stock_score (
  priKey varchar(30) not null,
  stockCode varchar(6) not null, /*證券代號*/
  stockName varchar(500) COLLATE utf8mb4_unicode_ci , /*證券名稱*/
  score DECIMAL(21,6), /*得分*/
  updateDate varchar(8),
  updateTime varchar(6),
  PRIMARY KEY (prikey)
);

ALTER TABLE db.error_log ADD INDEX (prikey);