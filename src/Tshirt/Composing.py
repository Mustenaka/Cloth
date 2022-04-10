from PIL import Image
import os


# Composing T-shirt
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

    # To resize all paths
    def Composing(self):
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

        # transpose 270°
        #img_forward = img_forward.transpose(Image.ROTATE_270)
        #img_backup = img_backup.transpose(Image.ROTATE_270)
        img_sleeve_l = img_sleeve_l.transpose(Image.ROTATE_180)
        img_sleeve_r = img_sleeve_r.transpose(Image.ROTATE_180)
        #img_neckline = img_neckline.transpose(Image.ROTATE_90)

        '''
        tmp_img_sleeve_l = img_sleeve_l.transpose(Image.ROTATE_180)
        tmp_img_sleeve_l.save(self.path_sleeve_l)
        tmp_img_sleeve_r = img_sleeve_r.transpose(Image.ROTATE_180)
        tmp_img_sleeve_r.save(self.path_sleeve_r)
        '''

        # region
        buffer_size = 1200  # not recommend too huge
        less_size = 100
        region = Image.new(
            "RGBA", (img_forward.size[0] - buffer_size + img_backup.size[0] + img_neckline.size[0],
                     img_backup.size[1] + img_sleeve_l.size[1] - less_size))

        # Place the front(forward)
        tmp = Image.new("RGBA", region.size)
        tmp.paste(img_forward,
                  (0,
                   img_sleeve_l.size[1] + img_neckline.size[1] - less_size))
        region = Image.alpha_composite(region, tmp)
        mid_forward = (img_forward.size[0])//2

        # Place the back(back)
        tmp = Image.new("RGBA", region.size)
        tmp.paste(img_backup,
                  (img_forward.size[0] - buffer_size + img_neckline.size[0],
                   img_sleeve_l.size[1] + img_neckline.size[1] - less_size - (img_backup.size[1] - img_forward.size[1])))
        region = Image.alpha_composite(region, tmp)
        mid_back = (img_forward.size[0] - buffer_size +
                    img_neckline.size[0] + img_backup.size[0]//2)

        # Place the neakline
        tmp = Image.new("RGBA", region.size)
        # tmp.paste(img_neckline,
        #           (int(region.size[0]//2-img_neckline.size[0]//2), img_sleeve_l.size[1] + img_neckline.size[1] + buffer_size-img_neckline.size[0]))
        tmp.paste(img_neckline,
                  (int(region.size[0]//2-img_neckline.size[0]//2), img_sleeve_l.size[1] - less_size - (img_backup.size[1] - img_forward.size[1])))
        region = Image.alpha_composite(region, tmp)

        # Place the double sleeve
        tmp = Image.new("RGBA", region.size)
        tmp.paste(img_sleeve_l,
                  (int(mid_forward - img_sleeve_l.size[0]//2), 0))
        region = Image.alpha_composite(region, tmp)
        tmp = Image.new("RGBA", region.size)
        tmp.paste(img_sleeve_r,
                  (int(mid_back - img_sleeve_r.size[0]//2), 0))
        region = Image.alpha_composite(region, tmp)
        # region.show()

        region.save(self.path_save+"\\Composed.png",
                    dpi=(96.0, 96.0), quality=95)


'''
style = "3XL"
a = Cut_Tshirt(
    "save\\Tshirt\\"+style+"\\eff",
    "save\\Tshirt\\"+style+"\\eff\\forward.png",
    "save\\Tshirt\\"+style+"\\eff\\neckline.png",
    "save\\Tshirt\\"+style+"\\eff\\back.png",
    "save\\Tshirt\\"+style+"\\eff\\sleeve.png",
    "save\\Tshirt\\"+style+"\\eff\\sleeve1.png"
)
a.printTest()
a.Composing()
'''
