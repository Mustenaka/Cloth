from PIL import Image
#import src.ColorSpace as ColorSpace

import os


# Composing T-shirt
class Composing():
    def __init__(self, path_save, path_forward, path_backup, path_hem,
                 path_cuff_l, path_cuff_r, path_front_bag_cloth,
                 path_hat_cloth_l, path_hat_cloth_r,
                 path_sleeve_l, path_sleeve_r):
        self.path_save = path_save          # 保存地址
        self.path_forward = path_forward    # 前片地址
        self.path_backup = path_backup      # 后片地址
        self.path_hem = path_hem            # 下摆地址
        self.path_cuff_l = path_cuff_l      # 左袖口地址
        self.path_cuff_r = path_cuff_r      # 右袖口地址
        self.path_front_bag_cloth = path_front_bag_cloth      # 袋布地址【口袋】
        self.path_hat_cloth_l = path_hat_cloth_l    # 帽布左地址
        self.path_hat_cloth_r = path_hat_cloth_r    # 帽布右地址
        self.path_sleeve_l = path_sleeve_l  # 左袖子地址
        self.path_sleeve_r = path_sleeve_r  # 右袖子地址

    # print test information
    def printTest(self):
        print(self.path_save, os.path.isdir(self.path_save))
        print(self.path_forward, os.path.isfile(self.path_forward))
        print(self.path_backup, os.path.isfile(self.path_backup))
        print(self.path_hem, os.path.isfile(self.path_hem))
        print(self.path_cuff_l, os.path.isfile(self.path_cuff_l))
        print(self.path_cuff_r, os.path.isfile(self.path_cuff_r))
        print(self.path_front_bag_cloth,
              os.path.isfile(self.path_front_bag_cloth))
        print(self.path_hat_cloth_l, os.path.isfile(self.path_hat_cloth_l))
        print(self.path_hat_cloth_r, os.path.isfile(self.path_hat_cloth_r))
        print(self.path_sleeve_l, os.path.isfile(self.path_sleeve_l))
        print(self.path_sleeve_r, os.path.isfile(self.path_sleeve_r))

    # To resize all paths
    def Composing(self):
        # Open file
        img_forward = Image.open(self.path_forward)
        img_backup = Image.open(self.path_backup)
        path_hem = Image.open(self.path_hem)
        path_cuff_l = Image.open(self.path_cuff_l)
        path_cuff_r = Image.open(self.path_cuff_r)
        path_front_bag_cloth = Image.open(self.path_front_bag_cloth)
        path_hat_cloth_l = Image.open(self.path_hat_cloth_l)
        path_hat_cloth_r = Image.open(self.path_hat_cloth_r)
        img_sleeve_l = Image.open(self.path_sleeve_l)
        img_sleeve_r = Image.open(self.path_sleeve_r)

        # from 'LA' convert to 'RGBA'
        img_forward = img_forward.convert("RGBA")
        img_backup = img_backup.convert("RGBA")
        path_hem = path_hem.convert("RGBA")
        path_cuff_l = path_cuff_l.convert("RGBA")
        path_cuff_r = path_cuff_r.convert("RGBA")
        path_front_bag_cloth = path_front_bag_cloth.convert("RGBA")
        path_hat_cloth_l = path_hat_cloth_l.convert("RGBA")
        path_hat_cloth_r = path_hat_cloth_r.convert("RGBA")
        img_sleeve_l = img_sleeve_l.convert("RGBA")
        img_sleeve_r = img_sleeve_r.convert("RGBA")

        # transpose 180°
        #tmp_hat_cloth_l = path_hat_cloth_l.transpose(Image.ROTATE_180)
        # tmp_hat_cloth_l.save(self.path_hat_cloth_l)
        #tmp_hat_cloth_r = path_hat_cloth_r.transpose(Image.ROTATE_180)
        # tmp_hat_cloth_r.save(self.path_hat_cloth_r)
        # NO TRANSPOSE

        # region
        region = Image.new(
            "RGBA", (path_front_bag_cloth.size[0]+img_sleeve_l.size[0]+img_sleeve_r.size[0]-150,
                     img_backup.size[1]+img_sleeve_r.size[1]+path_hat_cloth_l.size[1]+path_hem.size[1]+500))

        print(region.mode, region.size)

        # Place the front(forward)
        tmp = Image.new("RGBA", region.size)
        tmp.paste(img_forward,
                  (0, 0))
        region = Image.alpha_composite(region, tmp)

        # Place the back(back)
        tmp = Image.new("RGBA", region.size)
        tmp.paste(img_backup,
                  (img_forward.size[0]+100, 0))
        region = Image.alpha_composite(region, tmp)

        # Place the cuff_l
        tmp = Image.new("RGBA", region.size)
        tmp.paste(path_cuff_l,
                  (int(img_forward.size[0]//5*3-path_cuff_l.size[0]),
                   img_forward.size[1]+100))
        region = Image.alpha_composite(region, tmp)

        # Place the path_cuff_r
        tmp = Image.new("RGBA", region.size)
        tmp.paste(path_cuff_r,
                  (int(img_forward.size[0]//5*3-path_cuff_l.size[0]),
                   img_forward.size[1]+path_cuff_l.size[1]+200))
        region = Image.alpha_composite(region, tmp)

        # Place the front_bag_cloth
        tmp = Image.new("RGBA", region.size)
        tmp.paste(path_front_bag_cloth,
                  (0, img_forward.size[1]+img_sleeve_r.size[1]-path_front_bag_cloth.size[1]))
        region = Image.alpha_composite(region, tmp)

        # Place the sleeve_l
        tmp = Image.new("RGBA", region.size)
        tmp.paste(img_sleeve_l,
                  (path_front_bag_cloth.size[0]-200,
                   img_forward.size[1] + 100))
        region = Image.alpha_composite(region, tmp)

        # Place the sleeve_r
        tmp = Image.new("RGBA", region.size)
        tmp.paste(img_sleeve_r,
                  (path_front_bag_cloth.size[0] + img_sleeve_l.size[0]-150,
                   img_forward.size[1] + 100))
        region = Image.alpha_composite(region, tmp)

        # Place the hat_L
        tmp = Image.new("RGBA", region.size)
        tmp.paste(path_hat_cloth_r,
                  (path_front_bag_cloth.size[0]-200,
                   img_forward.size[1]+img_sleeve_l.size[1]+200))
        region = Image.alpha_composite(region, tmp)

        # Place the hat_r
        tmp = Image.new("RGBA", region.size)
        tmp.paste(path_hat_cloth_l,
                  (path_front_bag_cloth.size[0] + img_sleeve_l.size[0]-200,
                   img_forward.size[1]+img_sleeve_l.size[1]+200))
        region = Image.alpha_composite(region, tmp)

        # Place the hem
        tmp = Image.new("RGBA", region.size)
        tmp.paste(path_hem,
                  (region.size[0]//2-path_hem.size[0]//2,
                   region.size[1]-path_hem.size[1]-100))
        region = Image.alpha_composite(region, tmp)

        region.save(self.path_save+"\\Composed.png",
                    dpi=(96.0, 96.0), quality=95)
        # ColorSpace.ColorSpace(self.path_save+"\\Composed.png").changeColorSpace()
