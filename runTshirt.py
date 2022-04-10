import src.Tshirt.Slice_process as Slice_process
import src.Tshirt.Composing as Composing
import src.Tshirt.FoldDiagram as FoldDiagram
import src.Tshirt.ChangeName as ChangeName
import src.Tshirt.FlodDiagramIMG as FlodDiagramIMG
import src.Tshirt.createBig as createBig

import src.Render as Render
import src.ChangeStyle as ChangeStyle

import os
import threading


class runTshirt():
    # size ---> 尺码
    # Render_pic ---> 渲染图，注意只需要输入文件名
    # move ----> 渲染图进行渲染时的位移，注意移动过大会出现黑边
    def __init__(self, size, Render_pic):
        self.size = size
        self.Render_pic = "pic\\"+Render_pic
        super().__init__()

    def preFlodDiagram(self):
        FlodDiagramIMG.FlodDiagramIMG(
            "save\\Tshirt\\front.png", self.Render_pic, "save\\Tshirt\\out\\").FlodDiagram()

    def aftFlodDiagram(self, move):
        style = "Tshirt"  # 衣服种类
        posfile = "save\\"+style+"\\"+self.size[0]

        if(not os.path.exists(posfile+"\\flag")):
            ChangeStyle.ChangeStyle(posfile+"\\ori").tif_to_png_changeAll()
            ChangeName.ChangeName(posfile+"\\ori", posfile +
                                  "\\opt").ChangeNameAndMove()
            os.mkdir(posfile+"\\flag")
        else:
            print("跳过复制执行")
        # 渲染操作，正片叠底操作褶皱图
        a = FoldDiagram.FoldRender('save\\Tshirt\\front.png', 'save\\Tshirt\\front_neckline.png',
                                   'save\\Tshirt\\back.png', "save\\Tshirt\\out",
                                   "save\\Tshirt\\out\\bigImage.jpg", move[0], move[1])
        a.front_fusion()
        a.back_fusion()

    def Preprocessing(self):
        style = "Tshirt"  # 衣服种类
        sizes = self.size
        # 需要用以渲染出效果的图片：
        Render_pic = self.Render_pic

        for size in sizes:
            # 目标文件
            posfile = "save\\"+style+"\\"+size

            if(not os.path.exists(posfile+"\\flag")):
                ChangeStyle.ChangeStyle(posfile+"\\ori").tif_to_png_changeAll()
                ChangeName.ChangeName(posfile+"\\ori", posfile +
                                      "\\opt").ChangeNameAndMove()
                os.mkdir(posfile+"\\flag")
            else:
                print("跳过复制执行")
            # 进行图片处理-放大缩小，尺寸修改等等
            a = Slice_process.Slice_process(
                posfile+"\\tmp",
                posfile+"\\opt\\forward.png",
                posfile+"\\opt\\neckline.png",
                posfile+"\\opt\\back.png",
                posfile+"\\opt\\sleeve.png",
                posfile+"\\opt\\sleeve1.png",
                Render_pic,  # 目标图片
                posfile+"\\topt",
                [(0, 0), (0, 0)]
            )
            a.setflag(0, 0)
            a.Single_processing_new_Tshirt_forward()
            a.Single_processing_new_Tshirt_back()
            a.new_Single_processing_new_Tshirt_sleeve()
            a.Single_processing_new_Tshirt_neckline()

            createBig.createBig(posfile+"\\bigtmp", Render_pic,
                                posfile+"\\opt\\back.png", posfile+"\\opt\\sleeve.png").createBigPIC()

    def starts(self, move, movesleeve):
        thr = []
        for i in self.size:
            tmp = threading.Thread(self.start(i, move, movesleeve))
            thr.append(tmp)
        for i in thr:
            i.start()

        for i in thr:
            i.join()

    def start(self, size, move, movesleeve):
        style = "Tshirt"  # 衣服种类
        #size = self.size

        # 目标文件
        posfile = "save\\"+style+"\\"+size
        Render_pic = self.Render_pic

        # 进行图片处理-放大缩小，尺寸修改等等
        a = Slice_process.Slice_process(
            posfile+"\\tmp",
            posfile+"\\opt\\forward.png",
            posfile+"\\opt\\neckline.png",
            posfile+"\\opt\\back.png",
            posfile+"\\opt\\sleeve.png",
            posfile+"\\opt\\sleeve1.png",
            Render_pic,  # 目标图片
            posfile+"\\topt",
            movesleeve
        )
        a.setflag(move[0], move[1])
        a.Single_processing_new_Tshirt_forward()
        a.Single_processing_new_Tshirt_back()
        a.new_Single_processing_new_Tshirt_sleeve()
        a.Single_processing_new_Tshirt_neckline()

        RendPIC = [posfile+"\\topt\\img_sleeve_r.png",
                   posfile+"\\topt\\img_sleeve_l.png",
                   posfile+"\\topt\\img_backup.png",
                   posfile+"\\topt\\img_forward.png",
                   posfile+"\\topt\\img_neckline.png",
                   ]

        NeedPIC = [posfile+"\\tmp\\tmp_sleeve_r.jpg",
                   posfile+"\\tmp\\tmp_sleeve_l.jpg",
                   posfile+"\\tmp\\tmp_eff_back.jpg",
                   posfile+"\\tmp\\tmp_eff_forward.jpg",
                   posfile+"\\tmp\\tmp_neckline.jpg",
                   ]

        OutPIC = [posfile+"\\eff\\sleeve.png",
                  posfile+"\\eff\\sleeve1.png",
                  posfile+"\\eff\\back.png",
                  posfile+"\\eff\\forward.png",
                  posfile+"\\eff\\neckline.png"
                  ]

        # 渲染切片图，覆盖操作
        print(len(RendPIC))
        thr = []
        for i in range(0, len(RendPIC)):
            tmp = Render.Render(RendPIC[i], NeedPIC[i], OutPIC[i], i)
            thr.append(tmp)

        for t in thr:
            t.start()

        for t in thr:
            t.join()

    def slices(self):
        thr = []
        for i in self.size:
            tmp = threading.Thread(self.slice(i))
            thr.append(tmp)

        for i in thr:
            i.start()

        for i in thr:
            i.join()

    def slice(self, size):
        style = "Tshirt"  # 衣服种类
        #size = self.size
        # 目标文件
        posfile = "save\\"+style+"\\"+size
        # 汇总排版，生成排版图
        a = Composing.Cut_Tshirt(
            posfile+"\\eff",
            posfile+"\\eff\\forward.png",
            posfile+"\\eff\\neckline.png",
            posfile+"\\eff\\back.png",
            posfile+"\\eff\\sleeve.png",
            posfile+"\\eff\\sleeve1.png"
        )
        a.Composing()
        print("短袖处理完毕")


if __name__ == '__main__':
    sizeList = ["3XL"]
    move = (0, 0)
    movesleeve = [(0, 0), (1500, 0)]

    a = runTshirt(sizeList, "8.jpg")
    a.preFlodDiagram()
    a.aftFlodDiagram(move)
    a.Preprocessing()  # 预处理，去tmp//里面找bigImage

    # 第一个参数,不变，原切片的移动距离
    # 第二个参数，为袖子的移动距离,先左后右
    a.starts(move, movesleeve)
    a.slices()  # 切片排版处理，老样子
    del a
