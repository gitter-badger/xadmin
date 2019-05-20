#!/usr/bin/env python
# -*- coding: utf-8 -*-
import datetime
import calendar
print('datetime.datetime()',datetime.datetime.now())

time = datetime.date(2019, 5, 20) #年，月，日

#求该月第一天
first_day = datetime.date(time.year, time.month, 1)
print (u'该月第一天:' + str(first_day))

#求前一个月的第一天
#前一个月最后一天
pre_month = first_day - datetime.timedelta(days = 1) #timedelta是一个不错的函数
print (u'前一个月最后一天:' + str(pre_month))
#前一个月的第一天
first_day_of_pre_month = datetime.date(pre_month.year, pre_month.month, 1)
print (u'前一个月的第一天:' + str(first_day_of_pre_month))

#求后一个月的第一天
days_num = calendar.monthrange(first_day.year, first_day.month)[1] #获取一个月有多少天
first_day_of_next_month = first_day + datetime.timedelta(days = days_num) #当月的最后一天只需要days_num-1即可
print (u'后一个月的第一天:' + str(first_day_of_next_month))