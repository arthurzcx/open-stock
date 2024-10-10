 
### open-stock

Open source data analyzer for A-shares, based on python.

### Architecture brief

- common: package basic stocks, message, email and html content generated functions.
- analyzer: package analyszer implementation. Until now it has implemented MA, index and plate analyzer, and everyone can write a different analyzer, and run them at same time which can be managed by analyzer_manager.
- data: package data class implentation.
- draw: package data plot class implentation.
- local: package A-shares list and functions.
- my: package favorites and repository functions.
- simu: package backtrace and simulation functions.
- strategy: package many different strategy.
- web: package APIs for obtaining data through internet.OB


External data and test:
- data: storage directory for all different data.
- test: test different strategy.


### Installation

1. linux system is recommended. Just python3 supported, please do not use python2.
2. pull the code repository.
3. build virtualenv environment.
4. use command 'pip install -r requirement.txt' to install library dependency.


### Usage

1. First way: use command 'python main.py' into command line，and print 'help' to check functions that can be triggered.

```
python main.py
->help

Documented commands (type help <topic>):
========================================
add_favorite            test_all_sectors                          
analyzer_manager        test_broad_cap_index_analyze              
buy                     test_calc_minus_yesterday                 
draw_candle             test_create_market_value_data_from_history
draw_one_stock_history  test_draw_sector_continous_days           
draw_one_stock_today    test_read_broad_cap_index_latest          
exit                    test_read_one_section                     
find_a_stock            test_read_sector_continous_days           
help                    test_read_sector_continous_days_ma        
my_positions            test_read_sector_day                      
remove_favorite         test_sector_analyzer                      
sell                    update_history                            
test_all_section_list
```

2. Second way：use command 'python main.py -h' to check functions supported now.

```
python main.py -h
usage: main.py [-h] [--update_current] [--update_history]
               [--test_stocks_counter] [--test_read_dataframe_data]
               [--test_plot_df_on_stock_history]

The main entry to enjoy your stock trip......

optional arguments:
  -h, --help            show this help message and exit
  --update_current, -c  update current stock data from web
  --update_history, -u  update history data from web
  --test_stocks_counter, -n
                        test counter of stocks in China stocks market
  --test_read_dataframe_data, -d
                        test to read xls data, converted to DataFrame type
                        data
  --test_plot_df_on_stock_history, -p
                        test to draw one stock history data in DataFrame type
```


### Noitce

- All A-shares data from open web APIs.



**

### open-stock

** 
开源A股数据分析器,基于python实现。

 **

### 架构简述
** 

主体实现：
- common: 封装基本stock、message、email、html生产等属性与功能；
- analyzer: 封装分析器类实现，目前有均值MA、大盘、板块基本分析器，可自行创建分析器，并使用analyzer_manager同时运行多个分析器；
- data: 封装数据读取类实现；
- draw: 封装数据绘制类实现；
- local: A股数据列表及功能；
- my: 封装收藏、持仓功能；
- simu: 封装回溯仿真功能；
- strategy: 封装回溯与实操策略；
- web: 封装A股数据获取器等。


外部数据与测试：
- data: 本目录存储所有获取的数据；
- test: 实现测试用例等。


 **

### 安装教程
** 

1.  考虑模块匹配，建议使用linux系统；
2.  拉取repo;
3.  建立virtualevn虚拟环境；
4.  pip install -r requirement.txt 安装依赖。


 **

### 使用说明
** 

1.  第一种：python main.py进入cmd命令行，输入help查看可触发功能

```
python main.py
->help

Documented commands (type help <topic>):
========================================
add_favorite            test_all_sectors                          
analyzer_manager        test_broad_cap_index_analyze              
buy                     test_calc_minus_yesterday                 
draw_candle             test_create_market_value_data_from_history
draw_one_stock_history  test_draw_sector_continous_days           
draw_one_stock_today    test_read_broad_cap_index_latest          
exit                    test_read_one_section                     
find_a_stock            test_read_sector_continous_days           
help                    test_read_sector_continous_days_ma        
my_positions            test_read_sector_day                      
remove_favorite         test_sector_analyzer                      
sell                    update_history                            
test_all_section_list
```

2.  第二种：python main.py -h查看命令行支持功能。

```
python main.py -h
usage: main.py [-h] [--update_current] [--update_history]
               [--test_stocks_counter] [--test_read_dataframe_data]
               [--test_plot_df_on_stock_history]

The main entry to enjoy your stock trip......

optional arguments:
  -h, --help            show this help message and exit
  --update_current, -c  update current stock data from web
  --update_history, -u  update history data from web
  --test_stocks_counter, -n
                        test counter of stocks in China stocks market
  --test_read_dataframe_data, -d
                        test to read xls data, converted to DataFrame type
                        data
  --test_plot_df_on_stock_history, -p
                        test to draw one stock history data in DataFrame type
```


 **

### Noitce
** 
- A股数据来自互联网公开数据，如果存在违权、违法情形，请联系author进行删除；
- API接口的使用使用互联网公开接口，如果存在违权、违法情形，请联系author进行删除；
- 如果存在其它违权、违法情形，请联系author进行移除。

 **

### 其它
** 
关于软件运行时出现的StockSimulation字样说明，仅作为示例使用，可自行修改。


