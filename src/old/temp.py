import cv2
from PIL import Image
import numpy as np
import PIL.ImageChops as IC
import os


class FoldRender:
    # 褶皱图【前】，领口，褶皱图【后】，保存地址【路径】
    def __init__(self, FoldDiagram_front_path, FoldDiagram_front_neckline_path, FoldDiagram_back_path, savePath, needIMG):
        self.FoldDiagram_front_path = FoldDiagram_front_path
        self.FoldDiagram_front_neckline_path = FoldDiagram_front_neckline_path
        self.FoldDiagram_back_path = FoldDiagram_back_path
        self.savePath = savePath
        self.needIMG = needIMG
        h, w = self.specification(450, 120, 120)  # 450,448这个参数是极限距离，但任然有少量比例失常
        self.sameSize(h, w)
        super().__init__()
    '''
    def __del__(self):
        if os.path.isfile("tmp.jpg"):
            os.remove("tmp.jpg")
        if os.path.isfile("tmp_front.png"):
            os.remove("tmp_front.png")
        if os.path.isfile("tmp_back.png"):
            os.remove("tmp_back.png")
        if os.path.isfile("tmp_front_neckline.png"):
            os.remove("tmp_front_neckline.png")
    '''

    def specification(self, distance, addTop, addButton):
        # 左右裁剪，上下增加
        # 前 褶皱图处理
        FoldDiagram_front = Image.open(self.FoldDiagram_front_path)
        # FoldDiagram_front = FoldRender.alphabg2white_PIL(FoldDiagram_front)        #背景差异颜色处理
        cut_box = (int(FoldDiagram_front.size[0]//2 - distance),
                   0, int(FoldDiagram_front.size[0]//2 + distance), FoldDiagram_front.size[1])
        tmp_FoldDiagram_front = FoldDiagram_front.crop(cut_box)
        save_FoldDiagram_front = Image.new(
            "RGBA", (tmp_FoldDiagram_front.size[0], tmp_FoldDiagram_front.size[1]+addTop+addButton),(255,255,255,0))
        save_FoldDiagram_front.paste(tmp_FoldDiagram_front,(0,addTop))
        #tmp.show()
        
        # 后 褶皱图处理
        FoldDiagram_back = Image.open(self.FoldDiagram_back_path)
        #FoldDiagram_back = FoldRender.alphabg2white_PIL(FoldDiagram_back)
        cut_box = (int(FoldDiagram_back.size[0]//2 - distance),
                   0, int(FoldDiagram_back.size[0]//2 + distance), FoldDiagram_back.size[1])
        tmp_FoldDiagram_back = FoldDiagram_back.crop(cut_box)
        save_FoldDiagram_back = Image.new(
            "RGBA", (tmp_FoldDiagram_back.size[0], tmp_FoldDiagram_back.size[1]+addTop+addButton),(255,255,255,0))
        save_FoldDiagram_back.paste(tmp_FoldDiagram_front,(0,addTop))

        # 前 领口处理
        FoldDiagram_front_neckline = Image.open(
            self.FoldDiagram_front_neckline_path)
        #FoldDiagram_front_neckline = FoldRender.alphabg2white_PIL(FoldDiagram_front_neckline)
        cut_box = (int(FoldDiagram_front_neckline.size[0]//2 - distance),
                   0, int(FoldDiagram_front_neckline.size[0]//2 + distance), FoldDiagram_front_neckline.size[1])
        tmp_FoldDiagram_front_neckline = FoldDiagram_front_neckline.crop(
            cut_box)
        save_FoldDiagram_front_neckline = Image.new(
            "RGBA", (tmp_FoldDiagram_front_neckline.size[0], tmp_FoldDiagram_front_neckline.size[1]+addTop+addButton),(255,255,255,0))
        save_FoldDiagram_front_neckline.paste(tmp_FoldDiagram_front,(0,addTop))

        # tmp_FoldDiagram_front.show()
        save_FoldDiagram_front.save("tmp_front.png")
        save_FoldDiagram_back.save("tmp_back.png")
        save_FoldDiagram_front_neckline.save("tmp_front_neckline.png")
        return save_FoldDiagram_front.size

    # 统一需要的图片以及尺寸
    def sameSize(self, h, w):
        tmpIMG = Image.open(self.needIMG)
        tmpIMG = tmpIMG.resize((h, w))
        tmpIMG.save("tmp.jpg")
        print("---- 前期尺寸处理成功 ----")

    # ------------------------------------------------ #
    #                   前褶皱图渲染处理                 #
    # ------------------------------------------------ #
    def front_fusion(self):
        savePath = self.savePath + "\\ansFront.png"
        img1 = Image.open("tmp.jpg")
        img1 = img1.convert("RGBA")
        img2 = Image.open("tmp_front.png")
        print("开始正片叠底：", img1.mode, "----", img2.mode)
        result = IC.multiply(img2, img1)
        neckline = Image.open("tmp_front_neckline.png")
        result = Image.alpha_composite(result, neckline)
        result.save(savePath)
        print("保存褶皱图【前】渲染 成功")

    # ------------------------------------------------ #
    #                   后褶皱图渲染处理                #
    # ------------------------------------------------ #

    def back_fusion(self):
        savePath = self.savePath + "\\ansBack.png"
        img1 = Image.open("tmp.jpg")
        img1 = img1.convert("RGBA")
        img2 = Image.open("tmp_back.png")
        print("开始正片叠底：", img1.mode, "----", img2.mode)
        IC.multiply(img2, img1).save(savePath)
        print("保存褶皱图【后】渲染 成功")

    # PIL
    def transparent_back(self, img):
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

    def alphabg2white_PIL(self, img):
        img = img.convert('RGBA')
        sp = img.size
        width = sp[0]
        height = sp[1]
        print(sp)
        for yh in range(height):
            for xw in range(width):
                dot = (xw, yh)
                color_d = img.getpixel(dot)
                if(color_d[3] == 0):
                    color_d = (255, 0, 255, 255)
                    img.putpixel(dot, color_d)
        return img


a = FoldRender('save\\Tshirt\\font.png', 'save\\Tshirt\\font_neckline.png',
               'save\\Tshirt\\back.png', 'save\\Tshirt\\3XL\\eff', 'save\\Tshirt\\3XL\\tmp\\tmp_eff_forward.jpg')  # save\\Tshirt\\3XL\\tmp\\tmp_eff_forward.jpg  #save\\Tshirt\\3XL\\pic\\smoke.jpg
a.front_fusion()
a.back_fusion()
