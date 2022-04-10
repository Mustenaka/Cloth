from PIL import Image, ImageCms

import src.DrawBlackborder as DrawBlackborder
import os


class newColorSpace():
    def __init__(self, PILImagePath, outPath):
        self.PILImagePath = PILImagePath
        self.outPath = outPath
        super().__init__()

    def get_imlist_png(self, path):
        return [os.path.join(path, f) for f in os.listdir(path) if f.endswith(".png")]

    def usingICC(self):
        a=DrawBlackborder.Draw()
        a.createbackIMG(self.PILImagePath)
        a.getEdge(self.PILImagePath)
        del a
        img = Image.open(self.PILImagePath)
        tmp = Image.new(('RGBA'), img.size, color=(255, 255, 255, 255))
        img = Image.alpha_composite(tmp, img)
        result = ImageCms.profileToProfile(
            img,
            'ICCMODE\\sRGB Color Space Profile.icm',
            'ICCMODE\\JapanColor2001Coated.icc',
            renderingIntent=0,
            outputMode='CMYK')

        result.save(self.outPath, quality=95, dpi=(96, 96))
        print("RGB转换CMYK成功")


# 导入地址，导出地址
if __name__ == '__main__':
    newColorSpace("save\\Sweater\\3XL\\eff\\Composed.png",
                  "out.tif").usingICC()

# 导出PNG导出tif
# API说明：输入一个地址，在同地址进行覆盖，生成cmyk色彩空间的图片
# 导入 save\\Sweater\\3XL\\eff\\Composed.png 导出 out.tif
# 支持中文处理
