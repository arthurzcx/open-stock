import stock.data.get_info as get_info

def simu_get_all_hushi_a():
    '''    
    测试获取所有沪市股 
    '''
    print(get_info.get_all_hushi_a())

def simu_get_all_shenshi_a():
    '''
    测试获取所有深市股
    '''
    print(get_info.get_all_shenshi_a())

def simu_get_all_a():
    '''
    测试获取沪深两市所有A股
    '''
    print(get_info.get_all_a_stock())