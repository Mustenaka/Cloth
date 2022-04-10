import os
import shutil

#T-shirt
class ChangeName():
    def __init__(self, path, toPath):
        self.path = path  # 转换的地址
        self.toPath = toPath

    # 获取目录下全部尾缀文件名地址，返回一个list
    def get_imlist(path):
        return [os.path.join(path, f) for f in os.listdir(path) if f.endswith(".png")]

    def ChangeNameAndMove(self):
        dirs = ChangeName.get_imlist(self.path)
        for i in dirs:
            if "前片" in i :
                shutil.copyfile(i,self.toPath+"\\forward.png")
            if "后片" in i :
                shutil.copyfile(i,self.toPath+"\\back.png")
            if "领口" in i :
                shutil.copyfile(i,self.toPath+"\\neckline.png")
            if "袖子" in i or "袖口" in i:
                shutil.copyfile(i,self.toPath+"\\sleeve.png")
            if "袖子1" in i or "袖口1" in i:
                shutil.copyfile(i,self.toPath+"\\sleeve1.png")
        print(dirs)

