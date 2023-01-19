import stock.analyzer.analyzer_utils as utils

class AnalyzerAverageContinous:
    '''
    分析方法,求取日均值线
    '''
    continous_days = 5 # 几日求平均
    total_days = 20 #分析总天数
    is_plot = False #是否绘制图标

    def __init__(self, **kwargs):
        for (key, value) in kwargs.items():
            if key == "continous_days":
                self.continous_days = value
            elif key == "total_days":
                self.total_days = value
            elif key == "is_plot":
                self.is_plot = value
    
    def analyze(self, data):
        '''
        根据输入数据进行分析
        :param data 待分析数据,二维,第一维为日期,第二维为价格
        '''
        data_ndim2 = data[1]
        # print(len(data_ndim2))
        if len(data_ndim2) < self.total_days or self.total_days < self.continous_days:
            return None
        
        data_slice = data_ndim2[-self.total_days :]
        data_average = utils.average_continous(data_slice, self.continous_days)
        return [data[0][-self.total_days :], data_average]

