# -*- encoding:utf-8 -*-
'''
配置打印消息的样式和颜色

Created on 2022年10月22日

@author: Arthur
@copyright: Jancy Co.,Ltd.
'''

from enum import Enum

class Color():
    '''
    定义打印message的颜色.
    
    Attributes:
        参照内部属性定义.
    '''
    black = '40'
    red = '31'
    green = '32'
    yellow = '33'
    blue = '34'
    fuchsia = '35'
    cyan = '36'
    white = '37'

class Style():
    '''
    定义打印message的样式，例如高亮、下划线等.
    
    Attributes:
        参照内部属性定义.
    '''
    default = '0'
    highlight = '1'
    underline = '4'
    flicker = '5'
    anti_white = '7'
    invisible = '8'

class Alignment():
    '''
    定义打印Message的对齐方式.
    
    Attributes:
        参照内部属性定义.
    '''
    default = 0
    center = 1
    left = 2
    right = 3

class MessageLevel(Enum):
    Info = 0
    Warning = 1
    Error = 2

class Message():
    """
    安装样式和颜色打印消息的类
    
    Attributes:
        style: 样式
        color: 颜色值，Color类型 
    """

    def __init__(self, color=Color.white, style=Style.default):
        self.color = color
        self.style = style

    def local_print(self, message):
        msg = "\033[" + self.style + ";" + \
            self.color + "m" + message + "\033[0m"
        print(msg)

    def level_print(self, message, level=MessageLevel.Info):
        self.color = Color.white
        self.style = Style.default

        header_color = Color.blue
        header_style = Style.highlight
        header = "Info: "

        if level == MessageLevel.Warning:
            header_color = Color.yellow
            header = "Warnning: "
        elif level == MessageLevel.Error:
            header_color = Color.red
            header = "Error: "

        header = "\033[%s;%sm%s\033[0m" % (
            str(header_style), str(header_color), header)

        print(header + message)

def center_msg(msg_list, align_len=16):
    """ 
    Align the text in list center with the same length(align_len).

    Args:
        msg_list: message with list type.
        align_len: width of every string aligned.
    """
    new_msg_list = []
    for msg in msg_list:
        new_msg_list.append(msg.center(align_len))
    return new_msg_list


def left_msg(msg_list, align_len=16):
    """ 
    Align the text in list left with the same length(align_len).

    Args:
        msg_list: message with list type.
        align_len: width of every string aligned.
    """
    new_msg_list = []
    for msg in msg_list:
        new_msg_list.append(msg.ljust(align_len))
    return new_msg_list


def right_msg(msg_list, align_len=16):
    """ 
    Align the text in list left with the same length(align_len).

    Args:
        msg_list: message with list type.
        align_len: width of every string aligned.
    """
    new_msg_list = []
    for msg in msg_list:
        new_msg_list.append(msg.rjust(align_len))
    return new_msg_list

def left_indent_msg(msg_list, counter=4, sep=' '):
    '''
    字符串列表左侧缩进
    Arguments:
    @msg_list 字符串列表
    @counter 缩进数量
    @sep 缩进补充的字符串，默认空格
    '''
    new_msg_list = []
    for msg in msg_list:
        new_msg_list.append(counter*sep + msg)
    return new_msg_list

def print_msg(msg_list, color=Color.white, style=Style.default, alignment=Alignment.default, align_width=16):
    """
    print the message with specified color, style and alignment.
    """
    if alignment == Alignment.center:
        msg_list = center_msg(msg_list, align_width)
    elif alignment == Alignment.left:
        msg_list = left_msg(msg_list, align_width)
    elif alignment ==Alignment.right:
        msg_list = right_msg(msg_list, align_width)

    msg = Message(color, style)
    msg.local_print(" ".join(msg_list))


def print_msg_list(msg_list, color=Color.white, style=Style.default, alignment=Alignment.default, align_width=16):
    """
    print the multiple lines message with specified color, style and alignment.
    """
    if alignment == Alignment.center:
        msg_list = center_msg(msg_list, align_width)
    elif alignment == Alignment.left:
        msg_list = left_msg(msg_list, align_width)
    elif alignment ==Alignment.right:
        msg_list = right_msg(msg_list, align_width)

    msg = Message(color, style)
    for message in msg_list:
        msg.local_print(message)


def print_info(message):
    """ 
    Print an information message.
    """
    msg = Message()
    msg.level_print(message, MessageLevel.Info)


def print_warning(message):
    """ 
    Print a warnning message.
    """
    msg = Message()
    msg.level_print(message, MessageLevel.Warning)


def print_error(message):
    """ 
    Print an error message.
    """
    msg = Message()
    msg.level_print(message, MessageLevel.Error)
