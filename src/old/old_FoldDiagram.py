import cv2
from PIL import Image
import numpy as np
import os

class FoldRender:
    # 褶皱图【前】，领口，褶皱图【后】，保存地址【路径】
    def __init__(self, oriPath, backgroundImg, posPath):
        self.oriPath = oriPath
        self.backgroundImg = backgroundImg
        self.posPath = posPath
        self.sameSize()
        super().__init__()

    def __del__(self):
        if os.path.isfile("tmp.jpg"):
            os.remove("tmp.jpg")

    # 统一需要的图片以及尺寸
    def sameSize(self):
        simg = Image.open(self.oriPath)
        simg2 = Image.open(self.backgroundImg)
        simg2 = simg2.resize((simg.size))
        simg2.save("tmp.jpg")

    # print test information
    def printTest(self):
        print(self.oriPath, os.path.isfile(self.oriPath))
        print(self.backgroundImg, os.path.isfile(self.backgroundImg))
        print(self.posPath, os.path.isdir(self.posPath))

    def back_fusion(self):
        img = cv2.imread("tmp.jpg")  # 读取渲染图
        img2 = cv2.imread(self.oriPath,-1)  # 读取褶皱图
        rows, cols, channels = img2.shape
        roi = img[0:rows, 0:cols]
        GrayImage = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
        # 中值滤波
        GrayImage = cv2.medianBlur(GrayImage, 5)
        # 均值滤波 -- 不添加会有毛躁感
        GrayImage = cv2.blur(GrayImage,(5,5))
        # mask_bin 是黑白掩膜
        ret, mask_bin = cv2.threshold(GrayImage, 254, 255, cv2.THRESH_BINARY)
        # mask_inv 是反色黑白掩膜
        mask_inv = cv2.bitwise_not(mask_bin)
        # 黑白掩膜 和 大图切割区域 取和
        img1_bg = cv2.bitwise_and(roi, roi, mask=mask_inv)
        #ans = cv2.addWeighted(img1_bg,0.1,a,0.9,0)
        cv2.imwrite(self.posPath, img1_bg,[int(cv2.IMWRITE_PNG_COMPRESSION), 9])

        cv2.imshow("test", mask_bin)
        cv2.waitKey(0)
        cv2.destroyAllWindows()



        #把背景色变得透明
        backColor = Image.open(self.posPath)
        backColor = FoldRender.transparent_back(backColor)
        #backColor.save(self.posPath)
        #Image._show(backColor)

        oriColor = Image.open(self.oriPath)
        backColor = Image.blend(backColor,oriColor,0.005)
        Image._show(backColor)

        #把背景色变得透明
        backColor = Image.open(self.posPath)
        backColor = FoldRender.transparent_back(backColor)
        backColor.save("ttttt.png")

        print("保存褶皱渲染图成功")

    def front_fusion(self,linkouPath):
        img = cv2.imread("tmp.jpg")  # 读取渲染图
        img2 = cv2.imread(self.oriPath,-1)  # 读取褶皱图
        rows, cols, channels = img2.shape
        roi = img[0:rows, 0:cols]
        GrayImage = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
        # 中值滤波
        GrayImage = cv2.medianBlur(GrayImage, 5)
        # 均值滤波 -- 不添加会有毛躁感
        GrayImage = cv2.blur(GrayImage,(7,7))
        # mask_bin 是黑白掩膜
        ret, mask_bin = cv2.threshold(GrayImage, 254, 255, cv2.THRESH_BINARY)
        # mask_inv 是反色黑白掩膜
        mask_inv = cv2.bitwise_not(mask_bin)
        # 黑白掩膜 和 大图切割区域 取和
        img1_bg = cv2.bitwise_and(roi, roi, mask=mask_inv)
        #ans = cv2.addWeighted(img1_bg,0.1,a,0.9,0)
        cv2.imwrite(self.posPath, img1_bg,[int(cv2.IMWRITE_PNG_COMPRESSION), 9])

        #把背景色变得透明
        backColor = Image.open(self.posPath)
        backColor = FoldRender.transparent_back(backColor)
        #backColor.save(self.posPath)
        #Image._show(backColor)

        oriColor = Image.open(self.oriPath)
        backColor = Image.blend(backColor,oriColor,0.185)

        linkou = Image.open(linkouPath)
        linkou = linkou.convert("RGBA")
        #backColor.paste(linkou,(0,0))
        backColor = Image.alpha_composite(backColor, linkou)

        Image._show(backColor)
        backColor.save("tempF.png")
        print("保存褶皱渲染图成功")


    #PIL
    def transparent_back(img):
        img = img.convert('RGBA')
        L, H = img.size
        color_0 = (0,0,0,255)   #要替换的颜色
        for h in range(H):
            for l in range(L):
                dot = (l,h)
                color_1 = img.getpixel(dot)
                if color_1 == color_0:
                    color_1 = color_1[:-1] + (0,)
                    img.putpixel(dot,color_1)
        return img

    def CVshow(Img):
        cv2.imshow("test",Img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    # 让alpha通道变成白色 -cv2
    def alpha2white_opencv2(img):
        sp=img.shape
        width=sp[0]
        height=sp[1]
        for yh in range(height):
            for xw in range(width):
                color_d=img[xw,yh]
                if(color_d[3]==0):
                    img[xw,yh]=[255,255,255,255]
        return img


posImg = "save\\Tshirt\\3XL\\tmptmp_eff.jpg"

a = FoldRender("save\\Tshirt\\default_back.png",posImg,"temp.png")

#a = FoldRender("save\\Tshirt\\3XL\\aaaa.png",posImg,"temp.png")
a.printTest()
a.back_fusion()
#a.front_fusion("save\\Tshirt\\front_neck3.png")



'''
            Offset = int(math.sqrt((img_sleeve_r.size[1]//2)**2 //2))
            print(Offset)
            l_box = (img_eff.size[0]-img_sleeve_r.size[0]-Offset,
                200,
                img_eff.size[0],
                img_sleeve_r.size[1]+200)
            l_img = img_eff.crop(l_box)
            l_img = l_img.rotate(Rotation_angle)
            #img_eff = img_eff.rotate(Rotation_angle)
            img_eff.show()
            l_img.show()
'''