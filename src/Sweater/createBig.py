from PIL import Image
import os
import math

# T-shirt


class createBig():
    def __init__(self, path_save, posPath, path_backup, path_hem, path_sleeve, path_cuff):
        self.path_save = path_save
        self.posPath = posPath
        # Open file
        self.img_backup = Image.open(path_backup)
        self.img_hem = Image.open(path_hem)
        self.path_sleeve = Image.open(path_sleeve)
        self.path_cuff = Image.open(path_cuff)

    def createBigPIC(self):
        # -- 参数设置区域 -- #
        bg_forward = Image.open(self.posPath)

        needLength = self.img_backup.size[1]
        needHigh = self.img_backup.size[0] + self.img_hem.size[0]
        l = needLength / bg_forward.size[0]
        h = needHigh / bg_forward.size[1]
        print(l, h)
        print("-----------")
        print(needLength, needHigh)
        if l < h:
            self.Zoom_ratio = h
        else:
            self.Zoom_ratio = l
        Zoom_ratio = self.Zoom_ratio

        # 前后旋转角度
        img_backup = self.img_backup.transpose(Image.ROTATE_270)
        path_sleeve = self.path_sleeve.transpose(Image.ROTATE_270)
        img_hem = self.img_hem.transpose(Image.ROTATE_270)
        path_cuff = self.path_cuff.transpose(Image.ROTATE_270)

        region_f = Image.new(
            "RGB", img_backup.size)
        print("前件图案拉伸处理，mode:", region_f.mode, "\nszie:", region_f.size)

        bg_forward = bg_forward.resize(
            (int(bg_forward.size[0] * Zoom_ratio), int(bg_forward.size[1] * Zoom_ratio)), Image.ANTIALIAS)

        if(not os.path.exists(self.path_save+"\\back.png")):
            result = Image.new(
                "RGBA", (img_backup.size[0], img_backup.size[1]+img_hem.size[1]))
            result.paste(img_backup, (0, 0))
            result.paste(img_hem, (img_backup.size[0]//2, img_backup.size[1]))
            result.save(self.path_save+"\\back.png")

        if(not os.path.exists(self.path_save+"\\sleeveL.png") or not os.path.exists(self.path_save+"\\sleeveR.png")):
            cuff_l = path_cuff.crop(
                (0, 0, path_cuff.size[0]//2, path_cuff.size[1]))
            sleeveL = path_sleeve.crop(
                (0, 0, path_sleeve.size[0]//2, path_sleeve.size[1]))

            cuff_r = path_cuff.crop(
                (path_cuff.size[0]//2, 0, path_cuff.size[0], path_cuff.size[1]))
            sleeveR = path_sleeve.crop(
                (path_sleeve.size[0]//2, 0, path_sleeve.size[0], path_sleeve.size[1]))

            result_l = Image.new(
                "RGBA", (sleeveL.size[0], sleeveL.size[1]+cuff_l.size[1]))
            result_r = Image.new(
                "RGBA", (sleeveL.size[0], sleeveL.size[1]+cuff_l.size[1]))

            result_l.paste(sleeveL, (0, 0))
            result_l.paste(
                cuff_l, (sleeveL.size[0]-cuff_l.size[0], sleeveL.size[1]))

            result_r.paste(sleeveR, (0, 0))
            result_r.paste(cuff_r, (0, sleeveR.size[1]))

            result_l.save(self.path_save+"\\sleeveR.png")
            result_r.save(self.path_save+"\\sleeveL.png")

        bg_forward.save(self.path_save+"\\bigImage.jpg")
