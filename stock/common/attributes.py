# !/usr/bin/python
# -*- encoding:utf-8 -*-

# @author: Arthurz
# @date: 2022/04/03
# @version 1.0
# @desc: Access the attributes of a class.

import inspect

# from common.stock import Stock

def get_class_attrs(cls_name):
    """ Get attrs of a cls_name.
    """
    attrs =  inspect.getmembers(globals()[cls_name], lambda a: not inspect.isfunction(a))
    attrs = list(filter(lambda x: not x[0].startswith('__'), attrs))
    attrs = [ele[0] for ele in attrs]
    return attrs
