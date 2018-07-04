# /usr/bin/env python
# -*- coding=utf-8 -*-
# author = LH
# translation-tool.py

import sys
import re


class Temp:
    '温度处理模块'
    @staticmethod
    def tc_to_tf(tc):
        '华式度转摄氏度'
        return (9 / 5) * tc + 32

    @staticmethod
    def tf_to_tc(tf):
        '摄氏度转华氏度'
        return (5 / 9) * (tf - 32)


class Length:
    '长度处理模块'
    @staticmethod
    def m_to_ft(m):
        '中国长度米 转换为 英制长度 英尺'
        return m*3.28

    @staticmethod
    def ft_to_m(ft):
        '英制长度英尺 转换为 中国长度米'
        return ft*0.3


class Money:
    '货币转换模块'
    @staticmethod
    def usd_to_cny(usd):
        '美元转化为人民币'
        return usd*6.2945

    @staticmethod
    def cny_to_usd(cny):
        '人民币转化为美元'
        return cny*0.1589


class Transfer:
    '处理输入输出类'
    # 定义转换的单位菜单
    menus_li = ['F', 'C', 'USD', 'CNY', 'M', 'FT']

    def __init__(self, name: '自定义名称' = 'LH'):
        '定义初始化名字'
        self.name = name

    def welcome(self):
        '欢迎信息'
        print(f'欢迎使用{self.name}万能转换器')

    def my_help(self):
        '帮助信息'
        print(f''' 请直接输入数值+单位支持的转换：
            1.温度转换-摄氏度(f)与华氏度(c)之间的相互转换:\033[1;31;40m 1c或1f \033[0m
            2.长度转换-支持米(m)与英尺 (ft)之间的相互转换: \033[1;31;40m 1m或1ft \033[0m
            3.货币转换-支持人民币(CNY)与美元(USD)之间的相互转换:\033[1;31;40m 1cny或1usd \033[0m
          ''')

    def my_input(self):
        '对输入进行统一的格式化处理：1.去两端的空格 2.转化为大写'
        return input('请输入(q为退出，h为帮助):').strip().upper()

    def re_split(self, input_str):
        '对输入的字符串使用数值进行分割，如果正确，返回列表，如果格式错误返回False'
        li_result = []
        RE_NUM = '([\d|\.]{1,})'
        reg = re.compile(RE_NUM)
        li_reg = reg.split(input_str)
        try:
            if (len(li_reg) == 3) and (li_reg[2] != '') and (li_reg[0] == ''):
                # 如果输入正确，正则分割的列表为 ['', 1', '单位']
                li_result.append(float(li_reg[1]))
                li_result.append(li_reg[2])
                return li_result
            else:
                return False
        except Exception as e:
            print(e)
    
    def select_mode(self, li: list):
        '根据re_split返回的列表，进行操作，选择不同的转换模块'
        if li[1] in self.menus_li:
            if li[1] == 'F':  # 华式温度转换为摄氏温顿
                Tc = Temp.tf_to_tc(li[0])
                print(f'Tc = (5 / 9) * {li[0] - 32} = \033[1;33;40m{Tc}\033[0m ')
            elif li[1] == 'C':  # 摄氏温度转化为华式温度
                Tf = Temp.tc_to_tf(li[0])
                print(f'Tf = (9 / 5) * {li[0]} = \033[1;33;40m{Tf}\033[0m ')
            elif li[1] == 'M':  # 中国单位米 转化为 英制长度
                length_ft = Length.m_to_ft(li[0])
                print(f'Ft = 3.28 * length = \033[1;33;40m{length_ft}\033[0m')
            elif li[1] == 'FT':  # 英制长度转换为 中国长度米
                length_m = Length.ft_to_m(li[0])
                print(f'Ft = 3.28 * length = \033[1;33;40m{length_m}\033[0m')
            elif li[1] == 'CNY':  # 人民币 转化 美元
                money_us = Money.cny_to_usd(li[0])
                print(f'USD = 0.1589 * money = \033[1;33;40m{money_us}\033[0m')
            elif li[1] == 'USD':
                money_cny = Money.usd_to_cny(li[0])
                print(f'CNY = 6.2945 * money = \033[1;33;40m{money_cny}\033[0m')
        else:
            print('\033[1;31;40m 对不起，我还在进化中。\033[0m')


def main():
    trans = Transfer('LH')
    trans.welcome()
    trans.my_help()

    while True:
        words = trans.my_input()
        if words == 'Q':  # 退出程序
            print('拜拜，欢迎下次再来！')
            break
        elif words == 'H':  # 获取帮助信息
            trans.my_help()
        else:  # 除了q与h的情况
            result = trans.re_split(words)
            if result:
                trans.select_mode(result)
            else:
                print('\033[1;31;40m 输入有误,请重新输入\033[0m')


if __name__ == '__main__':
    main()
