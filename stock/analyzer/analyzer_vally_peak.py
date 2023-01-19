from stock.analyzer.analyzer_utils import average_continous

class AnalyzerVallyPeak:
    '''
    谷底爬坡分析法

    Attributes:
    down_from_days:向谷底下滑的次数,天数,输入前设定
    to_peak_days:向上爬坡的次数,天数,输入前设定
    '''
    down_from_days = 30 #向谷底下滑的次数,天数,输入前设定
    to_peak_days = 5 #向上爬坡的次数,天数,输入前设定

    final_to_peak_days = 0 #最终爬坡天数,之后转入下一个周期下坡,计算得出
    ratio_know_up_to_peak = 0.0 #从知道爬坡开始到爬坡结束时,一共爬升的比例,计算得出

    def __init__(self, **kwargs):
        for (key, value) in kwargs.items():
            if key == "down_from_days":
                self.to_peak_days = value
            elif key == "to_peak_days":
                self.down_from_days = value  

    def analyze(self, data):
        '''
        分析执行函数

        Args: 
            data: 输入待分析二维数据,应具有一定的样本数量,0维为日期,1维为价格

        Returns:
            返回分析执行后的结果
        '''
        data1 = data[1]
        if len(data1) < self.down_from_days + self.to_peak_days:
            return None
        #求数日连续均值
        data_aver = average_continous(data=data1)
        

