# -*- coding:utf-8-*-

import stock.analyzer.analyzer_utils as utils

def get_bigger_than_mean(df, weight=1.0):
    '''
    获取比均值高的数据切片
    :param df DataFrame格式的数据
    :param weight 在均值的基础上乘以该加权值，例如1.1
    '''
    mean = utils.get_df_mean(df)
    return df[df['data'] > (mean*weight)]

def get_lower_than_mean(df, weight=1.0):
    '''
    获取比均值低的数据切片
    :param df DataFrame格式的数据
    :param weight 在均值的基础上乘以该加权值，例如0.9
    '''
    mean = utils.get_df_mean(df)
    return df[df['data'] < (mean*weight)]

def get_bigger_than_middel(df, weight=1.0):
    '''
    获取比中值高的数据切片
    :param df DataFrame格式的数据
    :param weight 在中值的基础上乘以该加权值，例如1.1
    '''
    middle = utils.get_df_middle(df)
    return df[df['data'] > (middle*weight)]

def get_lower_than_middle(df, weight=1.0):
    '''
    获取比中值低的数据切片
    :param df DataFrame格式的数据
    :param weight 在中值的基础上乘以该加权值，例如0.9
    '''
    middle = utils.get_df_middle(df)
    return df[df['data'] < (middle*weight)]