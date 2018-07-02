#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: LH

import os
import sys
import fnmatch

from PIL import Image


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

from utils.config import MyConf
from utils.log_ctrl import lh_log
from utils.dataexport import Export


config_path = os.path.join(BASE_DIR, 'conf', 'config.ini')
image_base_dir_path = os.path.join(BASE_DIR, 'db')

class ImageUtils:
    """图像处理类"""
    def __init__(self):
        """
        初始化函数: 每次启动初始化，config的default的base路径，避免移动路径报错。
        @source_dir: 图片的原始文件夹目录，从config中获取
        @target_dir: 处理后的图片与目录存放的位置，从config中获取
        """
        self.config = MyConf(config_path)
        self.config.set_default(image_base_dir_path)  # 初始化的时候，重新写入数据的基础目录，以便于移动目录的时候，自动切换数据库来源
        self.source_dir = self.config.read_val('image', 'source_dir')
        self.target_dir = self.config.read_val('image', 'target_dir')
        self.log = lh_log('image')
    
    def set_dir_config(self, source_dir='${base_dir}/source', target_dir='$(base_dir)/target'):
        # self.config.add()
        # self.config[]
        pass
        

    def get_image_info(self):
        """获取图片的大小与名字"""
        try:
            image_info = []
            print(self.source_dir)
            for file_name in os.listdir(self.source_dir):
                image_path = os.path.join(self.source_dir, file_name)
                if os.path.isfile(image_path):
                    if fnmatch.fnmatch(file_name, '*.png') or  fnmatch.fnmatch(file_name, '*.jpg')\
                     or  fnmatch.fnmatch(file_name,'*.bmp') or fnmatch.fnmatch(file_name, '*.jpeg'):
                        im = Image.open(image_path)
                        file_name = os.path.basename(im.filename)
                        h, w = im.size
                        size = str(h) + '*' + str(w)
                        image_info.append((file_name, size))
            
            self.log.info('图片信息获取成功')
            return image_info
        except Exception as e:
            self.log.waring('图片信息获取失败', e)
            return None

    def export_image_info(self):
        image_info = self.get_image_info()
        if image_info:
            ex = Export(image_info)
            ex.export_excle('image_info.xlsx')
            self.log.info('图片信息导出成功，在db文件下')

    def rotate(self, file_name, point, transpose=False):
        '''旋转图片，并支持镜像
        @file_name: 图片名字
        @point:图片旋转角度
        @transpose:为True时支持水平镜像
        '''
        if file_name in os.listdir(self.source_dir):
            
            im = Image.open(os.path.join(self.source_dir, file_name))
            im_new = im.rotate(45)
            if transpose:
                im_new = im_new.transpose(Image.FLIP_LEFT_RIGHT)
            im_new.show()
            n1, n2 = file_name.split('.')
            im_new.save(os.path.join(self.target_dir, n1+'-rotate'+'.'+n2))
        else:
            print('源路径中不存在该文件')

    def cut(self, file_name, w1, h1 , w2, h2):
        """"裁剪图片并保存
        @file_name: str 文件名
        @w1,h1,w2,h2: 两个点坐标
        """
        if file_name in os.listdir(self.source_dir):
            im = Image.open(os.path.join(self.source_dir, file_name))
            box =  w1, h1, w2, h2
            im_new = im.crop(box)
            im_new.show()
            n1, n2 = file_name.split('.')
            im_new.save(os.path.join(self.target_dir, n1+'-crop'+'.'+n2))
        else:
            print('源路径中不存在该文件')

    def thumbnail(self, file_name, percent = 0.5):
        '''做一个缩略图，当前路径'''
        try:
            if file_name in os.listdir(self.source_dir):        
                im = Image.open(os.path.join(self.source_dir, file_name))
                im_new = im.copy()
                # 获取尺寸
                w, h = im.size            
                # 默认缩放到50%
                im_new.thumbnail((int(w*percent), int(h*percent)))
                n1, n2 = file_name.split('.')
                im_new.save(os.path.join(self.target_dir, n1+'-thumb'+'.'+n2))
            else:
                print('该文件不存在')
        except Exception as e:
            self.log.waring('缩略失败', e)

    def thumbnail_all(self, percent=0.5):
        '''循环source_dir下所有的图片文件，生成缩略图'''
        for file in os.listdir(self.source_dir):
            if fnmatch.fnmatch(file, '*.png') or  fnmatch.fnmatch(file, '*.jpg')\
             or  fnmatch.fnmatch(file,'*.bmp') or fnmatch.fnmatch(file, '*.jpeg'):                
                self.thumbnail(file, percent)

    def resize(self, w, h):
        
        for file in os.listdir()

    def resize_all(self)
        
def main():
    pic = ImageUtils()
    # print(pic.source_dir)
    # pic.export_image_info()
    # pic.rotate('1.jpg', 45, True)
    # pic.cut('1.jpg', 200,200,600,600)
    # pic.thumbnail('1.jpg', 0.5)
    pic.thumbnail_all()
if __name__ == '__main__':
    main()
