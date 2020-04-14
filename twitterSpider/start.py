# -*- coding: utf-8 -*-

import requests
import re
import os

gen_url = "https://video.twimg.com/ext_tw_video/1134172704142233600/pu/pl/1280x720/BAOnF12I1leKARLv.m3u8"

response_ts = requests.get(url=gen_url)

regex = re.compile("/ext_tw_video/.*\.ts")

result = regex.findall((response_ts.content))

print result[0]

root = "/Users/jiang/Pictures/video/"

if not os.path.exists(root):
    os.mkdir(root)

if os.path.exists(root):
    length = len(result)
    for i in range(length):
        tsname = str(i) + ".ts"  #result[i].split('/')[-1]
        path = root + tsname
        r = requests.get('https://video.twimg.com' + result[i])
        with open(path, 'wb') as f:
            f.write(r.content)
            f.close()
            print('\r' + tsname + " -->OK ({}/{}){:.2f}%".format(i, length, i*100/length))

# root = "/Users/jiang/Pictures/video/"
# dirs = "/Users/jiang/Pictures/video/"
# mp4 = "/Users/jiang/Pictures/output"
# filename = "video.mp4"
#
# a = 1
# content = ""
# lists = os.listdir(dirs)
# b = [lists[i:i+250] for i in range(0, len(lists), 250)]
# for lis in b:
#     cmd = "cd %s && ffmpeg -i \"concat:"%mp4
#     for file in lis:
#         if file != '.DS_Store':
#             file_path = os.path.join(dirs, file)
#             cmd += file_path + '|';
#             # print("文件：%s"%file_path)
#     cmd = cmd[:-1]
#     cmd += '" -bsf:a aac_adtstoasc -c copy -vcodec copy %s.mp4'%a
#     try:
#         os.system(cmd)
#         content += "file '%s.mp4'\n"%a
#         a = a+1
#     except:
#         print("Unexpected error")
#
# fp = open("%smp4list.txt"%mp4,'a+')
# fp.write(content)
# fp.close()
# mp4cmd = "cd %s && ffmpeg -y -f concat -i mp4list.txt -c copy %s"%(mp4,filename)
# os.system(mp4cmd)
