import datetime

from chinese_calendar import is_workday
da = datetime.date.today()
print(da)
boll = is_workday(da)
print(boll)