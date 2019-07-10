CREATE TABLE db.stock_price (
  priceDate date not null,
  stockCode varchar(6) not null,
  openPrice DECIMAL(12,6),
  highPrice DECIMAL(12,6),
  lowPrice DECIMAL(12,6),
  closePrice DECIMAL(12,6),
  adj_close DECIMAL(12,6),
  volume DECIMAL(56,6),
  updateDate varchar(8),
  updatTime varchar(6),
  PRIMARY KEY (priceDate,stockCode)
);

CREATE TABLE db.monthly_revenue (
  revenueMonth varchar(6) not null,
  stockCode varchar(6) not null,
  stockName varchar(500) COLLATE utf8mb4_unicode_ci ,
  thisMonthRevenue DECIMAL(21,6),
  lastMonthRevenue DECIMAL(21,6),
  lastYearRevenue DECIMAL(21,6),
  compLastMonth DECIMAL(12,6),
  compLastYear DECIMAL(12,6),
  thisMonthAccRevenue DECIMAL(21,6),
  lastYearAccRevenue DECIMAL(21,6),
  compLastAccRevenue DECIMAL(21,6),
  yoy DECIMAL(12,6),
  remarks varchar(500) COLLATE utf8mb4_unicode_ci ,
  updateDate varchar(8),
  updatTime varchar(6),
  PRIMARY KEY (revenueMonth,stockCode)
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