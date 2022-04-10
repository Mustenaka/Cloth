from PIL import Image
import os
import math

# T-shirt


class createBig():
    def __init__(self, path_save, posPath, path_backup, path_sleeve):
        self.path_save = path_save
        self.posPath = posPath
        # Open file
        self.img_backup = Image.open(path_backup)
        self.path_sleeve = Image.open(path_sleeve)

    def createBigPIC(self):
        # -- 参数设置区域 -- #
        bg_forward = Image.open(self.posPath)

        l = self.img_backup.size[1] / bg_forward.size[0]
        h = self.img_backup.size[0] / bg_forward.size[1]
        print(l, h)
        if l < h:
            self.Zoom_ratio = h
        else:
            self.Zoom_ratio = l
        Zoom_ratio = self.Zoom_ratio

        # 前后旋转角度
        img_backup = self.img_backup.transpose(Image.ROTATE_270)
        path_sleeve = self.path_sleeve.transpose(Image.ROTATE_270)

        region_f = Image.new(
            "RGB", img_backup.size)
        print("前件图案拉伸处理，mode:", region_f.mode, "\nszie:", region_f.size)

        bg_forward = bg_forward.resize(
            (int(bg_forward.size[0] * Zoom_ratio), int(bg_forward.size[1] * Zoom_ratio)), Image.ANTIALIAS)

        if(not os.path.exists(self.path_save+"\\back.png")):
            img_backup.save(self.path_save+"\\back.png")

        if(not os.path.exists(self.path_save+"\\sleeveL.png") or not os.path.exists(self.path_save+"\\sleeveR.png")):
            sleeveL = path_sleeve.crop(
                (0, 0, path_sleeve.size[0]//2, path_sleeve.size[1]))
            sleeveR = path_sleeve.crop(
                (path_sleeve.size[0]//2, 0, path_sleeve.size[0], path_sleeve.size[1]))
            sleeveL.save(self.path_save+"\\sleeveR.png")
            sleeveR.save(self.path_save+"\\sleeveL.png")

        bg_forward.save(self.path_save+"\\bigImage.jpg")
