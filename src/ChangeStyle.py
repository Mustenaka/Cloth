from wand.image import Image
import os
#windows下记得安装插件，linux下直接apt-get即可

class ChangeStyle():
    def __init__(self, path):
        self.path = path    #转换的地址

    #获取目录下全部尾缀文件名地址，返回一个list
    def get_imlist_tif(path):
        return [os.path.join(path, f) for f in os.listdir(path) if f.endswith(".tif")]
    def get_imlist_png(path):
        return [os.path.join(path, f) for f in os.listdir(path) if f.endswith(".png")]

    #FTI to PNG ,all files change
    def tif_to_png_changeAll(self):
        listdir = ChangeStyle.get_imlist_tif(self.path)     #调用本体函数

        for dir in listdir:
            print("发现文件：%s" % dir)
            with Image(filename=str(dir)) as img:
                # 存的目录为依旧是当前目录,用了一步replace，换了个目录
                img.save(
                    filename=(str(dir)[:-3]+'png').replace("HBsAg_tif", "HBsAg_png"))
                # png, jpg, bmp, gif, tiff All OK--
        print("转换png成功")

    #TTI to PNG ,One file change
    def tif_to_png_changeOne(self):
        with Image(filename=str(self.path)) as img:
            img.save(
                filename=(str(self.path)[:-3]+'png').replace("HBsAg_tif", "HBsAg_png")
                )
        print("转换png成功")

    #PNG to TIF ,all files change
    def png_to_tif_changeAll(self):
        listdir = ChangeStyle.get_imlist_png(self.path)
        for dir in listdir:
            print("发现文件：%s" % dir)
            with Image(filename=str(dir)) as img:
                # 存的目录为依旧是当前目录,用了一步replace，换了个目录
                img.save(
                    filename=(str(dir)[:-3]+'tif').replace("HBsAg_tif", "HBsAg_png"))
                # png, jpg, bmp, gif, tiff All OK--
        print("转换tif成功")

    #PNG to TIF ,One file change
    def png_to_tif_changeOne(self):
        with Image(filename=str(self.path)) as img:
            img.save(
                filename=(str(self.path)[:-3]+'tif').replace("HBsAg_tif", "HBsAg_png")
                )
        print("转换tif成功")

    def changeResolution(self):
        with Image(filename=str(self.path)) as img:
            print(img.width,img.height)
            print(img.size)
            img.resize(500,600)
            print(img.size)
            #img.resample(x_res=96,y_res=96)
            #img.resize(1000,2000)
            #img.resolution((96,96))
            img.save(filename=str("2.png"))
        with Image(filename=str("2.png")) as img:
            print("-------------")
            print(img.size)

    def dpi96(self):
        with Image(filename=str(self.path)) as img:
            tmp = img.size
            print(img.size)
            img.resample(96,96)
            print(img.size)
            #img.resize(tmp[0],tmp[1])
            print(img.size)
            img.save(
                filename=(str(self.path)[:-3]+'tif').replace("HBsAg_tif", "HBsAg_png")
                )
        print("转换tif成功")

'''
ChangeStyle旨在批量或者单独处理TIF和PNG互相转换
传入一个地址即可，可以是文件地址或者是文件夹地址
其中文件夹地址将会批量转换文件夹下的所有目录
'''