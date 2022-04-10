from PIL import Image


class FlodDiagramIMG:
    def __init__(self, FlodDiagramPATH, posPath, path_save):
        self.FlodDiagramPATH = FlodDiagramPATH
        self.posPath = posPath
        self.path_save = path_save
        super().__init__()

    def FlodDiagram(self):
        flodDiagram = Image.open(self.FlodDiagramPATH)
        bg_forward = Image.open(self.posPath)
        l = flodDiagram.size[0] / bg_forward.size[0]
        h = (flodDiagram.size[1]-95) / bg_forward.size[1]
        ratio = 0
        if l < h:
            ratio = h
        else:
            ratio = l
        bg_forward = bg_forward.resize(
            (int(bg_forward.size[0]*ratio), int(bg_forward.size[1]*ratio)), Image.ANTIALIAS)
        bg_forward.save(self.path_save+"\\bigImage.jpg",
                        dpi=(96, 96), quality=95)
