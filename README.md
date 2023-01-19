 
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


