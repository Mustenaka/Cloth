from PIL import Image

# API说明：
#     传入，图片地址列表（Imglist）,图片参数（Parlist），最大尺寸（maxSize）
#   图片地址列表为一个list，其中内容均为需要进行自由排版的切片地址
#   图片参数为一个list嵌套一个三元组(a,b,c)，其中a,b为放置位置【左上角(0，0)坐标系】，c为旋转角度，仅允许(0,90,180,270)四个参数
#   最大尺寸为一个二元组(x,y)，其表示这个自由排版的最大尺寸为
# 注：在传入时为了避免超框的问题应当最大尺寸设计合理，不宜过大或者过小


class FreeTypography():
    def __init__(self, Imglist, Parlist, maxSize, saveTo):
        self.Imglist = Imglist
        self.Parlist = Parlist
        self.maxSize = maxSize
        self.saveTo = saveTo

    def type(self):
        Imglist = self.Imglist
        Parlist = self.Parlist
        region = Image.new("RGBA", (self.maxSize), (255, 255, 255, 0))
        for i in range(0, len(Imglist)):
            img = Image.open(Imglist[i])
            tmp = Image.new("RGBA", region.size, (255, 255, 255, 0))
            if Parlist[i][2] == 0:
                pass
            elif Parlist[i][2] == 90:
                img = img.transpose(Image.ROTATE_90)
            elif Parlist[i][2] == 180:
                img = img.transpose(Image.ROTATE_180)
            elif Parlist[i][2] == 270:
                img = img.transpose(Image.ROTATE_270)
            tmp.paste(img, (Parlist[i][0], Parlist[i][1]))
            region = Image.alpha_composite(region, tmp)
        region.save(self.saveTo, dpi=(96.0, 96.0), quality=100)


'''
Imagelist = ["save\\Sweater\\3XL\\eff\\cuff_l.png","save\\Sweater\\3XL\\eff\\forward.png"]
Parlist = [(0,0,270),(1100,500,180)]
size = (3500,3500)

FreeTypography(Imagelist,Parlist,size,"save\\Sweater\\3XL\\eff\\save.png").type()
'''
