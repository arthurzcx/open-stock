import getdata.tencent_parser   as TencentParser
from getdata.parser_source import DataSourceType
from pandas import DataFrame as pd
import csv, os, requests, pandas
from contextlib2 import closing
from data import get_info

def get_data_one_year(data_source=DataSourceType.from_tencent, stock_code='', year=2020, just_days_lates=0):
    '''
    从某个数据源获取某一年的数据
    :paran data_source 数据源头, 见DataSourceType定义
    :param stock_name 股票代码 深市前缀sz,沪市前缀sh
    :param year 年代4位
    :param just_days_lates 仅需要最近多少天的数据 默认0时全需要
    :return 数据列表，[[ele1],[el2],...],每个数据依次为[时间200430，开盘价，封盘价，最高，最低]
    '''
    year_suffix = int(str(year)[2:])
    print(year)
    print(year_suffix)
    if data_source == DataSourceType.from_tencent:
        data = TencentParser.getData(stock_code, TencentParser.PeriodChoices.days_by_year, year=year_suffix, just_days_lates=just_days_lates)        
        return pd({"date":data[0], "data":data[1]})

def get_data_years(data_source=DataSourceType.from_tencent, stock_code='', years_range=[2017, 2020]):
    '''
    获取多年数据
    :param data_source 数据源
    :param stock_code 股票代码
    :param years_range 年份范围，默认集合右闭左闭
    :return DataFrame格式的数据，包括date和data
    '''
    years = []
    for y in range(years_range[0], years_range[1] + 1):
        years.append(int(str(y)[2:]))
    
    x_data = []
    y_data = []

    if data_source == DataSourceType.from_tencent:
        for y in years:
            ydata = TencentParser.getData(stock_code, TencentParser.PeriodChoices.days_by_year, year=y)
            for d in ydata[0]:
                x_data.append(d)            
            for d in ydata[1]:
                y_data.append(d)
                    
    return pd({'date':x_data, 'data':y_data})

def get_profit_csv(stock_code, file_path=''):
    '''
    获取profit报表
    :param stock_code 代码
    :param file_path 保存路径
    :return 返回完整的文件保存路径,含文件名称
    '''
    url = "http://quotes.money.163.com/service/lrb_" + stock_code.replace("sh", "").replace("sz", "") + ".html"

    # print(url)
    stock_name = get_info.get_name_by_code(stock_code)
    file_full_path = os.path.join(file_path, stock_name + '.csv')

    try:
        with closing(requests.get(url, stream=True)) as r:
            f = (line.decode('gbk') for line in r.iter_lines())
            data = csv.reader(f, delimiter=',', quotechar='"')

            ff = open(file_full_path, 'w', encoding='utf-8', newline='')
            csv_writer = csv.writer(ff)
            for row in data:
                csv_writer.writerow(row)
            ff.close()

    except Exception as e:
        print("Exception: ", e)
        return None

    return file_full_path

def get_df_from_csv(file_path):
    '''
    读入csv文件,转换为DataFarme数据
    :param file_path csv文件路径
    :return DataFrame数据
    '''
    if file_path == None:
        return None
    
    data = pandas.read_csv(file_path, low_memory=False)
    df = pandas.DataFrame(data)

    return df