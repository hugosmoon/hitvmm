#-*- coding: UTF-8 -*-

class Page(object):
    '分页对象'

    def __init__(self, page_num=1, page_size=10, count=False):
        '''
        Page 初始化方法
        - @param page_num 页码，默认为1
        - @param page_size 页面大小, 默认为10
        - @param count 是否包含 count 查询
        '''
        # 当前页数
        self.page_num = page_num if page_num > 0 else 1
        # 分页大小
        self.page_size = page_size if page_size > 0 else 10
        # 总记录数
        self.total = 0
        # 总页数
        self.pages = 1
        # 起始行（用于 mysql 分页查询）
        self.start_row = (self.page_num - 1) * self.page_size
        # 结束行（用于 mysql 分页查询）
        self.end_row = self.start_row + self.page_size
