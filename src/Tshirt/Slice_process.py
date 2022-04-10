from PIL import Image
import os
import math

# T-shirt


class Slice_process():
    def __init__(self, path_save, path_forward, path_neckline, path_backup,
                 path_sleeve_l, path_sleeve_r, posPath, TMPSAVEPATH,
                 Sleeve_pos):
        self.path_save = path_save
        self.posPath = posPath
        self.TMPSAVEPATH = TMPSAVEPATH
        # Open file
        self.img_forward = Image.open(path_forward)
        self.img_neckline = Image.open(path_neckline)
        self.img_backup = Image.open(path_backup)
        self.img_sleeve_l = Image.open(path_sleeve_l)
        self.img_sleeve_r = Image.open(path_sleeve_r)
        # from 'LA' convert to 'RGBA'
        self.img_forward = self.img_forward.convert("RGBA")
        self.img_neckline = self.img_neckline.convert("RGBA")
        self.img_backup = self.img_backup.convert("RGBA")
        self.img_sleeve_l = self.img_sleeve_l.convert("RGBA")
        self.img_sleeve_r = self.img_sleeve_r.convert("RGBA")
        # 默认参数
        self.Zoom_ratio = 2.3                   # 缩放倍率--- 整体图片在渲染的时候的缩放率，推荐2.2
        # 移动参数
        # self.pasteDown = 0  # 图案粘贴沉浮
        # self.pasteRight = 0  # 图案粘贴左右移动
        # 袖子的相对位置
        self.lSleeve_pos = Sleeve_pos[0]
        self.rSleeve_pos = Sleeve_pos[1]

    def setflag(self, pasteDown, pasteRight):
        # 注明：卫衣的褶皱图和切片图有 上下3.1倍的比例差，左右有2.7倍的比例差
        self.pasteDown = int(pasteDown * 3.1)
        self.pasteRight = int(pasteRight * 2.7)
        print(" ------------------- 相对位移为：", self.pasteRight, self.pasteDown)
        # 把默认处理设置为0，不处理
        self.Boundary_data = 0
        self.Boundary_data_top = 0
        self.Elongation_factor = 1.0
        # 缩放倍率--- 整体图片在渲染的时候的缩放率，推荐2.2
        bg_forward = Image.open(self.posPath)
        l = self.img_backup.size[1] / bg_forward.size[0]
        h = self.img_backup.size[0] / bg_forward.size[1]
        print(l, h)
        if l < h:
            self.Zoom_ratio = h
        else:
            self.Zoom_ratio = l

    # 处理背景图片使之可以较为方便的对 前件 and 后件 进行渲染
    # Mag(Magnification):倍率，整体图片缩放倍率
    # ------------------------------------------------------ #
    #                       前件拉伸处理                      #
    #  ----------------------------------------------------- #

    def Single_processing_new_Tshirt_forward(self):
        # -- 参数设置区域 -- #
        # 缩放倍率
        Zoom_ratio = self.Zoom_ratio
        # 前后旋转角度
        img_forward = self.img_forward.transpose(Image.ROTATE_270)
        img_forward.save(self.TMPSAVEPATH+"\\img_forward.png", dpi=(96, 96))
        region_f = Image.new(
            "RGB", img_forward.size)
        print("前件图案拉伸处理，mode:", region_f.mode, "\nszie:", region_f.size)

        # 整体缩放
        bg_forward = Image.open(self.posPath)

        bg_forward = bg_forward.resize(
            (int(bg_forward.size[0] * Zoom_ratio), int(bg_forward.size[1] * Zoom_ratio)), Image.ANTIALIAS)
        bg_forward.save(self.path_save+"\\bigImage.jpg")

        # 防止黑边，x左右，y上下
        # 3.20补，这里的约束条件不要乱动了，很容易出问题
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

        region_f.save(self.path_save+"\\tmp_eff_forward.jpg",
                      dpi=(96, 96), quality=95)

    # ------------------------------------------------------ #
    #                       后件拉伸处理                      #
    #  ----------------------------------------------------- #
    def Single_processing_new_Tshirt_back(self):
        # -- 参数设置区域 -- #
        # 缩放倍率
        Zoom_ratio = self.Zoom_ratio
        # 前后旋转角度
        img_backup = self.img_backup.transpose(Image.ROTATE_270)
        img_backup.save(self.TMPSAVEPATH+"\\img_backup.png", Ｆdpi=(96, 96))

        region_f = Image.new(
            "RGB", img_backup.size)
        print("后件图案拉伸处理，mode:", region_f.mode, "\nszie:", region_f.size)

        # 整体缩放
        bg_forward = Image.open(self.posPath)
        bg_forward = bg_forward.resize(
            (int(bg_forward.size[0] * Zoom_ratio), int(bg_forward.size[1] * Zoom_ratio)), Image.ANTIALIAS)

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
        # print("=========================",startl,endl,"=========================")
        bg_box = (startl,
                  start,
                  endl,
                  end)
        region_f = bg_forward.crop(bg_box)

        region_f.save(self.path_save+"\\tmp_eff_back.jpg",
                      dpi=(96, 96), quality=95)

    # ------------------------------------------------------------------ #
    #                       [新版]两个袖子拉伸处理，简化                    #
    #  ----------------------------------------------------------------- #

    def new_Single_processing_new_Tshirt_sleeve(self):
        img_sleeve_l = self.img_sleeve_l
        img_sleeve_r = self.img_sleeve_r

        img_sleeve_l_tmp = img_sleeve_l.transpose(Image.ROTATE_270)
        img_sleeve_r_tmp = img_sleeve_r.transpose(Image.ROTATE_270)

        img_sleeve_l_tmp.save(self.TMPSAVEPATH+"\\img_sleeve_l.png",
                          dpi=(96, 96))
        img_sleeve_r_tmp.save(self.TMPSAVEPATH+"\\img_sleeve_r.png",
                          dpi=(96, 96))

        img_sleeve_l = img_sleeve_l.transpose(Image.ROTATE_270)
        img_sleeve_r = img_sleeve_r.transpose(Image.ROTATE_270)

        img_sleeve_r = Image.new(
            "RGB", img_sleeve_r.size)
        img_sleeve_l = Image.new(
            "RGB", img_sleeve_l.size)

        print("袖子图案处理，mode:", img_sleeve_l.mode, "\nszie:", img_sleeve_l.size)
        # 参与处理大图
        img_eff = Image.open(self.path_save+"\\bigImage.jpg")
        #-----------------------------------------#
        lSleeve_pos = self.lSleeve_pos
        rSleeve_pos = self.rSleeve_pos

        # 防止lSleeve_pos超界处理
        if lSleeve_pos[0] < 0:
            lSleeve_pos = (0, lSleeve_pos[1])
        if lSleeve_pos[1] < 0:
            lSleeve_pos = (lSleeve_pos[0], 0)
        if lSleeve_pos[0] > img_eff.size[0]-img_sleeve_l.size[0]//2:
            lSleeve_pos[0] = (
                img_eff.size[0]-img_sleeve_l.size[0]//2, lSleeve_pos[1])
        if lSleeve_pos[1] > img_eff.size[1]-img_sleeve_l.size[1]:
            lSleeve_pos[0] = (
                lSleeve_pos[0], img_eff.size[1]-img_sleeve_l.size[1])

        # 防止rSleeve_pos超界处理
        if rSleeve_pos[0] < 0:
            rSleeve_pos = (0, rSleeve_pos[1])
        if rSleeve_pos[1] < 0:
            rSleeve_pos = (rSleeve_pos[0], 0)
        if rSleeve_pos[0] > img_eff.size[0]-img_sleeve_l.size[0]//2:
            rSleeve_pos = (
                img_eff.size[0]-img_sleeve_l.size[0]//2, rSleeve_pos[1])
        if rSleeve_pos[1] > img_eff.size[1]-img_sleeve_l.size[1]:
            rSleeve_pos = (
                rSleeve_pos[0], img_eff.size[1]-img_sleeve_l.size[1])

        l_box = (lSleeve_pos[0], lSleeve_pos[1],
                 lSleeve_pos[0] + img_sleeve_l.size[0]//2,
                 lSleeve_pos[1] + img_sleeve_l.size[1])
        '''
        l_box = (0, img_eff.size[1]//2-img_sleeve_l.size[1],
                 img_sleeve_l.size[0]//2, img_eff.size[1]//2)
        '''
        l_img = img_eff.crop(l_box)

        r_box = (rSleeve_pos[0], rSleeve_pos[1],
                 rSleeve_pos[0] + img_sleeve_l.size[0]//2,
                 rSleeve_pos[1] + img_sleeve_l.size[1])
        '''
        r_box = (img_eff.size[0]-img_sleeve_l.size[0]//2, img_eff.size[1] //
                 2-img_sleeve_l.size[1], img_eff.size[0], img_eff.size[1]//2)
        '''
        r_img = img_eff.crop(r_box)

        img_sleeve_l.paste(r_img, (0, 0))
        img_sleeve_l.paste(l_img, (r_img.size[0], 0))

        img_sleeve_l = img_sleeve_l.transpose(Image.ROTATE_90)
        img_sleeve_r = img_sleeve_l

        img_sleeve_l = img_sleeve_l.transpose(Image.ROTATE_270)
        img_sleeve_r = img_sleeve_r.transpose(Image.ROTATE_270)

        img_sleeve_l.save(self.path_save+"\\tmp_sleeve_r.jpg",
                          dpi=(96, 96), quality=95)
        img_sleeve_r.save(self.path_save+"\\tmp_sleeve_l.jpg",
                          dpi=(96, 96), quality=95)

    # ------------------------------------------------------ #
    #                       [旧版]两个袖子拉伸处理             #
    #  ----------------------------------------------------- #

    def Single_processing_new_Tshirt_sleeve(self, rectangle_heigh, rectangle_weigh, isORI):
        Rotation_angle = 360-45

        img_sleeve_l = self.img_sleeve_l
        img_sleeve_r = self.img_sleeve_r

        img_sleeve_l.save(self.TMPSAVEPATH+"\\img_sleeve_l.png",
                          dpi=(96, 96))
        img_sleeve_r.save(self.TMPSAVEPATH+"\\img_sleeve_r.png",
                          dpi=(96, 96))
        # img_forward = self.img_forward.transpose(Image.ROTATE_270)
        img_sleeve_r = Image.new(
            "RGB", img_sleeve_r.size)
        img_sleeve_l = Image.new(
            "RGB", img_sleeve_l.size)

        print("袖子图案处理，mode:", img_sleeve_l.mode, "\nszie:", img_sleeve_l.size)
        img_eff = Image.open(self.path_save+"\\tmp_eff_forward.jpg")

        if isORI == 0:
            # 原图拉伸
            l_box = (img_eff.size[0]-rectangle_weigh,
                     0,
                     img_eff.size[0],
                     rectangle_heigh)
            l_img = img_eff.crop(l_box)
            r_box = (0, 0, rectangle_weigh, rectangle_heigh)
            r_img = img_eff.crop(r_box)
        else:
            # 旋转处理
            # Offset = int(math.sqrt((img_sleeve_r.size[1]//2)**2 //2))
            # 先取出两倍的空间
            length = img_sleeve_l.size[1]//2
            print(length, img_sleeve_l.size)
            l_box = (img_eff.size[0]-2*length, 0, img_eff.size[0], 2*length)
            l_img = img_eff.crop(l_box)
            l_img = l_img.rotate(Rotation_angle)
            new_box = (int(l_img.size[0]//4), int(l_img.size[1]//4),
                       int(l_img.size[0]//4*3), int(l_img.size[1]//4*3))
            l_img = l_img.crop(new_box)

            r_box = (0, 0, 2*length, 2*length)
            r_img = img_eff.crop(r_box)
            r_img = l_img.rotate(Rotation_angle)
            new_box = (int(r_img.size[0]//4), int(r_img.size[1]//4),
                       int(r_img.size[0]//4*3), int(r_img.size[1]//4*3))
            r_img = r_img.crop(new_box)

        l_img = l_img.resize(
            (int(img_sleeve_l.size[0]), int(img_sleeve_l.size[1]//2)), Image.ANTIALIAS)

        r_img = r_img.resize(
            (int(img_sleeve_l.size[0]), int(img_sleeve_l.size[1]//2)), Image.ANTIALIAS)

        # left paste
        img_sleeve_l.paste(r_img, (0, 0))
        img_sleeve_l.paste(l_img, (0, img_sleeve_l.size[1]//2))
        # right paste
        # img_sleeve_r.paste(l_img,(0,0))
        # img_sleeve_r.paste(r_img,(0,img_sleeve_r.size[1]//2))
        # img_sleeve_r = img_sleeve_l.transpose(Image.FLIP_LEFT_RIGHT)
        # img_sleeve_r = img_sleeve_l.transpose(Image.FLIP_TOP_BOTTOM)
        img_sleeve_r = img_sleeve_l

        img_sleeve_l.save(self.path_save+"\\tmp_sleeve_r.jpg",
                          dpi=(96, 96), quality=95)
        img_sleeve_r.save(self.path_save+"\\tmp_sleeve_l.jpg",
                          dpi=(96, 96), quality=95)

    # ------------------------------------------------------ #
    #                       领口拉伸处理                      #
    #  ----------------------------------------------------- #
    def Single_processing_new_Tshirt_neckline(self):
        img_neckline = self.img_neckline.transpose(Image.ROTATE_90)
        img_neckline.save(self.TMPSAVEPATH+"\\img_neckline.png",
                          dpi=(96, 96))

        img_eff = Image.open(self.path_save+"\\tmp_eff_forward.jpg")

        t_box = (int(img_eff.size[0]//2-img_neckline.size[0]//2),
                 0, int(img_eff.size[0]//2+img_neckline.size[0]//2), img_neckline.size[1])
        t_img = img_eff.crop(t_box)
        print("领口图案处理，", t_img.mode, "\nszie:", t_img.size)
        t_img.save(self.path_save+"\\tmp_neckline.jpg",
                   dpi=(96, 96), quality=95)
