from wand.image import Image


class ColorSpace():
    def __init__(self, path):
        self.path = path
        super().__init__()

    def changeColorSpace(self):
        with Image(filename=str(self.path)) as img:
            img.transform_colorspace('cmyk')
            img.save(filename=self.path)


# API说明：输入一个地址，在同地址进行覆盖，生成cmyk色彩空间的图片
# 导入 粟.tif 将会在同路径将 粟.tif 的色彩空间转换成CMYK
# 支持中文处理
# 注：PNG,JPG不支持CMYK色彩空间

#ColorSpace("save\\Sweater\\3XL\\eff\\AAA_后件_3XL.tif").changeColorSpace()