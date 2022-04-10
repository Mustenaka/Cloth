from PIL import Image
import os


class Cut_Tshirt():
    def __init__(self, path_save, path_forward, path_neckline, path_backup, path_sleeve_l, path_sleeve_r):
        self.path_save = path_save          # 保存地址
        self.path_forward = path_forward    # 前片地址
        self.path_neckline = path_neckline  # 领口地址
        self.path_backup = path_backup      # 后片地址
        self.path_sleeve_l = path_sleeve_l  # 左袖子地址
        self.path_sleeve_r = path_sleeve_r  # 右袖子地址

    # print test information
    def printTest(self):
        print(self.path_save, os.path.isdir(self.path_save))
        print(self.path_forward, os.path.isfile(self.path_forward))
        print(self.path_neckline, os.path.isfile(self.path_neckline))
        print(self.path_backup, os.path.isfile(self.path_backup))
        print(self.path_sleeve_l, os.path.isfile(self.path_sleeve_l))
        print(self.path_sleeve_r, os.path.isfile(self.path_sleeve_r))

    #private and useless
    def addTransparency(img, factor):
        img = img.convert('RGBA')
        img_blender = Image.new('RGBA', img.size, (0, 0, 0, 0))
        img = Image.blend(img_blender, img, factor)
        return img

    # To resize all paths
    def SameSize(self):
        # Open file
        img_forward = Image.open(self.path_forward)
        img_neckline = Image.open(self.path_neckline)
        img_backup = Image.open(self.path_backup)
        img_sleeve_l = Image.open(self.path_sleeve_l)
        img_sleeve_r = Image.open(self.path_sleeve_r)

        # from 'LA' convert to 'RGBA'
        img_forward = img_forward.convert("RGBA")
        img_neckline = img_neckline.convert("RGBA")
        img_backup = img_backup.convert("RGBA")
        img_sleeve_l = img_sleeve_l.convert("RGBA")
        img_sleeve_r = img_sleeve_r.convert("RGBA")

        # same size --- 以前件作为基准
        region_f = Image.new(
            "RGBA", (10000, 5000))

        # 前后旋转角度
        img_forward = img_forward.transpose(Image.ROTATE_270)
        img_backup = img_backup.transpose(Image.ROTATE_270)

        # 前部保存
        tmp = Image.new("RGBA", region_f.size)
        tmp.paste(img_forward,
                  (0, 0))
        region_f = Image.alpha_composite(region_f, tmp)
        print("前件保存成功,尺寸：", img_forward.size)

        # 领口保存
        tmp = Image.new("RGBA", region_f.size)
        tmp.paste(img_neckline,
                  (img_forward.size[0]+100, 400))
        region_f = Image.alpha_composite(region_f, tmp)
        print("领口保存成功,尺寸:", img_neckline.size)
        # region_f = Image.alpha_composite(region_f, tmp)        通道混合代码，本模板省略

        # 后件保存
        tmp = Image.new("RGBA", region_f.size)
        tmp.paste(img_backup,
                  (img_forward.size[0]+img_neckline.size[0]+200, 0))
        region_f = Image.alpha_composite(region_f, tmp)
        print("后件保存成功,尺寸:", img_backup.size)

        # 袖口保存-Left
        tmp = Image.new("RGBA", region_f.size)
        tmp.paste(img_sleeve_l,
                  (img_forward.size[0]+img_neckline.size[0]+img_forward.size[0]+300, 420))
        region_f = Image.alpha_composite(region_f, tmp)
        print("袖口[左]保存成功,尺寸:", img_sleeve_l.size)

        # 袖口保存-Right
        tmp = Image.new("RGBA", region_f.size)
        tmp.paste(img_sleeve_r,
                  (img_forward.size[0]+img_neckline.size[0]+img_forward.size[0]+img_sleeve_l.size[0]+400, 420))
        region_f = Image.alpha_composite(region_f, tmp)
        print("袖口[右]保存成功,尺寸:", img_sleeve_r.size)

        #Image._show(region_f)
        region_f.save("effic1.png")

a = Cut_Tshirt(
    "save\\Tshirt\\3XL\\tmp",
    "save\\Tshirt\\3XL\\ori\\023 前片 3XL-1.png",
    "save\\Tshirt\\3XL\\ori\\023 领口 3XL-1.png",
    "save\\Tshirt\\3XL\\ori\\023 后片 3XL-1.png",
    "save\\Tshirt\\3XL\\ori\\023 袖子 3XL-1.png",
    "save\\Tshirt\\3XL\\ori\\023 袖子1 3XL-1.png",
)
a.printTest()
a.SameSize()


'''
如果你问为什么这个代码不精简化类
那么告诉你这个可以预留去修改为做合成效果的排版布局
'''
