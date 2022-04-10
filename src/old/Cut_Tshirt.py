from PIL import Image
import os

#作废代码--旧的排版代码
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
            "RGBA", (img_forward.size[1]+2600, img_forward.size[0]+300))
        region_b = Image.new(
            "RGBA", (img_forward.size[1]+2600, img_forward.size[0]+300))

        # 前后旋转角度
        img_forward = img_forward.transpose(Image.ROTATE_270)
        img_backup = img_backup.transpose(Image.ROTATE_270)
        # 领口旋转
        img_neckline = img_neckline.transpose(Image.ROTATE_90)
        # 袖子反转
        img_sleeve_l = img_sleeve_l.transpose(Image.ROTATE_180)

        # 前部保存
        tmp = Image.new("RGBA", region_f.size)
        newtmp = Image.new("RGBA", region_f.size)
        tmp.paste(img_forward,
                  (region_f.size[0]//2-img_forward.size[0]//2, 300))
        Savetmp = Image.alpha_composite(newtmp, tmp)
        region_f = Image.alpha_composite(region_f, tmp)
        Savetmp.save(self.path_save+"\\after_forward.png")
        print("前件保存成功,尺寸：", img_forward.size)

        # 领口保存
        tmp = Image.new("RGBA", region_f.size)
        newtmp = Image.new("RGBA", region_f.size)
        tmp.paste(img_neckline,
                  (region_f.size[0]//2-img_neckline.size[0]//2, 100))
        Savetmp = Image.alpha_composite(newtmp, tmp)
        region_f = Image.alpha_composite(region_f, tmp)
        Savetmp.save(self.path_save+"\\after_neckline.png")
        print("领口保存成功,尺寸:", img_neckline.size)
        # region_f = Image.alpha_composite(region_f, tmp)        通道混合代码，本模板省略

        # 后件保存
        tmp = Image.new("RGBA", region_f.size)
        newtmp = Image.new("RGBA", region_f.size)
        tmp.paste(img_backup,
                  (region_f.size[0]//2-img_backup.size[0]//2, 300))
        Savetmp = Image.alpha_composite(newtmp, tmp)
        region_b = Image.alpha_composite(region_b, tmp)
        Savetmp.save(self.path_save+"\\after_backup.png")
        print("后件保存成功,尺寸:", img_backup.size)

        # 袖口保存-Left
        tmp = Image.new("RGBA", region_f.size)
        newtmp = Image.new("RGBA", region_f.size)
        tmp.paste(img_sleeve_l,
                  (region_f.size[0]//2-img_forward.size[0]//2-img_sleeve_l.size[0]+150, 0))
        Savetmp = Image.alpha_composite(newtmp, tmp)
        region_f = Image.alpha_composite(region_f, tmp)
        Savetmp.save(self.path_save+"\\after_sleeve_l.png")
        print("袖口[左]保存成功,尺寸:", img_sleeve_l.size)

        # 袖口保存-Right
        tmp = Image.new("RGBA", region_f.size)
        newtmp = Image.new("RGBA", region_f.size)
        tmp.paste(img_sleeve_r,
                  (region_f.size[0]//2+img_forward.size[0]//2-150, 0))
        Savetmp = Image.alpha_composite(newtmp, tmp)
        region_f = Image.alpha_composite(region_f, tmp)
        Savetmp.save(self.path_save+"\\after_sleeve_r.png")
        print("袖口[右]保存成功,尺寸:", img_sleeve_r.size)

        # 导出临时效果
        #Image._show(region_f)
        region_f.save(self.path_save+"\\after_front.png")
        region_b.save(self.path_save+"\\after_back.png")

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
