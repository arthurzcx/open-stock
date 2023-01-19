# !/usr/bin/python
# -*- encoding:utf-8 -*-

# @author: Arthurz
# @date: 2022/04/03
# @version 1.0
# @desc: Class AppInfo.

class AppInfo():
    name = "StockSimulator"
    version = "V1.0.0"
    desc = "The software is used to simulate stocks market running mode. "
    desc_copyright = "Copyright (c) 2022-2052 by Jancy Technology Co., Ltd."
    rights = "ALL RIGHTS RESERVED https://www.jancy.com"

    def __init__(self):
        self.info_list = [self.name, self.version,
                          self.desc, self.desc_copyright, self.rights]
        self.msg_max_width = len(max(self.info_list, key=len, default=''))
