#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re

import os

from pro4_text_parser.Handler import HTMLRenderer
from pro4_text_parser.Rule import *
from pro4_text_parser.util import *


class Parser():
    """解析器父类"""
    def __init__(self, handler):
        self.handler = handler
        self.rules = []
        self.filters = []

    def addRule(self,rule):
        """添加规则"""
        self.rules.append(rule)

    def addFilter(self, pattern, name):
        """添加过滤器"""
        def filter(block, handler):
            return re.sub(pattern, handler.sub(name), block)
        self.filters.append(filter)

    def parse(self, file):
        """解析"""
        self.handler.start('document')
        for block in blocks(file):
            for filter in self.filters:
                block = filter(block, self.handler)
            for rule in self.rules:
                if rule.condition(block):
                    last = rule.action(block, self.handler)
                    if last:break
        self.handler.end('document')


class BasicTextParser(Parser):
    """纯文本解析器"""
    def __init__(self, handler):
        Parser.__init__(self, handler)
        self.addRule(ListRule())
        self.addRule(ListItemRule())
        self.addRule(TitleRule())
        self.addRule(HeadingRule())
        self.addRule(ParagraphRule())

        self.addFilter(r'\*(.+?)\*', 'emphasis')
        self.addFilter(r'(http://[\.a-zA-Z/]+)', 'url')
        self.addFilter(r'([\.a-zA-Z]+@[\.a-zA-Z]+[a-zA-Z]+)', 'mail')


if __name__ == '__main__':
    handler = HTMLRenderer()
    parser = BasicTextParser(handler)
    with open('../static/pro4_text.txt', 'r') as f:
        parser.parse(f)
    # 请尝试将其保存并生成html文件
    if os.path.exists('./Test.html') and os.path.isfile('./Test.html'):
        os.remove('./Test.html')
    with open('./Test.html', 'w') as f:
        f.write('')


