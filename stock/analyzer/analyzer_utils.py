# -*- coding:utf-8 -*-
from pandas import DataFrame as pd

def get_df_middle(df):
    '''
    获取DataFrame中值
    '''
    df1 = df.sort_values(by=['data'])
    return df1.loc[int(len(df.index)/2), 'data']

def get_df_min(df):
    '''
    获取DataFrame最小值
    '''
    return df['data'].min()

def get_df_max(df):
    '''
    获取DataFrame最大值
    '''
    return df['data'].max()

def get_df_mean(df):
    '''
    获取DataFrame均值
    '''    
    return df['data'].mean()

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
    计算数据data连续数日days,上升或下降的段, 注意平缓的段也可认为符号要求,平缓度以给定值ratio_slience为准
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

def make_data_percent(df):
    '''
    数据转换为百分比形式，均值为基数
    :param df DataFrame形式数据
    :return 返回百分比形式的数据
    '''
    dc = df.copy()
    data = df['data']
    mean = data.describe()['mean']
    print('mean:', mean)
    for i in range(len(data)):
        data[i] = (data[i] - mean)/mean
    dc['data'] = data
    return dc

def make_continous_group(data):
    '''
    将列表按照连续性进行分组，例如[1, 3,4,7,8]分为[[1],[3,4],[7,8]]
    :param data 待分组的列表
    '''
    groups = []
    i = 1
    group = []
    group.append(data[0])
    while i < len(data):
        if data[i] - data[i - 1] != 1:
            groups.append(group)
            group = []
            group.append(data[i])
        else:
            group.append(data[i])
            if i == len(data) - 1:
                groups.append(group)
        i = i + 1
    return groups