import cv2
from PIL import Image
import numpy as np
import PIL.ImageChops as IC
import os


class FoldRender:
    # 褶皱图【前】，领口，褶皱图【后】，保存地址【路径】
    def __init__(self, FoldDiagram_front_path, FoldDiagram_front_hat_path,
                 FoldDiagram_back_path, FoldDiagram_back_hat_path,
                 FoldDiagram_front_tie_path,
                 hat_cloth_l, hat_cloth_r,
                 savePath, needIMG, x, y):
        self.FoldDiagram_front_path = FoldDiagram_front_path
        self.FoldDiagram_front_hat_path = FoldDiagram_front_hat_path
        self.FoldDiagram_back_path = FoldDiagram_back_path
        self.FoldDiagram_back_hat_path = FoldDiagram_back_hat_path
        self.FoldDiagram_front_tie_path = FoldDiagram_front_tie_path
        # 切片图直接进行合并对应
        self.hat_cloth_l = hat_cloth_l
        self.hat_cloth_r = hat_cloth_r

        self.savePath = savePath
        self.needIMG = needIMG
        self.sameSize(45, x, y)
        # self.moveUp(130)
        self.Mirror(487, 202, 0)
        super().__init__()

    def __del__(self):
        if os.path.isfile("tmp.jpg"):
            os.remove("tmp.jpg")
        if os.path.isfile("tmp2.jpg"):
            os.remove("tmp2.jpg")
        if os.path.isfile("tmp3.jpg"):
            os.remove("tmp3.jpg")

    # 统一需要的图片以及尺寸    --生成tmp1
    def sameSize(self, distance, x, y):
        tmpIMG = Image.open(self.needIMG)
        posIMG = Image.open(self.FoldDiagram_front_path)
        #tmpIMG = tmpIMG.resize((posIMG.size))
        tmp = Image.new("RGB", (posIMG.size))
        print("--------------------",
              tmp.size[0], "---------------", tmp.size[1])
        tmp.paste(
            tmpIMG, (posIMG.size[0]//2-tmpIMG.size[0]//2+y, posIMG.size[1]//2-tmpIMG.size[1]//2+distance+x))
        # print("--------------------",tmp.size[0],"---------------",tmp.size[1])
        tmp.save("tmp.jpg", dpi=(96, 96), quality=95)
        print("---- 前期尺寸处理成功 ----")

    # 前置条件--sameSize创建完成tmp.jpg文件后才执行   --生成tmp2
    def moveUp(self, distance):
        tmpIMG = Image.open("tmp.jpg")
        new_bg = Image.new("RGB", (tmpIMG.size))
        new_bg.paste(tmpIMG, (0, (0-distance)))
        new_bg.save("tmp2.jpg", dpi=(96, 96), quality=95)
        print("---- 前期尺寸处理成功 ----")

    # 前置条件--tmp.jpg生成--现阶段使用这个方式      --生成tmp3
    def Mirror(self, h, w, distance):
        tmpIMG = Image.open("tmp.jpg")
        hat_l = Image.open(self.hat_cloth_l)
        hat_r = Image.open(self.hat_cloth_r)
        hat_img = Image.new("RGB", (hat_l.size[0]*2, hat_l.size[1]))
        hat_img.paste(hat_l, (0, 0))
        hat_img.paste(hat_r, (hat_l.size[0], 0))
        hat_img = hat_img.resize((h, w), Image.ANTIALIAS)
        save_img = Image.new("RGB", (tmpIMG.size))
        save_img.paste(
            hat_img, (int(save_img.size[0]//2-hat_img.size[0]//2), int(distance)))
        print(hat_img.size, save_img.size)
        # save_img.show()
        save_img.save("tmp3.jpg", dpi=(96, 96), quality=95)
        print("---- 前期尺寸处理成功 ----")

    # ------------------------------------------------ #
    #                   前褶皱图渲染处理                 #
    # ------------------------------------------------ #
    def front_fusion(self):
        savePath = self.savePath + "\\ansFront.png"
        img1 = Image.open("tmp.jpg")
        img1 = img1.convert("RGBA")
        img2 = Image.open(self.FoldDiagram_front_path)
        print("开始正片叠底：", img1.mode, "----", img2.mode)
        result1 = IC.multiply(img2, img1)

        white = Image.new("RGBA", img2.size, color=(255, 255, 255, 255))

        moveImg = Image.open("tmp3.jpg")
        moveImg = moveImg.convert("RGBA")
        hat = Image.open(self.FoldDiagram_front_hat_path)
        result2 = IC.multiply(hat, moveImg)
        result = Image.alpha_composite(result1, result2)

        # 领带覆盖
        tie = Image.open(self.FoldDiagram_front_tie_path)
        result = Image.alpha_composite(result, tie)

        result = Image.alpha_composite(white, result)

        result.save(savePath, dpi=(96, 96), quality=95)
        self.removeAlpha(savePath)

        if os.path.isfile(savePath):
            os.remove(savePath)
        print("保存褶皱图【前】渲染 成功")

    # ------------------------------------------------ #
    #                   后褶皱图渲染处理                #
    # ------------------------------------------------ #

    def back_fusion(self):
        savePath = self.savePath + "\\ansBack.png"
        img1 = Image.open("tmp.jpg")
        img1 = img1.convert("RGBA")
        img2 = Image.open(self.FoldDiagram_back_path)
        print("开始正片叠底：", img1.mode, "----", img2.mode)
        result1 = IC.multiply(img2, img1)

        white = Image.new("RGBA", img2.size, color=(255, 255, 255, 255))

        moveImg = Image.open("tmp3.jpg")
        moveImg = moveImg.convert("RGBA")
        hat = Image.open(self.FoldDiagram_back_hat_path)
        result2 = IC.multiply(hat, moveImg)
        result = Image.alpha_composite(result1, result2)
        result = Image.alpha_composite(white, result)
        result.save(savePath, dpi=(96, 96), quality=95)
        self.removeAlpha(savePath)

        if os.path.isfile(savePath):
            os.remove(savePath)
        print("保存褶皱图【后】渲染 成功")

    def removeAlpha(self, path):
        img = cv2.imread(path, -1)       # 读取渲染图
        bgr = img[:, :, :3]
        cv2.imwrite(path[:-3]+"jpg", bgr, [
                    int(cv2.IMWRITE_PNG_COMPRESSION), 9])      # 0 ~ 9 (low - high)
