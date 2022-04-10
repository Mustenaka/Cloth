from PIL import Image

# 不放入正式代码中，用于处理出一个合适的用于当前景的褶皱图

save = "save\\Sweater\\front_X.png"
pic = "save\\Sweater\\front.png"

img = Image.open(pic)

box = (0,95,img.size[0],img.size[1])
img = img.crop(box)

img.save(save,quality=100)