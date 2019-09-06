select * from db.stock_price where stockCode like '9904';

select priceDate,count(*) from db.stock_price group by priceDate order by priceDate;

select revenueMonth,count(*) from db.monthly_revenue group by revenueMonth order by revenueMonth desc;

select priceDate,count(*) from db.price_book_ratio group by priceDate order by priceDate;

select priceDate,count(*) from db.price_earnings_ratio group by priceDate order by priceDate desc;

select * from db.monthly_revenue where revenueMonth>'201806' and yoy>0.5;

select * from db.monthly_revenue where stockcode='2732' order by revenueMonth desc;

select * from db.price_book_ratio where stockcode is null;

select * from db.price_earnings_ratio where stockCode in (select stockCode from db.monthly_revenue where revenueMonth='201906' and compLastYear>0 and compLastAccRevenue>0) and PER<15;

select * from db.price_earnings_ratio where stockCode='6558' order by priceDate;

select * from db.error_log where pyFile='price_book_ratio2' order by prikey desc;

select * from db.error_log order by prikey desc;

-- delete from db.error_log;