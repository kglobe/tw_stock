select * from db.stock_price ;

select * from db.price_book_ratio order by priceDate;

select * from db.monthly_revenue where revenueMonth='201907';

select * from db.price_earnings_ratio where stockCode in (select stockCode from db.monthly_revenue where revenueMonth='201906' and compLastYear>0 and compLastAccRevenue>0) and PER<15;

select * from db.error_log where errorType='error' and msg like '%found%';

-- delete from db.error_log;