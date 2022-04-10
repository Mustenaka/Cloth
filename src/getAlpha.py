import os
from PIL import Image


class getAlpha():
    def __init__(self, path):
        self.path = path
        self.dirs = self.get_imlist(self.path)
        super().__init__()

    def __del__(self):
        pass

    def get_imlist(sself, path):
        return [os.path.join(path, f) for f in os.listdir(path) if f.endswith(".png")]

    def getAlpha(self):
        print(self.dirs)
        for i in self.dirs:
            newIMG = Image.open(i)
            newIMG.convert("RGBA")
            tmp = Image.new("RGBA", (newIMG.size))
            tmp.paste(newIMG, (0, 0))
            tmp.save(i)
            print("save [%s] successful" % i)


a = getAlpha("save\\Tshirt\\3XL\\opt").getAlpha()
