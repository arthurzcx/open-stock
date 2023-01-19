# -*- coding:utf-8 -*-

from stock.analyzer.dayk import DaykAnalyzer, AnalyzerType, AnalyzerMethod
from stock.analyzer.days_increase import AnalyzeDaysIncrease

from stock.getdata.parser_source import DataSourceType
from stock.analyzer.analyzer_utils import average_continous
import stock.analyzer.analyzer_utils as AnalyzerUtils

import os, json, time, sys
import stock.getdata.get_data as DataRead

from stock.draw.plot_day import plot_dayk, plot_list
from stock.data import get_info
from stock.common import stock, price
from datetime import datetime

from pandas import DataFrame

from stock.simu import simu_get_info, simu_data_frame, simu_mean_split
import xlrd, xlwt

from stock.strategy.strategy_mean_split import  strategy_mean_split

from stock.getdata import tencent_parser as TencentParse
from stock.web.tencent.tencent import  WebSourceTencent
import asyncio, aiohttp

# csv_file_path = DataRead.get_profit_csv(stock_code="sh601066", file_path=os.path.dirname(sys.argv[0]))
# csv_data = DataRead.get_df_from_csv(csv_file_path)
# # print(csv_data)
# profit_row = csv_data.loc[csv_data['报告日期']=='归属于母公司所有者的净利润(万元)']
# print(profit_row['2020-09-30'] - profit_row['2019-09-30'])
# sys.exit()

# print(TencentParse.getInfo(get_info.get_code_by_name(r'南方航空')))
# sys.exit()

# test data_source

st = stock.Stock("1", "上")
# st.code = "1"
# st.name = '上'
st.price = price.Price(5.5, datetime.strptime('2022-02-23 14:55:50', '%Y-%m-%d %H:%M:%S'))
print(st.code)
print(st.name)
print(st.price.value, st.price.dtime)
sys.exit()

ust = WebSourceTencent()
stocks = []
for i in range(100,900):
    stocks.append("sh600" + str(i))
ust.fetch_stocks_data(stocks)
print(ust.get_stock("sh600439"))
print(len(ust.get_all_data().keys()))
sys.exit()
# test asyncio , 数秒钟内可获取所有A股数据的异步IO方法
async def fetch(session, url):
    async with session.get(url) as res:    
        assert res.status == 200    
        text = await res.text()
        print(text)

stocks = ["sh600001", "sh600002", "sh600003", "sh600006", "sh600005"]
url = "http://qt.gtimg.cn/q="
ust =  WebSourceTencent()

loop = asyncio.get_event_loop()
tasks = []
session =  aiohttp.ClientSession()
for i in range(100, 900):
    stock = "sh600" + str(i)
    tasks.append(asyncio.ensure_future(fetch(session, ust.get_stock_url(stock))) )

tasks = asyncio.gather(*tasks)
loop.run_until_complete(tasks)
loop.run_until_complete(session.close())
loop.run_until_complete(asyncio.sleep(3))
loop.close()

sys.exit()
# =======================================================================

strategy_mean_split()
sys.exit()

stock_name = r'电广传媒'
if len(sys.argv) > 1:
    stock_name = sys.argv[1]
simu_mean_split.simu_mean_split(stock_name)
sys.exit()

simu_data_frame.simu_get_df_mean_max_min(r'南方航空')
sys.exit()

#近期连续增长模拟
def simu_days_increase():
    stock_name = r"南方航空"
    stock_code = get_info.get_code_by_name(stock_name)
    if stock_code == None:
        print('The stock_code is None!')
        return
    df = DataRead.get_data_years(DataSourceType.from_tencent, stock_code, [2015,2020])  
    df = df.tail(150)
    analyzerDaysIncrease = AnalyzeDaysIncrease()
    print(analyzerDaysIncrease.analyze(df))


simu_get_info.simu_get_all_a()
sys.exit()

simu_get_info.simu_get_all_shenshi_a()
sys.exit()

simu_get_info.simu_get_all_hushi_a()
sys.exit()

simu_days_increase()
sys.exit()

#测试多年数据绘图
stock_name = "南方航空"
stock_code = get_info.get_code_by_name(stock_name)
if stock_code == None:
    sys.exit()
print(stock_code)
pd = DataRead.get_data_years(DataSourceType.from_tencent, stock_code, [2010, 2020])
plot_dayk(pd, stock_name)
sys.exit()

#测试均值过滤
stock_code = "sh603220"
stock_name = get_info.get_name_by_code(stock_code)
print(stock_name)
year = 2020
data_sh600029 = DataRead.get_data_one_year(DataSourceType.from_tencent, stock_code , year)

dp = AnalyzerUtils.make_data_percent(data_sh600029)
plot_dayk(dp, title_text=stock_name, xlabel=str(year) , ylabel=u"price")
sys.exit()

data_avr = AnalyzerUtils.average_continous(data_sh600029['data'], 3)
for i in range(3):
    data_avr = AnalyzerUtils.average_continous(data_avr, 5)

data_sh600029_avr = data_sh600029.copy()
data_sh600029_avr['data'] = data_avr
extreme_pt = AnalyzerUtils.calc_dexreme_point(data_sh600029)
print(extreme_pt)
data_list=[data_sh600029,data_sh600029_avr]
plot_list(data_list, title_text=stock_name, xlabel=str(year) , ylabel=u"price", label=['实际价格', '滤波价格'])
# plot_dayk(data_sh600029, title_text=stock_name, xlabel=str(year) , ylabel=u"price")
# mean = data_sh600029.describe().loc['mean']

# def compare(x):
#     if x > mean:
#         return True
#     else:
#         return False

# print(data_sh600029['data'].apply(compare))
# print(data_sh600029.describe().loc['mean'])
# plot_dayk(data_sh600029, title_text=stock_name, xlabel=str(year) , ylabel=u"price")

# data_avr = AnalyzerUtils.average_continous(data2019_sh600029[1])
# data_avr = AnalyzerUtils.average_continous(data_avr)
# segs = AnalyzerUtils.clac_continous_down_seg(data_avr, 15, 0.2, 5,0.008)
# data2019_sh600029[1]  = data_avr
# print(segs)
# for i in range(len(segs)):
#     print(data2019_sh600029[0][segs[i][0]],data2019_sh600029[0][segs[i][1]])
# plot_dayk(data2019_sh600029, title_text=stock_name, xlabel=str(year) , ylabel=u"price")

# print(data2019_sh600029)

'''
寻找V形谷底方法:比如连续数日微涨,在此之前连续跌或不变化,此时较大概率由谷底返回!!!!可验证
'''

#k线分析
# analyzer=DaykAnalyzer(stock_name="南方航空", stock_code="sh600029", \
#     year=2020, years=(2010,2020), \
#     analyze_type=AnalyzerType.by_year, \
#     soure_type=DataSourceType.from_tencent, \
#     nanlyze_days_latest=30, \
#     method=AnalyzerMethod.by_day_k)
# analyzer.analyze()

# 使用连续增加法测试所有hushi_stock
# with open("./data/stock_shenshi.json", 'r') as f:
#     stock_hushi = json.load(f)
#     for (key, value) in stock_hushi.items():        
#         analyzer = DaykAnalyzer(stock_name=key, stock_code=value, \
#                                                             year=2020, years=(2010,2020), \
#                                                             analyze_type=AnalyzerType.by_year, \
#                                                             soure_type=DataSourceType.from_tencent, \
#                                                             nanlyze_days_latest=30, \
#                                                             method=AnalyzerMethod.by_days_increase)
#         analyzer.analyze()
#         time.sleep(0.5)

#测试连续平均法
# data = [1,2,3,4,5,6,7,8,9,10]
# new_data = average_continous(data, 5)
# print(new_data)

#连续均值分析
# analyzer=DaykAnalyzer(stock_name="南方航空", stock_code="sh600029", \
#     year=2020, years=(2010,2020), \
#     analyze_type=AnalyzerType.by_year, \
#     soure_type=DataSourceType.from_tencent, \
#     nanlyze_days_latest=100, \
#     method=AnalyzerMethod.by_average_continous)
# analyzer.analyze()