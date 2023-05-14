import os
dirname = ['word/', 'sentence/', 'trans_expression/', 'dymn_expression/', 'irrelevant/']
for dir in dirname:
    for filename in os.listdir(dir):   #‘logo/’是文件夹路径，你也可以替换其他
        newname = filename.replace('幻灯片','')
        os.rename(dir+filename, dir+newname)  
