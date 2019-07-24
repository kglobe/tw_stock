select * from db.stock_price;

select * from db.stock_price where stockCOde='2002' and priceDate='20190701';

select * from db.monthly_revenue where revenueMonth='201901';

select count(*) from db.monthly_revenue where revenueMonth='201901' and compLastYear>0 and compLastAccRevenue>0 and 
stockCode in (select stockCode from db.monthly_revenue where revenueMonth='201902' and compLastYear>0 and compLastAccRevenue>0 and 
stockCode in (select stockCode from db.monthly_revenue where revenueMonth='201903' and compLastYear>0 and compLastAccRevenue>0 and 
stockCode in (select stockCode from db.monthly_revenue where revenueMonth='201904' and compLastYear>0 and compLastAccRevenue>0 and 
stockCode in (select stockCode from db.monthly_revenue where revenueMonth='201905' and compLastYear>0 and compLastAccRevenue>0 and 
stockCode in (select stockCode from db.monthly_revenue where revenueMonth='201906' and compLastYear>0 and compLastAccRevenue>0)))));

select * from db.price_earnings_ratio where stockCode in (select stockCode from db.monthly_revenue where revenueMonth='201906' and compLastYear>0 and compLastAccRevenue>0) and priceDate='20190719' and PER<15;

select SUBSTR(revenueMonth,1,4),stockCode,count(*) from db.monthly_revenue group by SUBSTR(revenueMonth,1,4),stockCode;

select * from db.error_log where errorType='error' and msg like '%found%';

-- delete from db.error_log;