
from datetime import datetime, timedelta

year = 2019
month = 11
day = 5
hour = 11
minute = 10
second = 00

t1 = datetime(year, month, day, hour, minute, second)

#t1 = datetime.now()

t2 = datetime.timestamp(t1) * 1000

print (t1)
print (t2)

