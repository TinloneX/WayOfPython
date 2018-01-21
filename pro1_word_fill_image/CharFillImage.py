#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PIL import Image
import os

ASCII_CHAR = list("$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'. ")
IMG_PATH = '../static/test.png'
SAVE_PATH = 'sheep.txt'


def get_char(r, g, b, alpha=256):
    """根据色值获取对应比例字符"""
    if alpha == 0:
        return ' '
    gray = int(0.2126 * r + 0.7152 * g + 0.0722 * b)
    length = len(ASCII_CHAR)
    unit = (256.0 + 1) / length  # 每多少个单位色值对应字符表一个字符
    return ASCII_CHAR[int(gray / unit)]  # gray/unit 计算对应第几个字符


def translate(come, to, RGBA=True):
    if not os.path.exists(come):
        raise FileExistsError('File (%s) not exist!' % come)
    if os.path.exists(to):
        os.remove(to)

    rgba = 'RGBA'
    if not RGBA:
        rgba = 'RGB'

    img = Image.open(come).convert(rgba)
    width = int(img.size[0] / 12)
    height = int(img.size[1] / 12)
    img = img.resize((width, height)).convert(rgba)

    txt = ''

    for y in range(height):
        for x in range(width):
            txt += get_char(*img.getpixel((x, y)))
        txt += '\n'

    with open(to, 'w') as file:
        file.write(txt)
        print('图片(%s)转换完成,存储至:%s' % (come, to))


if __name__ == '__main__':
    translate(IMG_PATH, SAVE_PATH)
