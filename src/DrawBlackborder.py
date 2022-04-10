import numpy as np
import cv2
import os

from PIL import Image

class Draw():
    def __init__(self):
        super().__init__()
    
    def __del__(self):
        os.remove("pos_Path_tmp.png")

    def createbackIMG(self,changeImage):
        img = cv2.imread(changeImage, -1)      # 读取切片图
        rows, cols, channels = img.shape
        l, w = img.shape[:2]

        kernel = np.ones((7, 7), np.float32)/49
        shape = np.array([[0, -1, 0],
                        [-1, 5, -1],
                        [0, -1, 0]])
        dst = cv2.filter2D(img, -1, kernel)
        dst = cv2.filter2D(dst, -1, shape)

        blank_image = np.zeros((l, w, 3), np.uint8)

        alpha = dst[:, :, 3]
        black_bgr = blank_image[:, :, :3]
        result = np.dstack([black_bgr, alpha])
        roi = result[0:rows, 0:cols]

        GrayImage = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        ret, mask_bin = cv2.threshold(GrayImage, 100, 255, cv2.THRESH_BINARY)

        # 黑白掩膜 和 大图切割区域 取和
        img1_bg = cv2.bitwise_and(roi, roi, mask=mask_bin)

        #纯黑无质量需求
        cv2.imwrite("pos_Path_tmp.png", img1_bg, [
                    int(cv2.IMWRITE_PNG_COMPRESSION), 0])

    def getEdge(self,saveImage):
        black = Image.open("pos_Path_tmp.png")
        posImage = Image.open(saveImage)
        result = Image.alpha_composite(black,posImage)
        result.save(saveImage)
