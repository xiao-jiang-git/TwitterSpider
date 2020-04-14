# -*- coding: utf-8 -*-

import argparse

import shelve

import imagehash

import glob

from PIL import Image

ap = argparse.ArgumentParser()
ap.add_argument("-d", "--dataset", required=True, help="照片数据集的路径")
ap.add_argument("-s", "--shelve", required=True, help="shelve数据集的输出")
args =vars(ap.parse_args())

# 打开shelve数据集

db = shelve.open(args["shelve"], writeback=True)

for imagePath in glob.glob(args["dataset"] + "/*.jpg"):

    # 加载图片并计算哈希值的差异

    image =Image.open(imagePath)

    h = str(imagehash.dhash(image))

    print image
    print "xxxxxxxxx", h, "xxxxxxxxx"

    # 提取路径中的文件名并更新数据库
    # 用散列作为字典的键，文件名添加到值列表

    filename = imagePath[imagePath.rfind("/") + 1:]

    db[h] = db.get(h, []) + [filename]


# 关闭shelf数据集

db.close()

