# -*- coding=utf-8 -*-


from stock.analyzer.dayk import DaykAnalyzer, AnalyzerType, AnalyzerMethod
from stock.analyzer.days_increase import AnalyzeDaysIncrease

from stock.getdata.parser_source import DataSourceType
from stock.analyzer.analyzer_utils import average_continous
import stock.analyzer.analyzer_utils as AnalyzerUtils

import os, json, time, sys
import stock.getdata.get_data as DataRead

from stock.draw.plot_day import plot_dayk, plot_list
from stock.data import get_info

from pandas import DataFrame

from stock.simu import simu_get_info, simu_data_frame, simu_mean_split
import xlrd, xlwt

def strategy_mean_split():
    '''
    根据平均值策略选择
    '''    
    df = DataFrame(columns={'stock_name', 'stock_code', 'mean','per_lower_than_mean_days','neigh_days_lower_than_mean'})
    all_a_stock = get_info.get_all_a_stock()

    for i in range(len(all_a_stock)):
        # print(all_a_stock[i])
        try:
            ret = simu_mean_split.simu_mean_trade_strategy(all_a_stock[i]['name'])
            if ret != None:
                # print(ret['stock_name'], ret['stock_code'])            
                df = df.append([ret], ignore_index=True)
                simu_mean_split.simu_mean_split(all_a_stock[i]['name'], save=True)
            time.sleep(0.5)
        except Exception as e:
            print("Error! ",all_a_stock[i]['code'])
            print("Exception: ", e)

    df_sort = df.sort_values(by=['gain_same_period'], ascending=False)
    
    #获取其它信息
    # for code in df_sort['stock_code']:
    #     # print("csv_code: ", code)
    #     csv_file_path = DataRead.get_profit_csv(code, os.path.join(os.getcwd(), 'outer'))    
    #     df_csv = DataRead.get_df_from_csv(csv_file_path)    
    #     if df_csv != None:


    work_file_path = os.path.join(os.getcwd(), 'outer',  '2020-12-13_work.xls')
    wb = xlwt.Workbook(encoding='utf-8')
    sheet = wb.add_sheet('mean_beat')

    cols = [column for column in df_sort]
    counter = 0
    for i in df_sort.index:
        for j in range(len(cols)):
            if counter == 0:
                label=''
                if cols[j] == 'stock_name':
                    label = '名称'
                elif cols[j] == 'stock_code':
                    label = '代码'
                elif cols[j] == 'mean':
                    label = '平均价格'
                elif cols[j] == 'per_lower_than_mean_days':
                    label = '每次低于均值的持续天数均值'
                elif cols[j] == 'neigh_days_lower_than_mean':
                    label = '近期低于均值的持续天数'
                elif cols[j] == 'days_ratio':
                    label = '近期低于均值的天数与每次低于均值天数均值的比'   
                elif cols[j] == 'max_mean_ratio':
                    label = '近期最大值与均值的比例（获利百分比不会比该值大）'  
                elif cols[j] == 'beat_mean_times':
                    label='击穿均值的次数'       
                elif cols[j] == 'shi_jing_lv':
                    label = '市净率'
                elif cols[j] == 'shi_ying_lv':
                    label = '市盈率'             
                elif cols[j] == 'gain_same_period':
                    label = '同期增长(%)'      
                elif cols[j] == 'gain_prev_year':
                    label = '上一期利润'                                   
                elif cols[j] == 'gain_cur_year':
                    label = '当期利润'                        
                    
                sheet.write(0, j, label=label)
            sheet.write(counter + 1, j, label= df_sort.loc[i, cols[j]])
        counter += 1

    wb.save(work_file_path)

    return df_sort