#MyImage

> Author:LH

# 功能介绍
使用标准过程目录，添加了日志，配置文件。
实现了如下的功能：

1. 图片的信息导出到excle中
2. 图片的旋转
3. 图片的裁剪
4. 图片的缩略图
5. 图片的尺寸变换

# 使用帮助
如果先使用自己的文件目录，先要在配置文件中修改，目录的路径  

    -h                              获取帮助;
    -g                              获取文件信心；
    -e                              导出图片信息到excel；
    -r image_name point(旋转角度)  bool(0:不镜像,1:镜像)
    -c image_name w1 h1 w2 h2       裁剪图片
    -t image_name [percent(缩小比例为浮点数，默认为0.5)]   为单一文件生产缩略图
    -t_all  [percent(缩小比例为浮点数，默认为0.5)]              为源目录下所有生产缩略图       
    -size        w   h             重置图片的大小
    -size_all    w   h                   重置目录下所有图片的大小

如下测试命令:  
python main.py -h  
python main.py -e  
python main.py -r 1.jpg 25 0  
python main.py -c 1.jpg  1  1 500 400  
python main.py -t 1.jpg 0.6  
python main.py -t_all  0.6  
python main.py -size 1.jpg  200 200  
python main.py -size_all 200 200  
 
