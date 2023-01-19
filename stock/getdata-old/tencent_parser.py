# -*- coding:utf-8 -*-
import urllib.request as request
from enum import Enum
import time, re

class PeriodChoices(Enum):
    '''
    腾讯数据获取的方式的定义,时间周期

    Attributes:
        latest_by_day: 最新的日k数据
        latest_by_week: 最新的周k数据
        days_by_year: 指定年的日k数据
        monthly: 月k线，可能含10-20年的数据
    '''
    latest_by_day = 1
    latest_by_week = 2
    days_by_year = 4
    monthly = 5

def transferDateData(data):
    '''
    腾讯股票数据中的日期数据转换为时间格式
    :param data 腾讯股票数据中的时间数据，形似200430
    :return 返回日期格式为 %d/%m%Y 形似30/04/20    
    '''
    day = data[4:]
    month = data[2:4]
    year = data[0:2]
    # print(day,month,year)

    if int(year) > 50:
        year = "19" + year
    else:
        year = "20" + year
    str_src = year+month+day
    time_ymd = time.strptime(str_src, "%Y%m%d")
    return time.strftime("%m/%d/%Y", time_ymd)
    
def splitBySpace(data):
    '''
    分割数据并转换数据类型
    :param data腾讯股票数据，去掉了头尾和每行末尾
    :return 返回转换数据类型后的列表
    '''
    data = data.split(" ")
    # print(data)
    res = []
    for i in range(len(data)):
        if i == 0:
            date = transferDateData(data[i])
            res.append(date)
        else:
            res.append(float(data[i]))
    return res

def parseData(src_data, day_choices=PeriodChoices.latest_by_day):
    '''
    处理腾讯数据为列表形式数据
    :param src_data 腾讯原始数据
    :param day_choices 获取数据的方式，由枚举类TencentChoices定义
    :return 数据列表，[[ele1],[el2],...],每个数据依次为[时间200430，开盘价，停盘价，最高，最低]
    '''
    res = []
    if day_choices == PeriodChoices.latest_by_day:
        if not src_data.startswith( "latest_daily_data"):
            return False
        
        src_data = src_data.split("\n")[2:]
        src_data.pop()
        for i in range(len(src_data)):
            src_data[i] = src_data[i].rstrip(src_data[i][-3:])
            res.append(splitBySpace(src_data[i]))
        
        return res
    elif day_choices == PeriodChoices.latest_by_week:        
        if not src_data.startswith("latest_weekly_data"):
            return False
        
        src_data = src_data.split("\n")[2:]
        src_data.pop()
        
        for i in range(len(src_data)):
            src_data[i] = src_data[i].rstrip(src_data[i][-3:])
            res.append(splitBySpace(src_data[i]))
        
        return res
    elif day_choices == PeriodChoices.monthly:
        if not src_data.startswith( "monthly_data"):
            return False
        
        src_data = src_data.split("\n")[2:]
        src_data.pop()
        for i in range(len(src_data)):
            src_data[i] = src_data[i].rstrip(src_data[i][-3:])
            res.append(splitBySpace(src_data[i]))
        
        return res      
    elif day_choices == PeriodChoices.days_by_year:
        if not src_data.startswith( "daily_data_"):
            return False
        
        src_data = src_data.split("\n")[1:]
        src_data.pop()
        for i in range(len(src_data)):
            src_data[i] = src_data[i].rstrip(src_data[i][-3:])
            res.append(splitBySpace(src_data[i]))
        
        return res   
    else:
        return False       
    

def getData(stock_name="sz000750", day_choices=PeriodChoices.latest_by_day,year=20, just_days_lates=0):
    '''
    从腾讯获取某年某股票的日k数据    
    :param stock_name 股票代码 深市前缀sz,沪市前缀sh
    :param day_choices 获取数据的方式，由枚举类TencentChoices定义
    :param year 年代的后2位,当需要获取指定年的日k数据时使用    
    :param just_days_lates 仅需要最近多少天的数据 默认0时全需要
    :return 数据列表，[[ele1],[el2],...],每个数据依次为[时间200430，开盘价，封盘价，最高，最低]
    '''

    url = "http://data.gtimg.cn/flashdata/hushen/"

    if day_choices == PeriodChoices.latest_by_day:
        url = url + "latest/daily/" + stock_name +".js?maxage=43201&visitDstTime=1"    
    elif day_choices == PeriodChoices.latest_by_week:
        url = url + "latest/weekly/" + stock_name +".js?maxage=43201&visitDstTime=1"    
    elif day_choices == PeriodChoices.days_by_year:
        url = url + "daily/" + str(year) + "/" + stock_name +".js?visitDstTime=1"
    elif day_choices == PeriodChoices.monthly:
        url = url + "monthly/" + stock_name +".js?maxage=43201"
    else:
        return False
        
    # print("获取腾讯数据的URL:", url)
    res = request.urlopen(url)
    src_data = res.read().decode("utf-8")
    data = parseData(src_data, day_choices)

    x_data = []
    y_data = []
    for i in range(len(data)):
        x_data.append(data[i][0])
        y_data.append(data[i][2])
    
    if just_days_lates == 0 or (len(x_data) < just_days_lates):
        return [x_data, y_data]
    else:        
        return [x_data[-just_days_lates:], y_data[-just_days_lates:]]
  
# 日k 
# http://data.gtimg.cn/flashdata/hushen/latest/daily/sz000002.js?maxage=43201&visitDstTime=1

# 指定年份的日K先 
# http://data.gtimg.cn/flashdata/hushen/daily/17/sz000750.js?visitDstTime=1

# 周K 
# http://data.gtimg.cn/flashdata/hushen/latest/weekly/sz000002.js?maxage=43201&visitDstTime=1

# 月k 
# http://data.gtimg.cn/flashdata/hushen/monthly/sz000002.js?maxage=43201

def getInfo(stock_code):
    '''
    获取该stock的相关信息
    '''
    url = "http://qt.gtimg.cn/q=" + stock_code
    # print(stock_code)
        
    try:
        res = request.urlopen(url)
        src_data = res.read().decode("gbk")
        
        pattern = re.compile('"(.*)"')        
        data = pattern.findall(src_data)
        data_list = str(data).split("~")
        data_len = len(data_list)
        # print("data_len: ", data_len)
        if data_len < 47:
            return None
        info = {}
        for i in range(data_len):
            if i == 0:
                pass
            elif i == 1:
                info['stock_name'] = data_list[1]
            elif i == 2:
                info["stock_code"] = stock_code
            elif i == 3:
                info['price'] = data_list[3]
            elif i == 4:
                info['price_yesterday'] = data_list[4]
            elif i == 5:
                info['price_today_begin'] = data_list[5]
            elif i == 6:
                info['trade_hand'] = data_list[6] # 成交量（手）
            elif i == 7:
                info['outer_plate'] = data_list[7] # 外盘
            elif i == 8:
                info['innter_plate'] = data_list[i] # 内盘
            elif i == 30:
                info['time'] = data_list[i] # 时间 
            elif i == 31:
                info['gain_loss'] = data_list[i] # 涨跌
            elif i == 32:
                info['gain_loss_ratio'] = data_list[i] # 涨跌 %
            elif i == 39:
                info['shi_ying_lv'] = data_list[i] # 市盈率 
            elif i == 44:
                info['liu_tong_shi_zhi'] = data_list[i] # 流通市值 
            elif i == 45:
                info['zong_shi_zhi'] = data_list[i] # 总市值
            elif i == 46:
                info['shi_jing_lv'] = data_list[i] #市净率                    
        return info          
# 5. 4:  今开 
# 6. 5: 成交量（手）
# 7. 6:  外盘
# 8. 7:  内盘
# 9. 8:  买一 
# 10. 9: 买一量（手）
# 11. 10-17:  买二 买五 
# 12. 18: 卖一 
# 13. 19: 卖一量  
# 14. 20-27: 卖二 卖五
# 15. 28:  最近逐笔成交 
# 16. 29: 时间 
# 17. 30: 涨跌
# 18. 31:  涨跌%
# 19. 32:  最高 
# 20. 33: 最低 
# 21. 34: 价格/成交量（手）/成交额 
# 22. 35: 成交量（手）
# 23. 36:  成交额（万）
# 24. 37:  换手率
# 25. 38:  市盈率 
# 26. 39: 
# 27. 40: 最高 
# 28. 41: 最低 
# 29. 42: 振幅 
# 30. 43: 流通市值 
# 31. 44: 总市值
# 32. 45:  市净率 
# 33. 46: 涨停价 
# 34. 47:跌停价 
       
    except Exception as e:
        print('getInfo exception!')
        print(e)
        return None