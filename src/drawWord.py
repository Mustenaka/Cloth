from PIL import Image, ImageDraw, ImageFont


class drawWord():
    # ImagePath图片路径，text图片附加文字，其余API已屏蔽，就这两个要用
    def __init__(self, ImagePath, text, tra=0):
        fname1 = ImagePath
        im = Image.open(fname1)
        # 旋转角度修改
        if tra == 90:
            im = im.transpose(Image.ROTATE_90)
        elif tra == 180:
            im = im.transpose(Image.ROTATE_180)
        elif tra == 270:
            im = im.transpose(Image.ROTATE_270)
        pointsize = 14
        text = text

        # x,y 正位居中调整（自适应）
        x = im.size[0]//2-(int(len(text)*pointsize)//2)
        y = im.size[1]-pointsize

        fillcolor = (0, 0, 0)
        shadowcolor = "white"

        font = "font\\Deng.ttf"
        draw = ImageDraw.Draw(im)
        font = ImageFont.truetype(font, pointsize)

        # 调用函数
        self.text_border(draw, x, y, font, shadowcolor, fillcolor, text)
        if tra == 90:
            im = im.transpose(Image.ROTATE_270)
        elif tra == 180:
            im = im.transpose(Image.ROTATE_180)
        elif tra == 270:
            im = im.transpose(Image.ROTATE_90)
        im.save(ImagePath)
        super().__init__()

    # 用于文字边框展示，传入draw,坐标x,y，字体，边框颜色和填充颜色
    def text_border(self, draw, x, y, font, shadowcolor, fillcolor, text):
        # thin border
        draw.text((x - 1, y), text, font=font, fill=shadowcolor)
        draw.text((x + 1, y), text, font=font, fill=shadowcolor)
        draw.text((x, y - 1), text, font=font, fill=shadowcolor)
        draw.text((x, y + 1), text, font=font, fill=shadowcolor)

        # thicker border
        draw.text((x - 1, y - 1), text, font=font, fill=shadowcolor)
        draw.text((x + 1, y - 1), text, font=font, fill=shadowcolor)
        draw.text((x - 1, y + 1), text, font=font, fill=shadowcolor)
        draw.text((x + 1, y + 1), text, font=font, fill=shadowcolor)

        # now draw the text over it
        draw.text((x, y), text, font=font, fill=fillcolor)


# ImagePath图片路径(会进行覆盖处理)，text图片附加文字
if __name__ == '__main__':
    try:
        drawWord("back.png", "CCC_后片_3XL")
    except Exception as e:
        f = open("log.txt", "w")
        f.write(e)
        f.close()

# text传入规则
# 类型:string
# 编码_类型_尺码
