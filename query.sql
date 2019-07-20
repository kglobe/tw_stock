select * from db.stock_price order by priceDate desc;

select * from db.monthly_revenue where revenueMonth='';

select SUBSTR(revenueMonth,1,4),stockCode,count(*) from db.monthly_revenue group by SUBSTR(revenueMonth,1,4),stockCode;

select * from db.error_log where errorType='error' and msg like '%found%';

-- delete from db.error_log;