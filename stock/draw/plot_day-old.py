# -*- coding:utf-8 -*-

import matplotlib
import matplotlib.pyplot as plt

import matplotlib.dates as mdates
import matplotlib.axes as axes
from datetime import datetime
import platform, os

plt.rcParams['font.sans-serif']=['SimHei', 'URW Palladio L', 'Manjari Bold'] #用来正常显示中文标签

def plot_list(data_list, title_text="not title", xlabel='noxlabel', ylabel='nolabel', label=[], save=False):
    '''
    将多个曲线数据绘制到一个图上
    :param data_list 多个曲线数据形成的列表
    :title_text 标题
    :xlabel x轴说明
    :ylabel y轴说明
    '''
    fig, axes = plt.subplots()

    xs = [datetime.strptime(d, '%m/%d/%Y').date() for d in data_list[0]['date']]    

    axes.xaxis.set_major_formatter(mdates.DateFormatter('%m/%d'))
    axes.xaxis.set_major_locator(mdates.MonthLocator(interval=1))

    for i in range(len(data_list)):  
        l='default_label'
        if len(label) > i:
            l = label[i]      
        plt.plot(xs, data_list[i]['data'], label=l)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title_text)
    plt.legend()

    axes.grid(True)
    fig.autofmt_xdate()

    if save == True:
        plt.savefig(os.path.join(os.getcwd(), 'outer', title_text + ".jpg"))
    else:
        plt.show()


def plot_dayk(data, title_text="no_title", xlabel="noxlabel", ylabel="noylabel"):
    '''
    绘制xy数据
    :param data 二维数据列表[[x1,x2,x3...], [y1,y2,y3...]],x为形似04/30/2020的时间
    :param title_text 绘制图的标题
    '''
    fig, axes = plt.subplots()

    xs = [datetime.strptime(d, '%m/%d/%Y').date() for d in data['date']]    

    axes.xaxis.set_major_formatter(mdates.DateFormatter('%m/%d'))
    axes.xaxis.set_major_locator(mdates.MonthLocator(interval=1))

    plt.plot(xs, data['data'])
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title_text)

    axes.grid(True)
    fig.autofmt_xdate()
    plt.show()    

def plot_dayk_compare(data, years, title_text="no_title",xlabel="noxlable", ylabel="noylabel"):
    '''
    历年日k线比较
    :param data 历年的日k数据,形似[[[x1,x2,x3..],[y1,y2,y3...]],[[],[]]  ]
    :param years 历年组成的元组，形似(2001,2002,2003,...)
    :param title_text 绘图标题
    :param xlabel x轴标签
    :param ylabel y轴标签
    '''
    
    if len(data) != len(years):
        print("plot_dayk_compare: the capacity of data and years are not equal!")
        return
    fig, axes = plt.subplots()

    axes.xaxis.set_major_formatter(mdates.DateFormatter('%m/%d'))
    axes.xaxis.set_major_locator(mdates.MonthLocator(interval=1))
         
    for i in range(0,len(data)):
        for j in range(0,len(data[i][0])):
            data[i][0][j] = data[i][0][j][0:5]

    for c in range(0, len(data)):
        counter_feb_29 = -1
        for i in range(0, len(data[c][0])):
            if data[c][0][i].startswith("02/29"):
                counter_feb_29 = i
                break
        print("counter_feb_29:", counter_feb_29)
        if counter_feb_29 != -1:
            data[c][0].pop(counter_feb_29)
            data[c][1].pop(counter_feb_29)
        
    for i in range(len(data)):           
        xs = [datetime.strptime(d1, '%m/%d').date() for d1 in data[i][0]]
        plt.plot(xs, data[i][1],label=years[i])        
    
    axes.legend()

    plt.xlabel(xlabel)
    plt.ylabel(ylabel)

    plt.title(title_text)

    axes.grid(True)
    fig.autofmt_xdate()
    plt.show() 
