import datetime
import re
# start = input("請輸入起始日期(Ex:20190101)：")
# before = input("請輸入往前抓幾天？：")
# fromDate = datetime.datetime.strptime(start, '%Y%m%d')
# print(fromDate)
# add = fromDate + datetime.timedelta(days=-1)
# print(add)
# today = datetime.date.today()
# print(today)
# yes = today + datetime.timedelta(days=-1)
# print(yes)

#########################################

# dataDate = datetime.datetime.strptime('201901', '%Y%m')
# print(dataDate.strftime("%Y%m"))
# lastMonthYear = dataDate.year
# lastMonth = dataDate.month - 1
# if lastMonth == 0:
#     lastMonth = 12
#     lastMonthYear = lastMonthYear - 1
# last = datetime.datetime.strptime(str(lastMonthYear)+str(lastMonth), '%Y%m')
# print(last.strftime("%Y%m"))

#########################################

# runDay = datetime.date.today()
# print(runDay.year)
# print(runDay.month)
# print(runDay.day)
# dataDate = datetime.datetime.strptime('20190825', '%Y%m%d')
# print(dataDate)

print(len(re.findall(r'[\u4e00-\u9fa5]', '群益中國政金債')))
print(re.findall(r'[\u4e00-\u9fa5]', '00695B'))