# 这是一个不会在正式运行中使用的代码
# 调用removebg.com的API，旨在利用第三方API（收费）
# 来进行图片的去除背景的处理
# 将会加载Jpg图片并发送给目标网站
# 在网络通畅的情况下会得到去除背景的PNG图
# 可以用来处理【褶皱图】

# API:
# 仅剩 50次、


from cutbg.API_removebg import API_removebg

import os

APIkey="swgmh9EQKCxBbEv52CJMqNpE"
Imgname="jialin.jpg"

folder = os.getcwd() 

if(os.path.exists(folder)):
    pass
else:
    os.makedirs(folder)
    print("Create successful folder")

Imgpath = folder + Imgname

print(Imgpath)

API_removebg(APIkey,Imgpath).API_RMBG_use()
