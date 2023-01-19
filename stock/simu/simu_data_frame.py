import stock.analyzer.analyzer_utils as utils
import stock.getdata.get_data as DataRead
import stock.data.get_info as get_info

def simu_get_df_mean_max_min(stock_name='东方航空'):
    '''
    测试获取DataFrame的max,min,mean值
    :param stock_name 股票名称
    '''
    stock_code = get_info.get_code_by_name(stock_name)
    df = DataRead.get_data_one_year(stock_code=stock_code)
    
    print("stock_name: ", stock_name, stock_code)
    print('mean: ', utils.get_df_mean(df))
    print('max: ', utils.get_df_max(df))
    print('min: ', utils.get_df_min(df))
