from PIL import Image


class FlodDiagramIMG:
    def __init__(self, FlodDiagramPATH, posPath, path_save):
        self.FlodDiagramPATH = FlodDiagramPATH
        self.posPath = posPath
        self.path_save = path_save
        super().__init__()

    def FlodDiagram(self):
        flodDiagram = Image.open(self.FlodDiagramPATH)
        print("褶皱图：", flodDiagram.size[0], flodDiagram.size[1])
        bg_forward = Image.open(self.posPath)
        print("背景图：", bg_forward.size[0], bg_forward.size[1])
        l = flodDiagram.size[0] / bg_forward.size[0]
        h = flodDiagram.size[1] / bg_forward.size[1]
        print("l and h", l, h)
        ratio = 0
        if l < h:
            ratio = h
        else:
            ratio = l
        bg_forward = bg_forward.resize(
            (int(bg_forward.size[0]*ratio), int(bg_forward.size[1]*ratio)), Image.ANTIALIAS)
        bg_forward.save(self.path_save+"\\bigImage.jpg",
                        dpi=(96, 96), quality=95)
