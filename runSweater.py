import src.Sweater.ChangeName as ChangeName
import src.Sweater.Slice_process as Slice_process
import src.Sweater.FoldDiagram as FoldDiagram
import src.Sweater.Composing as Composing
import src.Sweater.FlodDiagramIMG as FlodDiagramIMG
import src.Sweater.createBig as createBig

import src.ChangeStyle as ChangeStyle
import src.Render as Render

import os
import threading


class runSweater():
    # size ---> 尺码
    # Render_pic ---> 渲染图，注意只需要输入文件名
    # move ----> 渲染图进行渲染时的位移，注意移动过大会出现黑边
    def __init__(self, size, Render_pic):
        self.size = size
        self.Render_pic = "pic\\"+Render_pic
        super().__init__()

    def preFlodDiagram(self):
        FlodDiagramIMG.FlodDiagramIMG(
            "save\\Sweater\\front.png", self.Render_pic, "save\\Sweater\\out\\").FlodDiagram()

    def aftFlodDiagram(self, move):
        style = "Sweater"  # 衣服种类
        # size = self.size
        # 3.20修改，目标文件 --- 以默认较小的尺码为处理标准
        # 原来做法是帽子不同的尺码略有不同，现在只以第一个为处理标准，可以加速处理效果
        # 3.21发现bug:必须要先处理一次切片的缓存，不然没办法渲染褶皱图的帽子
        posfile = "save\\"+style+"\\"+self.size[0]
        Render_pic = self.Render_pic

        if(not os.path.exists(posfile+"\\flag")):
            ChangeStyle.ChangeStyle(posfile+"\\ori").tif_to_png_changeAll()
            ChangeName.ChangeName(posfile+"\\ori", posfile +
                                  "\\opt").ChangeNameAndMove()
            os.mkdir(posfile+"\\flag")
        else:
            print("跳过复制执行")

        hat_move_path = "tmp\\hat.txt"
        hat_move = (int(0), int(0))
        try:
            f = open(hat_move_path, mode="r")
            content = f.read()
            f.close()
            hat_move = content.split(' ')
            hat_move[0] = int(hat_move[0])
            hat_move[1] = int(hat_move[1])
        except:
            print("文件丢失，采取默认参数0")
        print(hat_move)

        a = Slice_process.Slice_process(
            posfile+"\\tmp",
            posfile+"\\opt\\forward.png",
            posfile+"\\opt\\back.png",
            posfile+"\\opt\\hem.png",
            posfile+"\\opt\\cuff.png",
            posfile+"\\opt\\cuff1.png",
            posfile+"\\opt\\front_bag_cloth.png",
            posfile+"\\opt\\hat_cloth.png",
            posfile+"\\opt\\hat_cloth1.png",
            posfile+"\\opt\\sleeve.png",
            posfile+"\\opt\\sleeve1.png",
            Render_pic,  # 目标图片
            posfile+"\\topt",
            hat_move,
            [(0, 0), (0, 0)]
        )
        a.setflag(move[0], move[1])
        a.Single_processing_new_Tshirt_forward()
        a.Single_processing_new_Tshirt_back()
        a.merge_double_all()

        # 渲染褶皱图
        a = FoldDiagram.FoldRender("save\\Sweater\\front.png", "save\\Sweater\\front_hat.png",
                                   "save\\Sweater\\back.png", "save\\Sweater\\back_hat.png",
                                   "save\\Sweater\\tie.png",
                                   posfile+"\\tmp\\tmp_eff_hat_cloth_l.jpg", posfile+"\\tmp\\tmp_eff_hat_cloth_r.jpg",
                                   "save\\Sweater\\out\\",
                                   "save\\Sweater\\out\\\\bigImage.jpg", move[0], move[1])
        a.front_fusion()
        a.back_fusion()

    # 运行完成这个方法才弹窗
    # createBig 创建大图用
    def Preprocessing(self):
        style = "Sweater"  # 衣服种类
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

            a = Slice_process.Slice_process(
                posfile+"\\tmp",
                posfile+"\\opt\\forward.png",
                posfile+"\\opt\\back.png",
                posfile+"\\opt\\hem.png",
                posfile+"\\opt\\cuff.png",
                posfile+"\\opt\\cuff1.png",
                posfile+"\\opt\\front_bag_cloth.png",
                posfile+"\\opt\\hat_cloth.png",
                posfile+"\\opt\\hat_cloth1.png",
                posfile+"\\opt\\sleeve.png",
                posfile+"\\opt\\sleeve1.png",
                Render_pic,  # 目标图片
                posfile+"\\topt",
                (0, 0),
                [(0, 0), (0, 0)]
            )
            a.setflag(0, 0)
            a.Single_processing_new_Tshirt_forward()
            a.Single_processing_new_Tshirt_back()
            a.merge_double_all()

            createBig.createBig(posfile+"\\bigtmp", Render_pic,
                                posfile+"\\opt\\back.png", posfile+"\\opt\\hem.png",
                                posfile+"\\opt\\sleeve.png", posfile+"\\opt\\cuff.png").createBigPIC()

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
        style = "Sweater"  # 衣服种类
        # size = self.size
        # 目标文件
        posfile = "save\\"+style+"\\"+size
        Render_pic = self.Render_pic

        hat_move_path = "tmp\\hat.txt"
        hat_move = (int(0), int(0))
        try:
            f = open(hat_move_path, mode="r")
            content = f.read()
            f.close()
            hat_move = content.split(' ')
            hat_move[0] = int(hat_move[0])
            hat_move[1] = int(hat_move[1])
        except:
            print("文件丢失，采取默认参数0")
        print(hat_move)

        a = Slice_process.Slice_process(
            posfile+"\\tmp",
            posfile+"\\opt\\forward.png",
            posfile+"\\opt\\back.png",
            posfile+"\\opt\\hem.png",
            posfile+"\\opt\\cuff.png",
            posfile+"\\opt\\cuff1.png",
            posfile+"\\opt\\front_bag_cloth.png",
            posfile+"\\opt\\hat_cloth.png",
            posfile+"\\opt\\hat_cloth1.png",
            posfile+"\\opt\\sleeve.png",
            posfile+"\\opt\\sleeve1.png",
            Render_pic,  # 目标图片
            posfile+"\\topt",
            hat_move,
            movesleeve,
        )
        a.setflag(move[0], move[1])
        a.Single_processing_new_Tshirt_forward()
        a.Single_processing_new_Tshirt_back()
        a.merge_double_all()

        print("多线程处理完毕")
        RendPIC = [posfile+"\\topt\\back.png",
                   posfile+"\\topt\\forward.png",
                   posfile+"\\topt\\cuff_l.png",
                   posfile+"\\topt\\cuff_r.png",
                   posfile+"\\topt\\front_bag_cloth.png",
                   posfile+"\\topt\\hat_cloth_r.png",
                   posfile+"\\topt\\hat_cloth_l.png",
                   posfile+"\\topt\\hem.png",
                   posfile+"\\topt\\sleeve_l.png",
                   posfile+"\\topt\\sleeve_r.png"]

        NeedPIC = [posfile+"\\tmp\\tmp_eff_back.jpg",
                   posfile+"\\tmp\\tmp_eff_forward.jpg",
                   posfile+"\\tmp\\tmp_eff_cuff_l.jpg",
                   posfile+"\\tmp\\tmp_eff_cuff_r.jpg",
                   posfile+"\\tmp\\tmp_eff_front_bag_cloth.jpg",
                   posfile+"\\tmp\\tmp_eff_hat_cloth_l.jpg",
                   posfile+"\\tmp\\tmp_eff_hat_cloth_r.jpg",
                   posfile+"\\tmp\\tmp_eff_hem.jpg",
                   posfile+"\\tmp\\tmp_eff_sleeve_l.jpg",
                   posfile+"\\tmp\\tmp_eff_sleeve_r.jpg"]

        OutPIC = [posfile+"\\eff\\back.png",
                  posfile+"\\eff\\forward.png",
                  posfile+"\\eff\\cuff_l.png",
                  posfile+"\\eff\\cuff_r.png",
                  posfile+"\\eff\\front_bag_cloth.png",
                  posfile+"\\eff\\hat_cloth_l.png",
                  posfile+"\\eff\\hat_cloth_r.png",
                  posfile+"\\eff\\hem.png",
                  posfile+"\\eff\\sleeve_l.png",
                  posfile+"\\eff\\sleeve_r.png"]

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
        style = "Sweater"  # 衣服种类
        # size = self.size
        posfile = "save\\"+style+"\\"+size

        print("开始处理固定排版")
        a = Composing.Composing(
            posfile+"\\eff",
            posfile+"\\eff\\forward.png",
            posfile+"\\eff\\back.png",
            posfile+"\\eff\\hem.png",
            posfile+"\\eff\\cuff_l.png",
            posfile+"\\eff\\cuff_r.png",
            posfile+"\\eff\\front_bag_cloth.png",
            posfile+"\\eff\\hat_cloth_r.png",
            posfile+"\\eff\\hat_cloth_l.png",
            posfile+"\\eff\\sleeve_l.png",
            posfile+"\\eff\\sleeve_r.png"
        )
        a.Composing()
        print("排版处理完毕")
        print("卫衣处理完毕")


if __name__ == '__main__':
    # 传入参考 - 尺码， 渲染图
    # 多尺码，渲染图名称
    sizeList = ["3XL"]
    move = (0, 0)
    movesleeve = [(0, 0), (2000, 0)]
    a = runSweater(sizeList, "8.jpg")
    a.preFlodDiagram()
    a.aftFlodDiagram(move)
    a.Preprocessing()  # 预处理，去tmp//里面找bigImage

    # 第一个参数,不变，原切片的移动距离
    # 第二个参数，为袖子的移动距离,先左后右
    a.starts(move, movesleeve)  # 预处理之后，往里面发(向下移动距离，向右移动距离)
    a.slices()  # 切片排版处理，老样子
    del a
