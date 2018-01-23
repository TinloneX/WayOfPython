#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PIL import Image
import hashlib
import time


im = Image.open('../static/1.bmp')

im.convert("P")

# ---------test------------
his = im.histogram()
values = {}

for i in range(256):
    values[i] = his[i]

for j, k in sorted(values.items(), key=lambda x: x[1], reverse=True)[:10]:
    print(j, k)

im2 = Image.new("P", im.size, 255)

for x in range(im.size[1]):
    for y in range(im.size[0]):
        r,g,b = im.getpixel((y, x))
        if g ==0 and b ==0:
            im2.putpixel((y, x), 0)

# im2.show()
# im2.save('gray.bmp')  # 验证二值图片

inletter = False
foundletter=False
start = 0
end = 0

letters = []

for y in range (im2.size[0]):
    for x in range(im2.size[1]):
        pix = im2.getpixel((y,x))
        if pix != 255:
            inletter = True
    if foundletter is False and inletter is True:
        foundletter = True
        start = y
    if foundletter is True and inletter is False:
        foundletter = False
        end = y
        letters.append((start, end))

    inletter=False

# print(letters)
count = 0
for letter in letters:
    m = hashlib.md5()
    im3 = im2.crop((letter[0], 0, letter[1], im2.size[1]))
    m.update(("%s%s" % (time.time(), count)).encode('utf-8'))
    im3.save("./iconset/1/%s.gif" % (m.hexdigest()))
    count += 1


