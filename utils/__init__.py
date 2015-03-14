from datetime import date, timedelta, datetime
import time
import random

def get_week_days(year, week):
    d = date(year,1,1)
    if(d.weekday()>3):
        d = d+timedelta(7-d.weekday())
    else:
        d = d - timedelta(d.weekday())

    dlt = timedelta(days = (week-1)*7)
    return d + dlt,  d + dlt + timedelta(days=6)

def strTimeProp(start, end, format, prop):
    stime = time.mktime(time.strptime(start, format))
    etime = time.mktime(time.strptime(end, format))

    ptime = stime + prop * (etime - stime)

    return datetime.strptime(time.strftime(format, time.localtime(ptime)), format)

def randomDate(start, end, prop):
    return strTimeProp(start, end, '%Y-%m-%dT%H:%M', prop)
