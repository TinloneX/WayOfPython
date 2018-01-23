#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 训练集由util.py 生成，仅手动生成了0，1的训练子集，故此处验证码使用简单的01组合
# 如需验证更多，请自行下载或生成训练字符集

from PIL import Image
import hashlib
import os

import math


class VectorCompare():
    def magnitude(self, concordance):
        total = 0
        for word, count in concordance.items():
            total += count ** 2
        return math.sqrt(total)

    def relation(self, concordance1, concordance2):
        topvalue = 0
        for word, count in concordance1.items():
            if word in concordance2:
                topvalue += count * concordance2[word]
        return topvalue / (self.magnitude(concordance1) * self.magnitude(concordance2))


def build_vector(im):
    d1 = {}
    count = 0
    for i in im.getdata():
        d1[count] = i
        count += 1
    return d1


v = VectorCompare()
iconset = ['0', '1']  # 如需验证其他请在此处添加字符并增加对应的训练集
imageset = []

for letter in iconset:
    for img in os.listdir('./iconset/%s/' % (letter)):
        temp = []
        if img != "Thumbs.db" and img != ".DS_Store":
            temp.append(build_vector(Image.open("./iconset/%s/%s" % (letter, img))))
        imageset.append({letter: temp})

im = Image.open("code.bmp")
im2 = Image.new("P", im.size, 255)
im.convert("P")
temp = {}

for x in range(im.size[1]):
    for y in range(im.size[0]):
        pix = im.getpixel((y, x))
        r, g, b = pix
        temp[pix] = pix
        if g==0 and b == 0:  # these are the numbers to get
            im2.putpixel((y, x), 0)

inletter = False
foundletter = False
start = 0
end = 0
letters = []

for y in range(im2.size[0]):  # slice across
    for x in range(im2.size[1]):  # slice down
        pix = im2.getpixel((y, x))
        if pix != 255:
            inletter = True

    if foundletter == False and inletter == True:
        foundletter = True
        start = y

    if foundletter == True and inletter == False:
        foundletter = False
        end = y
        letters.append((start, end))

    inletter = False

count = 0
for letter in letters:
    m = hashlib.md5()
    im3 = im2.crop((letter[0], 0, letter[1], im2.size[1]))

    guess = []

    for image in imageset:
        for x, y in image.items():
            if len(y) != 0:
                guess.append((v.relation(y[0], build_vector(im3)), x))

    guess.sort(reverse=True)
    print("", guess[0])

    count += 1
