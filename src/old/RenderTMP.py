import cv2
from PIL import Image
import numpy as np
import os


class Render:
    # 切片图，渲染图，保存地址【文件】
    def __init__(self, ori_front_Path, ori_back_Path, backgroundImg, pos_Path):
        self.ori_front_Path = ori_front_Path
        self.ori_back_Path = ori_back_Path
        self.backgroundImg = backgroundImg
        self.pos_Path = pos_Path
        self.sameSize()
        super().__init__()

    # def __del__(self):
    #    if os.path.isfile("tmp.jpg"):
    #        os.remove("tmp.jpg")

    # 统一需要的图片以及尺寸
    def sameSize(self):
        simg = Image.open(self.ori_front_Path)
        simg2 = Image.open(self.backgroundImg)
        #simg2 = simg2.resize((simg.size))

        tmp = Image.new("RGB", simg.size)
        simg2 = simg2.resize(
            (int(simg2.size[0]*3.2), int(simg2.size[1]*3.2)), Image.ANTIALIAS)
        tmp.paste(
            simg2, (tmp.size[0]//2-simg2.size[0]//2, tmp.size[1]-simg2.size[1]))
        tmp.save("tmp.jpg")

    # print test information
    def printTest(self):
        print(self.ori_front_Path, os.path.isfile(self.ori_front_Path))
        print(self.ori_back_Path, os.path.isfile(self.ori_back_Path))
        print(self.backgroundImg, os.path.isfile(self.backgroundImg))
        print(self.pos_Path, os.path.isdir(self.pos_Path))

    def fusion(oriPath, posPath):
        img = cv2.imread("tmp.jpg")     # 读取渲染图
        img2 = cv2.imread(oriPath)      # 读取切片图
        rows, cols, channels = img2.shape
        roi = img[0:rows, 0:cols]
        GrayImage = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
        # 中值滤波
        GrayImage = cv2.medianBlur(GrayImage, 5)
        # mask_bin 是黑白掩膜
        ret, mask_bin = cv2.threshold(GrayImage, 100, 255, cv2.THRESH_BINARY)
        # mask_inv 是反色黑白掩膜
        mask_inv = cv2.bitwise_not(mask_bin)
        # 黑白掩膜 和 大图切割区域 取和
        img1_bg = cv2.bitwise_and(roi, roi, mask=mask_bin)
        cv2.imwrite(posPath, img1_bg)


        backColor = Image.open(posPath)
        backColor = backColor.convert('RGBA')
        backColor = Render.transparent_back(backColor)
        backColor.save(posPath)


        print("保存图片成功")

    def CVshow(Img):
        cv2.imshow("test", Img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    # PIL
    def transparent_back(img):
        img = img.convert('RGBA')
        L, H = img.size
        color_0 = (0, 0, 0, 255)  # 要替换的颜色
        for h in range(H):
            for l in range(L):
                dot = (l, h)
                color_1 = img.getpixel(dot)
                if color_1 == color_0:
                    color_1 = color_1[:-1] + (0,)
                    img.putpixel(dot, color_1)
        return img

    def start(self):
        start_front = self.ori_front_Path
        start_back = self.ori_back_Path
        end_front = self.pos_Path+"front.png"
        end_back = self.pos_Path+"back.png"

        Render.fusion(start_front, end_front)
        Render.fusion(start_back, end_back)


saveRootPath = "save\\Tshirt\\3XL\\eff\\"
posImg = "save\\Tshirt\\3XL\\pic\\138-140914161056.jpg"

a = Render("save\\Tshirt\\3XL\\tmp\\after_front.png",
           "save\\Tshirt\\3XL\\tmp\\after_back.png",
           posImg, saveRootPath)
a.printTest()
a.start()


'''
orilist = [
    "save\\Tshirt\\3XL\\tmp\\after_forward.png",
    "save\\Tshirt\\3XL\\tmp\\after_neckline.png",
    "save\\Tshirt\\3XL\\tmp\\after_backup.png",
    "save\\Tshirt\\3XL\\tmp\\after_sleeve_l.png",
    "save\\Tshirt\\3XL\\tmp\\after_sleeve_r.png",
]
posImg = "save\\Tshirt\\3XL\\pic\\138-140924095606.jpg"
# Post-rendered picture
saveRootPath = "save\\Tshirt\\3XL\\eff\\"
savePath = [
    "rendered_forward.png",
    "rendered_neckline.png",
    "rendered_backup.png",
    "rendered_sleeve_l.png",
    "rendered_sleeve_r.png",
]

for i in range(0, 5):
    print(orilist[i],saveRootPath+savePath[i])
    a=Render(orilist[i],posImg,saveRootPath+savePath[i])
    a.printTest()
    a.fusion()
    del a
'''
