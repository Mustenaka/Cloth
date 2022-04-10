import os

#快速创建文件夹用
dirs = ["L","M","S","XL","XXL","3XL","4XL","5XL","6XL","7XL"]
posPath = "save\\Sweater\\"
Subdirectory = ["eff","opt","ori","pic","tmp","topt"]

for i in dirs:
    if(not os.path.exists(posPath+i)):
        os.mkdir(posPath+i)
        for j in Subdirectory:
            os.mkdir(posPath+i+"\\"+j)