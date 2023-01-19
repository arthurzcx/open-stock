# -*- coding:utf-8 -*-
from patsy.util import pandas_Categorical_categories
import pandas

def to_percent(num_value):
    '''
    将数组转换为百分比字符串
    :param num_value 待转换数值
    '''
    return str(round(num_value*100.0,2)) + "%"

def average_continous(data, continous_counter = 5):
    '''
    求连续平均值, 所谓连续平局值是指例如20天共20个数据,每连续5天求均值
    头部continous_counter-1个数据按照相应位置递增天数求均值
    :param data 待求均值数据
    :param continous_counter连续几个数据求均值
    :return 返回求平均后的列表
    '''
    if len(data) < continous_counter or len(data) == 0 or continous_counter < 1 :
        return data
    
    average_data = []
    for i in range(len(data)):
        sum = 0 
        if i == 0:
            average_data.append(data[0])
        elif i < continous_counter:
            for c in range(i + 1):
                sum += data[i - c]
            average_data.append(sum/(i+1))
        else:
            for c in range(continous_counter):
                sum +=data[i - c]
            average_data.append(sum/continous_counter)
    return average_data

def clac_continous_down_seg(data, days, ampitude_down = 0.25, gate_up_days = 5, ratio_slience = 0.008):
    '''
    计算数据data连续数日days,上升或下降的段, 注意平缓的段也可认为符合要求,平缓度以给定值ratio_slience为准
    连续days作为窗口在数据上移动进行分析
    :param data 输入数据
    :param days连续上升或下降的次数或天数   
    :param ampitude_down下降幅度阈值,必须下降到阈值之下才视为下降
    : gate_up_days允许出现后一天大于前一天的次数,其超出的值不得超过ratio_slience,否则认为不符合下降要求
    :param ratio_slience判定是否为平缓段的阈值 
    :return 返回由段组成的列表,每段使用开始和结束索引值组成, 例如[[1, 30],[45,50],...],如果没有找到则返回为None
    '''

    if (len(data) < days) or (days < 2) or (gate_up_days >= days):
        return None

    # 以第一天为基准的百分比
    data_ratio = []
    for i in range(len(data) - 1):
        data_ratio.append((data[i + 1] - data[0])/data[0])
        # print(round(data_ratio[i], 2))

    segs = []
    i = 0 
    while i < (len(data_ratio) - days):
        
        j = i + days
        seg_this_fit = False

        if data_ratio[i] > data_ratio[j] + ampitude_down:    
            
            tag_data_j = data_ratio[j]        
            
            #    该处需要修改为判定数天增长即断开 
            counter_increase = 0
            for k in range(j + 1, len(data_ratio) - days):       
                if counter_increase >= 3:
                    j = k - 3
                    print(data_ratio[k-1], tag_data_j)
                    seg_this_fit = True
                    break
                elif data_ratio[k] >   data_ratio[k-1]:
                    counter_increase = counter_increase + 1
                    j = k
                elif counter_increase < 3:
                    j  = k            

            couter_overflow_days = 0 #计数后者大于前者的次数
            max_overflow_ratio = 0.0 #计数最大的溢出值(后一天大于前一天视为溢出)

            for k in (i, j):
                if data_ratio[k+1] > data_ratio[k] : 
                    couter_overflow_days = couter_overflow_days + 1
                    if max_overflow_ratio < data_ratio[k+1] - data_ratio[k]:
                        max_overflow_ratio = data_ratio[k+1] - data_ratio[k]
            if max_overflow_ratio < ratio_slience and couter_overflow_days <= gate_up_days:
                segs.append([i, j])
                # print(i,j)
        if seg_this_fit:        
            i = j
        else:
            i = i + 1
            

    return segs

def calc_dexreme_point(df, is_filter = False):
    '''    
    求极值点对应日期
    '''
    dd = df['data']
    if is_filter == True:
        dd = average_continous(dd)
    dt = dd.copy()
    for i in range(len(dd)):                
        if i > 0:            
            dt.iloc[i] = ((dd.iloc[i] - dd.iloc[i - 1] )> 0)         
        else:
            dt.iloc[0] = 0
         
    dt.iloc[0] = dt.iloc[1]
    print(dt)

    pdate = []
    for i in range(1, len(dt) - 1):
        if dt.iloc[i] != dt.iloc[i - 1]:
            pdate.append(df['date'].iloc[i])
    return pdate

def calc_minus_yesterday(df_data, data_column):
    '''
    计算连续数据中当天与前一天的数据差，由此可以得出每日相对前一日数据的增减
    
    Args:
    @df_data:  DataFrame格式数据
    @data_column: 数据列的名称 ， 比如market_value
    
    @return: 将在df_data数据中插入一列名为 minus_yesterday
    '''
    data = df_data[data_column]
    minus_yesteraty = []
    for i in range(0, data.size):
        if i == 0:
            minus_yesteraty.append(0.0)
        else:
            minus_yesteraty.append(data[i] - data[i-1])
    df_data.insert(df_data.shape[1], 'minus_yesterday', minus_yesteraty)
    return df_data    

def calc_inc_or_decr_continous_days_and_ratio(df_data, column, base_data_column):
    '''
    分析calc_minus_yesterday的结果数据 在近期的连续增长或下跌天数
    
    Args:
    @df_data: padans.DataFrame格式的数据
    @column: 待分析的数据的列名 例如minus_yesterday
    @base_data_column: 原始数据列名，用于求百分比，例如市值数据market_value
    
    @return: 返回一个map对象 {"increase": True, "days": 2, "ratio": "2%"}
    increase=True表示连续数日增长，False代表下跌
    days表示连续增长或下跌天数
    ratio表示连续增长或下跌的百分比
    '''
    data = df_data[column]
    base_data = df_data[base_data_column]
    
    rows = data.shape[0]
    
    increase = False
    continous_days = 0
    for i in range(data.size - 1, 0, -1):
        if i == data.size - 1 :
            increase = data[i] > 0.0
        else:
            if increase == True and data[i] < 0.0:
                continous_days = data.size - i - 1
                break
            elif increase == False and data[i] > 0.0:
                continous_days = data.size - i - 1
                break
    
    ratio = data[data.size - 1]/base_data[data.size -2]
    if continous_days >= 1: 
        ratio = (base_data[data.size - 1] - base_data[data.size - continous_days -1])/base_data[data.size - continous_days -1]
    
    return {"increase":increase, "days":continous_days, "ratio":ratio}
                
                
        
    
    
    
    