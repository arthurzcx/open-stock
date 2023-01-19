# !/usr/bin/python
# -*- encoding:utf-8 -*-

# @author: Arthurz
# @date: 2022/04/03
# @version 1.0
# @desc: Get the datetime for your need.

import datetime

class UtilDateTime():
    """ A util class for datetime.
    """

    def __init__(self):
        pass
    
    @staticmethod
    def now_utc():
        """ 
        UTC now.
        """
        return datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc)
    
    @staticmethod
    def now_beijing():
        """ 
        Beijing now.
        @return: a DateTime object
        """
        now_utc = UtilDateTime.now_utc()
        return now_utc.astimezone(datetime.timezone(datetime.timedelta(hours=8), name='Asia/Shanghai',))
    
    @staticmethod
    def weekday(dtime):
        """ 
        Get the week_day from the datetime input.
        """
        return dtime.weekday() + 1
    
    @staticmethod
    def is_valid_trade_day(dtime):
        '''
        判断是否为合法的交易日期，例如国庆假期、元旦、周末等非交易日
        
        ToDo: 使用农历假期换算交易日
        
        Arguments:
            @dtime 待判断的日期
        
        Returns:
            True 表示交易日， False表示非交易日
        '''
        wd = UtilDateTime.weekday(dtime)
        month = dtime.month
        day = dtime.day
        if wd > 5:
            return False
        elif month == 10 and day < 8:
            return False
        elif month == 1 and day < 3:
            return False
        else:
            return True
    
        