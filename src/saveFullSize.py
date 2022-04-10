from PIL import Image

import os


class saveFullSzie:
    def __init__(self, path, savePath, mode):
        self.save(path, savePath, mode)

        super().__init__()

    def save(self, path, savePath, mode):
        try:
            fileName = "tmp\\prelist\\FoldDiagramSize\\fullSize"+mode+".txt"
            f = open(file=fileName)
            contect = f.read()
            x, y = map(int, contect.split(' '))
        except:
            print("读取文件异常，请检查文件是否存在或者尺寸是否输入正确")
            print("文件位置位于 'tmp\\prelist\\FoldDiagramSize\\' 中")
        
        saveFile = Image.new("RGB", (x, y), color=(255, 255, 255))
        img = Image.open(path)
        saveFile.paste(img, (saveFile.size[0]//2 - img.size[0]//2,
                             saveFile.size[1]//2 - img.size[1]//2))
        saveFile.save(savePath)


#saveFullSzie("褶皱.jpg", "褶皱图.jpg", "Sweater")
#API接口说明：
#输入图片（输入褶皱图），输出图片（输出褶皱图），褶皱图类型（短袖Tshirt和卫衣Sweater）
