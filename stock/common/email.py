#!/usr/bin/python3
# -*- coding: utf-8 -*-

'''
实现定制化的发送电子邮件
'''
import zmail, pandas
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from stock.common.message import print_error, print_info


class Email:
    '''
    定制化发送邮件
    
    @args
    @sender: 发送者邮箱
    @password: 发送者邮箱密码或者终端授权码
    @receiver: 接收者邮箱
    @receiver_list: 接收者邮箱列表
    @subject: 邮件主题
    @mail_executer: zamil对象，发送邮件的执行对象
    '''
    def __init__(self, *args, **kwargs):
        '''
        Arguments:
        @sender 发送者邮箱，默认default@xxx.com
        @password 邮箱密码
        @receiver: 接收者邮箱
        @receiver_list: 接收者邮箱列表
        @subject: 邮件主题
        '''
        self.sender = ""
        self.password = ""
        self.receiver = None
        self.receiver_list = []
        
        if kwargs != None:
            keys = kwargs.keys()
            if "sender" in keys:
                self.sender = kwargs["sender"]
            if "password" in keys:
                self.password = kwargs["password"]
            if "receiver" in keys:
                self.receiver = kwargs["receiver"]
            if "receiver_list" in keys:
                self.receiver_list = kwargs["receiver_list"]
            if "subject" in keys:
                self.subject = kwargs["subject"]
        
        self.mail_executer = zmail.server(username=self.sender,password=self.password)
            
    def send_content(self, content=None, content_html=None):
        '''
        发送邮件
        
        Arguments:
            @content 文件正文，文本格式数据或字符串数据
            @content_html HTML格式文本
        '''
        if self.receiver != None:
            self.receiver_list.append(self.receiver)
        mail_msg = {
            "subject": self.subject,
            "content_text":content
            }
        if content_html != None:
            mail_msg["content_html"] = content_html
        try:
            self.mail_executer.send_mail(recipients=self.receiver, mail=mail_msg)
        except Exception as e:
            print_error("发送邮件时发生异常")
            print(e)
            return
        print_info("邮件发送成功")

def send_default_email(content=None, content_html=None, subject=None):
    '''
    快捷发送邮件接口，默认发送邮件给default@xxx.com
    
    Arguments:
        content: 普通文本，不可与content_html共存
        content_html: HTML格式文件，不可与content共存
        subject: 邮件主题
    '''
    print_info("发送邮件中...")
    email = Email(receiver="default@xxx.com", subject=subject)
    email.send_content(content_html=content_html, content=content)
    print_info("邮件发送完成...")
