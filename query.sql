select * from db.stock_price where stockCode = '9904';

select priceDate,count(*) from db.stock_price group by priceDate order by priceDate desc;

select revenueMonth,count(*) from db.monthly_revenue group by revenueMonth order by revenueMonth desc;

select priceDate,count(*) from db.price_book_ratio group by priceDate order by priceDate desc;

select priceDate,count(*) from db.price_earnings_ratio group by priceDate order by priceDate desc;

select * from db.monthly_revenue where lastMonthRevenue=0 order by revenueMonth desc;

select * from db.monthly_revenue where revenueMonth='20199';

select * from db.price_book_ratio order by priceDate desc;

select * from db.price_earnings_ratio where stockCode in (select stockCode from db.monthly_revenue where revenueMonth='201906' and compLastYear>0 and compLastAccRevenue>0) and PER<15;

select * from db.price_earnings_ratio order by priceDate desc;

select * from db.error_log where pyFile='price_book_ratio2' order by prikey desc;

select * from db.error_log order by prikey desc;

-- delete from db.error_log;