from PIL import Image
import os
import math

# Sweater


class Slice_process():
    def __init__(self, path_save, path_forward, path_backup, path_hem,
                 path_cuff_l, path_cuff_r, path_front_bag_cloth,
                 path_hat_cloth_l, path_hat_cloth_r, path_sleeve_l, path_sleeve_r,
                 posPath, TMPSAVEPATH, hat_move, Sleeve_pos):
        self.path_save = path_save
        self.posPath = posPath
        self.TMPSAVEPATH = TMPSAVEPATH
        # Open file
        self.img_forward = Image.open(path_forward)
        self.img_backup = Image.open(path_backup)
        self.img_hem = Image.open(path_hem)
        self.img_cuff_l = Image.open(path_cuff_l)
        self.img_cuff_r = Image.open(path_cuff_r)
        self.img_front_bag_cloth = Image.open(path_front_bag_cloth)
        self.img_hat_cloth_l = Image.open(path_hat_cloth_l)
        self.img_hat_cloth_r = Image.open(path_hat_cloth_r)
        self.img_sleeve_l = Image.open(path_sleeve_l)
        self.img_sleeve_r = Image.open(path_sleeve_r)
        # from 'LA' convert to 'RGBA'
        self.img_forward = self.img_forward.convert("RGBA")
        self.img_backup = self.img_backup.convert("RGBA")
        self.img_hem = self.img_hem.convert("RGBA")
        self.img_cuff_l = self.img_cuff_l.convert("RGBA")
        self.img_cuff_r = self.img_cuff_r.convert("RGBA")
        self.img_front_bag_cloth = self.img_front_bag_cloth.convert("RGBA")
        self.img_hat_cloth_l = self.img_hat_cloth_l.convert("RGBA")
        self.img_hat_cloth_r = self.img_hat_cloth_r.convert("RGBA")
        self.img_sleeve_l = self.img_sleeve_l.convert("RGBA")
        self.img_sleeve_r = self.img_sleeve_r.convert("RGBA")
        # 默认参数
        self.Zoom_ratio = 2.3                     # 缩放倍率--- 整体图片在渲染的时候的缩放率，推荐2.2
        # 移动参数
        self.pasteDown = 0  # 图案粘贴沉浮
        self.pasteRight = 0  # 图案粘贴左右移动
        # 帽子图片的下移参数
        self.hat_move_x = hat_move[0] * 6.3
        self.hat_move_y = hat_move[1] * 6.3
        #self.hat_move_x = hat_move[0] * 4.15
        #self.hat_move_y = hat_move[1] * 3.9
        # 袖子的自由移动
        self.lSleeve_pos = Sleeve_pos[0]
        self.rSleeve_pos = Sleeve_pos[1]

    def setflag(self, pasteDown, pasteRight):
        # 注：切片和褶皱图差不多有5倍的大小差
        self.pasteDown = pasteDown * 5
        self.pasteRight = pasteRight * 5
        # 把默认处理设置为0，不处理
        self.Boundary_data = 0
        self.Boundary_data_top = 0
        self.Elongation_factor = 1.0
        # 缩放倍率--- 整体图片在渲染的时候的缩放率，推荐2.2
        # 注意，卫衣的缩放倍率需要额外放大
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

    # 处理背景图片使之可以较为方便的对 前件 and 后件 进行渲染
    # Mag(Magnification):倍率，整体图片缩放倍率
    # ------------------------------------------------------------- #
    #                   袖口与前件与下摆与口袋拉伸处理                 #
    #  ------------------------------------------------------------ #

    def Single_processing_new_Tshirt_forward(self):
        # -- 参数设置区域 -- #
        Elongation_factor = self.Elongation_factor     # 拉伸系数 --- 左右拉伸使用 ，推荐3.2
        Zoom_ratio = self.Zoom_ratio                   # 缩放倍率--- 整体图片在渲染的时候的缩放率，推荐2.2
        # 边界数据(像素) --- 截取横向长度，推荐300
        Boundary_data = self.Boundary_data
        # 边界数据(像素) --- 截取上方向长度，推荐300
        Boundary_data_top = self.Boundary_data_top
        # 以前件作为基准
        # 前后旋转角度
        img_forward = self.img_forward.transpose(Image.ROTATE_270)
        img_hem = self.img_hem.transpose(Image.ROTATE_90)
        img_front_bag_cloth = self.img_front_bag_cloth.transpose(
            Image.ROTATE_270)
        img_sleeve_l = self.img_sleeve_l.transpose(Image.ROTATE_270)
        img_sleeve_r = self.img_sleeve_r.transpose(Image.ROTATE_270)
        img_cuff_l = self.img_cuff_l.transpose(Image.ROTATE_270)
        img_cuff_r = self.img_cuff_r.transpose(Image.ROTATE_270)

        img_hem.save(self.TMPSAVEPATH+"\\hem.png", dpi=(96, 96))
        img_forward.save(self.TMPSAVEPATH+"\\forward.png", dpi=(96, 96))
        img_front_bag_cloth.save(
            self.TMPSAVEPATH+"\\front_bag_cloth.png", dpi=(96, 96))
        img_sleeve_l.save(self.TMPSAVEPATH+"\\sleeve_l.png", dpi=(96, 96))
        img_sleeve_r.save(self.TMPSAVEPATH+"\\sleeve_r.png", dpi=(96, 96))
        img_cuff_l.save(self.TMPSAVEPATH+"\\cuff_l.png", dpi=(96, 96))
        img_cuff_r.save(self.TMPSAVEPATH+"\\cuff_r.png", dpi=(96, 96))

        region_f = Image.new(
            "RGB", (int(img_forward.size[0]),
                    img_forward.size[1]+img_hem.size[1]))
        print("前件图案拉伸处理，mode:", region_f.mode, "\nszie:", region_f.size)

        # 整体缩放
        bg_forward = Image.open(self.posPath)

        bg_forward = bg_forward.resize(
            (int(bg_forward.size[0] * Zoom_ratio + 0.5), int(bg_forward.size[1] * Zoom_ratio + 0.5)), Image.ANTIALIAS)
        # bg_forward.save(self.path_save+"\\bigImage.jpg")

        start = bg_forward.size[1]//2 - region_f.size[1]//2 - self.pasteDown
        end = bg_forward.size[1]//2 + region_f.size[1]//2 - self.pasteDown

        if start <= 0:
            start = 0
            end = region_f.size[1]

        if end >= bg_forward.size[1]:
            start = bg_forward.size[1] - region_f.size[1]
            end = bg_forward.size[1]

        startl = bg_forward.size[0]//2 - region_f.size[0]//2 - self.pasteRight
        endl = bg_forward.size[0]//2 + region_f.size[0]//2 - self.pasteRight

        if startl < 0:
            startl = 0
            endl = region_f.size[0]

        if endl >= bg_forward.size[0]:
            startl = bg_forward.size[0] - region_f.size[0]
            endl = bg_forward.size[0]

        bg_box = (startl,
                  start,
                  endl,
                  end)
        region_f = bg_forward.crop(bg_box)
        # region_f.save(self.path_save+"\\zhezhou.jpg")
        # bg_forward.save("aa.jpg")
        # region_f.paste(
        #    bg_forward, (region_f.size[0]//2-bg_forward.size[0]//2+self.pasteRight,  region_f.size[1]-bg_forward.size[1]+self.pasteDown))
        #---------------------------------------------------------------#
        #---------------------------------------------------------------#
        lSleeve_pos = self.lSleeve_pos
        rSleeve_pos = self.rSleeve_pos
        # 防止lSleeve_pos超界处理
        if lSleeve_pos[0] < 0:
            lSleeve_pos = (0, lSleeve_pos[1])
        if lSleeve_pos[1] < 0:
            lSleeve_pos = (lSleeve_pos[0], 0)
        if lSleeve_pos[0] > bg_forward.size[0]-img_sleeve_l.size[0]//2:
            lSleeve_pos[0] = (
                bg_forward.size[0]-img_sleeve_l.size[0]//2, lSleeve_pos[1])
        if lSleeve_pos[1] > bg_forward.size[1]-img_sleeve_l.size[1]:
            lSleeve_pos[0] = (
                lSleeve_pos[0], bg_forward.size[1]-img_sleeve_l.size[1])

        # 防止rSleeve_pos超界处理
        if rSleeve_pos[0] < 0:
            rSleeve_pos = (0, rSleeve_pos[1])
        if rSleeve_pos[1] < 0:
            rSleeve_pos = (rSleeve_pos[0], 0)
        if rSleeve_pos[0] > bg_forward.size[0]-img_sleeve_l.size[0]//2:
            rSleeve_pos = (
                bg_forward.size[0]-img_sleeve_l.size[0]//2, rSleeve_pos[1])
        if rSleeve_pos[1] > bg_forward.size[1]-img_sleeve_l.size[1]:
            rSleeve_pos = (
                rSleeve_pos[0], bg_forward.size[1]-img_sleeve_l.size[1])

        l_box = (lSleeve_pos[0], lSleeve_pos[1],
                 lSleeve_pos[0] + img_sleeve_l.size[0]//2,
                 lSleeve_pos[1] + img_sleeve_l.size[1])

        #---------------------------------------------------------------#
        # 左边袖子修改
        sleeve_l_box = (lSleeve_pos[0],
                        lSleeve_pos[1],
                        lSleeve_pos[0]+img_sleeve_l.size[0]//2,
                        lSleeve_pos[1]+img_sleeve_l.size[1])
        print(sleeve_l_box)
        sleeve_l_img = bg_forward.crop(sleeve_l_box)
        # sleeve_l_img.show()
        sleeve_l_img.save(
            self.path_save+"\\tmp_eff_sleeve_l_0.jpg", dpi=(96, 96), quality=95)
        sleeve_l_img.save(
            self.path_save+"\\tmp_eff_sleeve_l_1.jpg", dpi=(96, 96), quality=95)

        # 右边袖子修改
        sleeve_r_box = (rSleeve_pos[0],
                        rSleeve_pos[1],
                        rSleeve_pos[0]+img_sleeve_l.size[0]//2,
                        rSleeve_pos[1]+img_sleeve_l.size[1])
        sleeve_r_img = bg_forward.crop(sleeve_r_box)
        sleeve_r_img.save(
            self.path_save+"\\tmp_eff_sleeve_r_0.jpg", dpi=(96, 96), quality=95)
        sleeve_r_img.save(
            self.path_save+"\\tmp_eff_sleeve_r_1.jpg", dpi=(96, 96), quality=95)

        # 左边袖口处理img_cuff_l
        cuff_l_box = (lSleeve_pos[0],
                      lSleeve_pos[1]+img_sleeve_l.size[1],
                      lSleeve_pos[0]+img_cuff_l.size[0]//2,
                      lSleeve_pos[1]+img_sleeve_l.size[1]+img_cuff_l.size[1])
        cuff_l_img = bg_forward.crop(cuff_l_box)
        cuff_l_img.save(self.path_save+"\\tmp_eff_cuff_l_0.jpg",
                        dpi=(96, 96), quality=95)
        cuff_l_img.save(self.path_save+"\\tmp_eff_cuff_l_1.jpg",
                        dpi=(96, 96), quality=95)

        # 右边袖口处理img_cuff_r
        cuff_r_box = (rSleeve_pos[0],
                      rSleeve_pos[1]+img_sleeve_l.size[1],
                      rSleeve_pos[0]+img_cuff_l.size[0]//2,
                      lSleeve_pos[1]+img_sleeve_l.size[1]+img_cuff_l.size[1])
        cuff_r_img = bg_forward.crop(cuff_r_box)
        cuff_r_img.save(self.path_save+"\\tmp_eff_cuff_r_0.jpg",
                        dpi=(96, 96), quality=95)
        cuff_r_img.save(self.path_save+"\\tmp_eff_cuff_r_1.jpg",
                        dpi=(96, 96), quality=95)

        # 下摆处理  hem -----------------------------------------
        hem_box = (
            region_f.size[0]-img_hem.size[0]//2,
            region_f.size[1]-img_hem.size[1],
            region_f.size[0], region_f.size[1]
        )
        hem_img = region_f.crop(hem_box)
        hem_img.save(self.path_save+"\\tmp_eff_hem_l.jpg",
                     dpi=(96, 96), quality=95)
        # 图片裁剪，前件处理 -------------------------------------
        region_box = (
            0,
            0,
            img_forward.size[0],
            region_f.size[1]-hem_img.size[1]
        )
        region_f = region_f.crop(region_box)
        region_f.save(self.path_save+"\\tmp_eff_forward.jpg",
                      dpi=(96, 96), quality=95)
        # 口袋处理 img_front_bag_cloth --------------------------
        front_bag_box = (
            int(region_f.size[0]//2 - img_front_bag_cloth.size[0]//2),
            region_f.size[1] - img_front_bag_cloth.size[1],
            int(region_f.size[0]//2 + img_front_bag_cloth.size[0]//2),
            region_f.size[1]
        )
        front_bag_img = region_f.crop(front_bag_box)
        front_bag_img.save(
            self.path_save+"\\tmp_eff_front_bag_cloth.jpg", dpi=(96, 96), quality=95)

    # ------------------------------------------------------ #
    #                       后件与下摆拉伸处理                 #
    #  ----------------------------------------------------- #

    def Single_processing_new_Tshirt_back(self):
        # 缩放倍率--- 整体图片在渲染的时候的缩放率
        Zoom_ratio = self.Zoom_ratio
        # 前后旋转角度
        img_backup = self.img_backup.transpose(Image.ROTATE_270)
        img_hem = self.img_hem.transpose(Image.ROTATE_90)
        #img_sleeve_l = self.img_sleeve_l.transpose(Image.ROTATE_270)
        #img_sleeve_r = self.img_sleeve_r.transpose(Image.ROTATE_270)
        #img_cuff_l = self.img_cuff_l.transpose(Image.ROTATE_270)
        #img_cuff_r = self.img_cuff_r.transpose(Image.ROTATE_270)
        #img_hat_cloth_l = self.img_hat_cloth_l.transpose(Image.ROTATE_270)
        #img_hat_cloth_r = self.img_hat_cloth_r.transpose(Image.ROTATE_180)
        #img_hat_cloth_r = img_hat_cloth_r.transpose(Image.FLIP_TOP_BOTTOM)
        img_hat_cloth_r = self.img_hat_cloth_r.transpose(Image.FLIP_LEFT_RIGHT)
        img_hat_cloth_l = self.img_hat_cloth_l
        #img_hat_cloth_r = self.img_hat_cloth_r

        img_backup.save(self.TMPSAVEPATH+"\\back.png",
                        dpi=(96, 96), quality=95)
        #img_hat_cloth_l_tmp = img_hat_cloth_l.transpose(Image.ROTATE_180)
        #img_hat_cloth_r_tmp = img_hat_cloth_r.transpose(Image.ROTATE_180)

        img_hat_cloth_l.save(
            self.TMPSAVEPATH+"\\hat_cloth_l.png", dpi=(96, 96))
        img_hat_cloth_r.save(
            self.TMPSAVEPATH+"\\hat_cloth_r.png", dpi=(96, 96))

        region_f = Image.new(
            "RGB", (int(img_backup.size[0]),
                    img_backup.size[1]+img_hem.size[1]))
        print("后件图案拉伸处理，mode:", region_f.mode, "\nszie:", region_f.size)

        # 整体缩放
        bg_forward = Image.open(self.posPath)

        bg_forward = bg_forward.resize(
            (int(bg_forward.size[0] * Zoom_ratio + 0.5), int(bg_forward.size[1] * Zoom_ratio + 0.5)), Image.ANTIALIAS)

        # 防止黑边设计的约束
        start = bg_forward.size[1]//2 - region_f.size[1]//2 - self.pasteDown
        end = bg_forward.size[1]//2 + region_f.size[1]//2 - self.pasteDown

        if start <= 0:
            start = 0
            end = region_f.size[1]

        if end >= bg_forward.size[1]:
            start = bg_forward.size[1] - region_f.size[1]
            end = bg_forward.size[1]

        startl = bg_forward.size[0]//2 - region_f.size[0]//2 - self.pasteRight
        endl = bg_forward.size[0]//2 + region_f.size[0]//2 - self.pasteRight

        if startl < 0:
            startl = 0
            endl = region_f.size[0]

        if endl >= bg_forward.size[0]:
            startl = bg_forward.size[0] - region_f.size[0]
            endl = bg_forward.size[0]

        bg_box = (startl,
                  start,
                  endl,
                  end)
        region_f = bg_forward.crop(bg_box)

        # region_f.paste(
        #    bg_forward, (region_f.size[0]//2-bg_forward.size[0]//2+self.pasteRight, region_f.size[1]-bg_forward.size[1]+self.pasteDown))

        '''
        # 26更新，作废这个区域的代码，采用更加高效的方式
        #---------------------------------------------------------------#
        #---------------------------------------------------------------#
        # 左边袖子修改
        sleeve_l_box = (0,
                        region_f.size[1]-img_hem.size[1]-img_sleeve_l.size[1],
                        img_sleeve_l.size[0]//2,
                        region_f.size[1]-img_hem.size[1])
        sleeve_l_img = region_f.crop(sleeve_l_box)
        sleeve_l_img.save(
            self.path_save+"\\tmp_eff_sleeve_l_1.jpg", dpi=(96, 96), quality=95)

        # 右边袖子修改
        sleeve_r_box = (region_f.size[0]-img_sleeve_r.size[0]//2,
                        region_f.size[1]-img_hem.size[1]-img_sleeve_r.size[1],
                        region_f.size[0],
                        region_f.size[1]-img_hem.size[1])
        sleeve_r_img = region_f.crop(sleeve_r_box)
        sleeve_r_img.save(
            self.path_save+"\\tmp_eff_sleeve_r_1.jpg", dpi=(96, 96), quality=95)

        # 左边袖口处理img_cuff_l
        cuff_l_box = (0,
                      region_f.size[1]-img_hem.size[1],
                      img_backup.size[0]//2,
                      region_f.size[1])
        cuff_l_img = region_f.crop(cuff_l_box)
        cuff_l_img.save(self.path_save+"\\tmp_eff_cuff_l_1.jpg",
                        dpi=(96, 96), quality=95)

        # 右边袖口处理img_cuff_r
        cuff_r_box = (region_f.size[0]-img_cuff_r.size[0],
                      region_f.size[1]-img_hem.size[1],
                      region_f.size[0],
                      region_f.size[1])
        cuff_r_img = region_f.crop(cuff_r_box)
        cuff_r_img.save(self.path_save+"\\tmp_eff_cuff_r_1.jpg",
                        dpi=(96, 96), quality=95)
        '''
        # 帽子的切片处理 0---镜像，1---居中
        # 2-22更新，删除居中效果
        # Downshift = int(self.hat_move + 0.5)
        # hat_box = (int(region_f.size[0]//2-img_hat_cloth_l.size[0]//2), Downshift,
        #           int(region_f.size[0]//2+img_hat_cloth_l.size[0]//2), img_hat_cloth_l.size[1] + Downshift)
        # 3-10更新，修改帽子处理排版为自由排版
        if self.hat_move_x < 0:
            self.hat_move_x = 0
        if self.hat_move_x > bg_forward.size[0] - img_hat_cloth_l.size[0]:
            self.hat_move_x = bg_forward.size[0] - img_hat_cloth_l.size[0]

        if self.hat_move_y < 0:
            self.hat_move_y = 0
        if self.hat_move_y > bg_forward.size[1] - img_hat_cloth_l.size[1]:
            self.hat_move_y = bg_forward.size[1] - img_hat_cloth_l.size[1]

        hat_box = (self.hat_move_x, self.hat_move_y,
                   self.hat_move_x+img_hat_cloth_l.size[0], self.hat_move_y+img_hat_cloth_l.size[1])
        print("帽子的相对位置：", hat_box)
        hat_cloth_l = bg_forward.crop(hat_box)
        hat_cloth_r = hat_cloth_l.transpose(Image.FLIP_LEFT_RIGHT)
        #hat_cloth_l = hat_cloth_l.transpose(Image.ROTATE_180)
        #hat_cloth_r = hat_cloth_r.transpose(Image.ROTATE_180)
        hat_cloth_l.save(
            self.path_save+"\\tmp_eff_hat_cloth_r.jpg", dpi=(96, 96), quality=95)
        hat_cloth_r.save(
            self.path_save+"\\tmp_eff_hat_cloth_l.jpg", dpi=(96, 96), quality=95)

        # 下摆处理  hem
        hem_box = (
            region_f.size[0]-img_hem.size[0]//2,
            region_f.size[1]-img_hem.size[1],
            region_f.size[0], region_f.size[1]
        )
        hem_img = region_f.crop(hem_box)
        hem_img.save(self.path_save+"\\tmp_eff_hem_r.jpg",
                     dpi=(96, 96), quality=95)

        # 图片裁剪，后件处理 -------------------------------------
        region_box = (
            0,
            0,
            img_backup.size[0],
            region_f.size[1]-hem_img.size[1]
        )
        print(region_box)
        region_f = region_f.crop(region_box)
        region_f.save(self.path_save+"\\tmp_eff_back.jpg",
                      dpi=(96, 96), quality=95)

    # ------------------------------------------------------ #
    #                   合并两边的图片                        #
    #  ----------------------------------------------------- #

    def merge_double(self, Apath, Bpath, Outpath):
        l = Image.open(Apath)
        r = Image.open(Bpath)
        bg = Image.new("RGB", (l.size[0]+r.size[0], l.size[1]))
        bg.paste(l, (0, 0))
        bg.paste(r, (l.size[0], 0))
        bg.save(Outpath, dpi=(96, 96), quality=95)
        os.remove(Apath)
        os.remove(Bpath)

    def merge_double_all(self):
        # 下摆处理
        self.merge_double(self.path_save+"\\tmp_eff_hem_l.jpg",
                          self.path_save+"\\tmp_eff_hem_r.jpg",
                          self.path_save+"\\tmp_eff_hem.jpg")
        # 袖子处理
        self.merge_double(self.path_save+"\\tmp_eff_sleeve_r_0.jpg",
                          self.path_save+"\\tmp_eff_sleeve_l_0.jpg",
                          self.path_save+"\\tmp_eff_sleeve_l.jpg")
        # 袖子处理2
        self.merge_double(self.path_save+"\\tmp_eff_sleeve_r_1.jpg",
                          self.path_save+"\\tmp_eff_sleeve_l_1.jpg",
                          self.path_save+"\\tmp_eff_sleeve_r.jpg")
        # 袖口处理
        self.merge_double(self.path_save+"\\tmp_eff_cuff_r_0.jpg",
                          self.path_save+"\\tmp_eff_cuff_l_0.jpg",
                          self.path_save+"\\tmp_eff_cuff_l.jpg")
        # 袖口处理2
        self.merge_double(self.path_save+"\\tmp_eff_cuff_r_1.jpg",
                          self.path_save+"\\tmp_eff_cuff_l_1.jpg",
                          self.path_save+"\\tmp_eff_cuff_r.jpg")
