#!/usr/bin/env python3
# -*- coding: utf-8 -*-


class Handler():
    """处理程序父类"""

    def __init__(self):
        self.html = ''

    def callback(self, prefix, name, *args):
        method = getattr(self, prefix + name, None)
        if callable(method): return method(*args)

    def start(self, name):
        self.callback('start_', name)

    def end(self, name):
        self.callback('end_', name)

    def sub(self, name):
        def substitution(match):
            result = self.callback('sub_', name, match)
            if result is None: result = match.group(0)
            return result

        return substitution


class HTMLRenderer(Handler):
    """HTML处理程序，给文本块加相应的HTML标记"""

    def start_document(self):
        self.html += '<html><head><title>ShiYanLou</title></head><body>\n'
        print('<html><head><title>ShiYanLou</title></head><body>')

    def end_document(self):
        self.html += '</body></html>\n'
        print('</body></html>')

    def start_paragraph(self):
        self.html +='<p style="color:#444;">\n'
        print('<p style="color:#444;">')

    def end_paragraph(self):
        self.html += '</p>\n'
        print('</p>')

    def start_heading(self):
        self.html +='<h2 style="color:#68BE5D;">\n'
        print('<h2 style="color:#68BE5D;">')

    def end_heading(self):
        self.html+= '</h2>\n'
        print('</h2>')

    def start_list(self):
        self.html +='<ul style="color:#363736;">\n'
        print('<ul style="color:#363736;">')

    def end_list(self):
        self.html +='</ul>\n'
        print('</ul>')

    def start_listitem(self):
        self.html +='<li>\n'
        print('<li>')

    def end_listitem(self):
        self.html +='</li>\n'
        print('</li>')

    def sub_emphasis(self, match):
        return '<em>%s</em>' % match.group(1)

    def sub_url(self, match):
        return '<a target="_blank" style="text-decoration: none;color: #BC1A4B;" href="%s">%s</a>' % (
            match.group(1), match.group(1))

    def sub_mail(self, match):
        return '<a style="text-decoration: none;color: #BC1A4B;" href="mailto:%s">%s</a>' % (
            match.group(1), match.group(1))

    def feed(self, data):
        self.html += data + '\n'
        print(data)
