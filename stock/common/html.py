# -*- coding:utf-8 -*-
'''
构建HTML文件

Created on 2022年10月16日

@author: Arthur
@copyright: Jancy Co.,Ltd.
'''

# THML表格的css样式表
HTML_TABLE_STYLE = \
    """
        table {
            border-collapse:collapse;
        }
        td {
            border-collapse: collapse;
        }
        th {
            border-collapse: collapse;
        }
        tr {
            border-collapse: collapse;
        }
    """

def convert_text_to_html_headline(text, headlevel=3):
    '''
    将字符串str转换为HTML格式的标题
    
    Arguments:
        @text 字符串
        @headlevel int数字表示标题级别，1-6
    
    Returns:
        HTML格式的标题节点
    '''
    return "<h%d>%s</h%d>"%(headlevel, text, headlevel)

def convert_df_to_html_body(df, title, headlevel=3):
    '''
    将pandas.DataFrame数据转换为HTML格式的table格式
    
    Arguments:
        @df 表示pandas.DataFrame格式数据
        @title 表格标题
    
    Returns:
        代表html格式的文本或字符串
    '''
    html = ""
    # html += "<div>%s</div>"%(title)
    html += convert_text_to_html_headline(text=title,headlevel=headlevel)
    html += df.to_html(index=False)
    return html

def convert_text_to_p(text):
    '''
    将字符串text转换为HTML格式的p节点
    Arguments:
        @text 字符串
    
    Returns:
        HTML格式的段落节点
    '''
    return "<p>%s</p>"%(text)
    
def assembel_html(body):
    '''
    组装html内容
    
    Arguments:
        @body 代表html body的文本
        
    Returns:
        完整的html文本
    '''
    html = """
        <html>
            <head>
                <meta charset="utf-8">
                <style type="text/css">
                    %s
                </style>
            </head>
            <body>
                   %s 
            </body>
        </html>
        """%(HTML_TABLE_STYLE, body)
    return html