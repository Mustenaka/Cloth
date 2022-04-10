from PIL import Image

import numpy as np
#import src.ColorSpace as ColorSpace

import os
import cv2
import threading


class Render(threading.Thread):
    # 切片图，渲染图，保存地址【文件】
    def __init__(self, ori_Path, backgroundImg, pos_Path, tmpname):
        threading.Thread.__init__(self)
        self.ori_Path = ori_Path
        self.backgroundImg = backgroundImg
        self.pos_Path = pos_Path
        self.tmpname = str(tmpname) + ".jpg"
        self.only_sameSize()

    def __del__(self):
        if os.path.isfile(self.tmpname):
            os.remove(self.tmpname)

    def run(self):
        fusion(self.ori_Path, self.tmpname, self.pos_Path)

    def only_sameSize(self):
        simg = Image.open(self.ori_Path)
        simg2 = Image.open(self.backgroundImg)
        simg2 = simg2.resize((simg.size), Image.ANTIALIAS)
        simg2.save(self.tmpname)


def fusion(ori_Path, tmpname, pos_Path):
    print(tmpname, os.path.isfile(tmpname))
    img = cv2.imread(tmpname, -1)       # 读取渲染图
    img2 = cv2.imread(ori_Path, -1)      # 读取切片图
    rows, cols, channels = img2.shape

    alpha = img2[:, :, 3]
    bgr = img[:, :, :3]
    result = np.dstack([bgr, alpha])

    roi = result[0:rows, 0:cols]
    GrayImage = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
    # 中值滤波
    GrayImage = cv2.medianBlur(GrayImage, 15)

    # mask_bin 是黑白掩膜
    ret, mask_bin = cv2.threshold(GrayImage, 100, 255, cv2.THRESH_BINARY)
    # mask_inv 是反色黑白掩膜
    mask_inv = cv2.bitwise_not(mask_bin)

    # 黑白掩膜 和 大图切割区域 取和
    img1_bg = cv2.bitwise_and(roi, roi, mask=mask_bin)
    cv2.imwrite(pos_Path, img1_bg, [
                int(cv2.IMWRITE_PNG_COMPRESSION), 9])      # 0 ~ 9 (low - high)

    Image.open(pos_Path).save(pos_Path, dpi=(96.0, 96.0))
    # ColorSpace.ColorSpace(pos_Path).changeColorSpace() #png不支持CMYK色彩空间
    print(tmpname, "保存切片渲染图片成功")
