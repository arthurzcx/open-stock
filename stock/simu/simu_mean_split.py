import stock.analyzer.analyzer_mean_split as ms
import stock.analyzer.analyzer_utils as utils
import stock.data.get_info as get_info
import stock.getdata.get_data as DataRead
import stock.getdata.tencent_parser as TencentParser
import stock.draw.plot_day as pltd
import json,os

def simu_mean_trade_strategy(stock_name='东方航空'):
    '''
    确定选股策略如下：
    完全符合以下各条件的股可买入：
    1.近期维持在均值（或加权值均值*0.8）以下时间超出 往日维持在均值下天数的均值；
    2.近期一半时间内没有明显上涨，可通过近期最大峰值是否在后半段或前半段进行判定。
    符合以下条件的股必须卖出：
    1.涨幅超过20%；
    2.跌幅超过10%
    '''
    stock_code=get_info.get_code_by_name(stock_name)
    
    #数据
    df = DataRead.get_data_years(stock_code=stock_code, years_range=[2019,2021])
    
    #均值
    mean = utils.get_df_mean(df)

    #所有大于均值的数据
    dfms_higher = ms.get_bigger_than_mean(df)
    dfms_higher = ms.get_bigger_than_mean(df)

    #所有低于均值的数据
    weight = 1.0
    dfms_lower = ms.get_lower_than_mean(df, weight)

    if len(dfms_lower) < 1:
        return None
    
    #每次低于均值的持续天数的均值per_lower_than_mean_days：比如存在2次低于均值时间，一段5天，一段10天，则平均为7.5天  
    # 同时只关注那些长期位于均值下的股票，股设定一个假想值，必须大于10天  
    groups_higher = utils.make_continous_group(dfms_higher.index)
    groups_lower = utils.make_continous_group(dfms_lower.index)
    sum_lower_than_mean_days = 0
    for i in range(len(groups_lower)):        
        sum_lower_than_mean_days += len(groups_lower[i])    
    per_lower_than_mean_days = 0
    if len(groups_lower) > 0:
        per_lower_than_mean_days = sum_lower_than_mean_days/len(groups_lower)
    if per_lower_than_mean_days < 10:
        return None
    
    #近期是否一直处于均值下
    df_neighbor = df.loc[len(df.index) - per_lower_than_mean_days :, :]
    max_neighbor = utils.get_df_max(df_neighbor)
    if max_neighbor > mean:
        return None
    max_index = df_neighbor['data'].idxmax()
    # print('max_index:', max_index)
    if max_index > (len(df.index) - 0.5*per_lower_than_mean_days):
        return None

    #大于6个月认为无价值
    if (per_lower_than_mean_days > 180) or (len(groups_lower[len(groups_lower) - 1])   > 180):
        return None
    
    #如果均值价格小于2.5,认为风险大
    if mean < 2.5:
        return None
    
    #如果击穿均值次数少,也不考虑
    if len(groups_higher) < 2:
        return None
    
    #市盈率等信息,太小或太大都不合法
    shi_jing_lv = 0.0
    shi_ying_lv = 0.0
    info_others = TencentParser.getInfo(stock_code)
    if info_others != None:
        if float(info_others['shi_ying_lv'])< 2.0:
            return None
        else:
            shi_ying_lv = info_others['shi_ying_lv']
        
        shi_jing_lv = info_others["shi_jing_lv"]
    if float(shi_ying_lv ) > 120.0:
        return None
    
    ret = {}

    #year report information
    csv_file_path = DataRead.get_profit_csv(stock_code, os.path.join(os.getcwd(), 'outer'))    
    df_csv = DataRead.get_df_from_csv(csv_file_path)    
    if df_csv is not None:
        col1_name= '报告日期'
        row_name = '归属于母公司所有者的净利润(万元)'
        profit_row = df_csv.loc[df_csv[col1_name]==row_name]

        gain_same_period =  (float(profit_row['2020-09-30']) -  float(profit_row['2019-09-30']))/float(profit_row['2019-09-30'])

        ret['gain_same_period'] = round(gain_same_period*100.0, 2)
        ret['gain_prev_year'] = float(profit_row['2019-09-30'])
        ret['gain_cur_year'] = float(profit_row['2020-09-30'])

        #历年利润为0视为不合法, 没有实现增长的也不合法
        if  float(profit_row['2019-09-30'])  < 0:
            return None
        if float(profit_row['2020-09-30']) < 0:
            return None
        if round(gain_same_period*100.0, 2) < 0.0:
            return None
    else:
        return None            
    
    ret['stock_name'] = stock_name
    ret['stock_code'] = stock_code
    ret['mean'] = round(mean, 2)
    ret['per_lower_than_mean_days'] = round(per_lower_than_mean_days, 2)
    ret['neigh_days_lower_than_mean'] = len(groups_lower[len(groups_lower) - 1])  
    ret['days_ratio'] =  round(ret['neigh_days_lower_than_mean']/per_lower_than_mean_days, 2) #近期低于均值持续天数 与 每次低于均值持续天数均值的比例
    ret['max_mean_ratio'] = utils.to_percent((utils.get_df_max(df)/mean) - 1.0)
    ret['beat_mean_times'] = len(groups_higher)
    ret['shi_jing_lv'] = shi_jing_lv
    ret["shi_ying_lv"] = shi_ying_lv
    # print("ret:", ret)
    return ret

def simu_mean_split(stock_name='东方航空', save=False):
    '''
    测试均值分割切片,并将连续的大于均值的切片求出

    '''
    stock_code=get_info.get_code_by_name(stock_name)
    df = DataRead.get_data_years(stock_code=stock_code, years_range=[2019,2020])
    
    mean = utils.get_df_mean(df)
    print("mean:", mean)
    dfms_higher = ms.get_bigger_than_mean(df, 1.01)
    dfms_lower = ms.get_lower_than_mean(df, 0.9)
    if len(dfms_lower) < 1:
        # pltd.plot_list([df],title_text=stock_name)
        return None
    # dfms_higher = ms.get_bigger_than_middel(df, 1.01)
    # dfms_lower = ms.get_lower_than_middle(df, 1.0)

    ret = {}
    ret['stock_name'] = stock_name
    ret['stock_code'] = stock_code
    
    ret['mean'] = mean    

    groups_higher = utils.make_continous_group(dfms_higher.index)
    groups_lower = utils.make_continous_group(dfms_lower.index)    
    
    # 高于均值每次持续的天数的一半
    sum_bigger_than_mean_days = 0
    for i in range(len(groups_higher)):
        # print('group ' + str(i) + ": ", groups_higher[i][0], groups_higher[i][len(groups_higher[i]) - 1])
        sum_bigger_than_mean_days = sum_bigger_than_mean_days + len(groups_higher[i])    
    per_bigger_than_mean_days_half = 0
    if len(groups_higher) > 0:
        per_bigger_than_mean_days_half = 0.5*sum_bigger_than_mean_days/len(groups_higher)
    ret['continous_higher_than_mean_days_HALF'] = per_bigger_than_mean_days_half #该值为平均持有天数

    # 低于均值每次持续的天数
    sum_lower_than_mean_days = 0
    for i in range(len(groups_lower)):
        # print('group ' + str(i) + ": ", groups_lower[i][0], groups_lower[i][len(groups_lower[i]) - 1])
        sum_lower_than_mean_days = sum_lower_than_mean_days + len(groups_lower[i])    
    per_lower_than_mean_days = 0
    if len(groups_lower) > 0:
        per_lower_than_mean_days = sum_lower_than_mean_days/len(groups_lower)
    ret['continous_lower_than_mean_days'] = per_lower_than_mean_days #每次低于均值持续天数的均值

    print(groups_lower[len(groups_lower) - 1])

    #为了利益最大化，可以将低于均值运行的天数加大，以保证该段时间为此比较久
    # per_lower_than_mean_days *= 2
    #调整持有天数大于均值
    # per_bigger_than_mean_days_half *= 1.2

    if (per_bigger_than_mean_days_half) < 1 or (per_lower_than_mean_days < 1):
        return None
    #买入条件：目前低于均值的天数 > 每次低于均值持续天数的均值
    #卖出条件：已经持有 每次大于平均值持续天数的一半
    #以此买入条件和卖出条件进行买卖模拟，并计算每次买卖的平均收益率

    ratios = [] #每次买卖盈亏比例
    for i in range(len(groups_lower)):
        group = groups_lower[i]
        if len(group) > per_lower_than_mean_days:
            day_buy_in = group[len(group) - 1]
            day_sell_out = (int)(day_buy_in + per_bigger_than_mean_days_half)
            if day_sell_out >= len(df['data'].index):
                day_sell_out = len(df['data'].index) - 1
                
            ratio = (df.loc[day_sell_out,'data'] - df.loc[day_buy_in,'data'])/df.loc[day_buy_in,'data']
            ratios.append(ratio)
            print('ratio:', ratio, df.loc[day_sell_out,'date'], df.loc[day_buy_in,'date'], day_buy_in, day_sell_out)    

    ret['buy_sell_times'] = len(ratios)
    ret['max_earn_ratio'] = max(ratios)
    ret['min_earn_ratio'] = min(ratios)
    mean_ratio = 0
    if len(ratios) > 0:
        mean_ratio = sum(ratios)/len(ratios)
    ret['mean_earn_ration'] = mean_ratio

    # for (key, value) in ret.items():
    #     print(key, value)    
    
    df_mean = df.copy()
    for i in range(len(df.index)):
        df.loc[i, 'data'] = mean
    pltd.plot_list([df, df_mean],title_text=stock_name, save=save)
    return ret


