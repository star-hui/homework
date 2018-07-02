
 Lhmemo

> Author:LH

<!-- TOC -->

- [1. LH-Memo v2.0实现的功能](#1-lh-memo-v20实现的功能)
- [2. 工程文件说明](#2-工程文件说明)
- [3. 学习的笔记](#3-学习的笔记)
- [4. 程序版本与依赖说明](#4-程序版本与依赖说明)
- [5. 使用帮助](#5-使用帮助)

<!-- /TOC -->

# 1. LH-Memo v2.0实现的功能
v2.0  
1. 重写整个程序，采用命令行的方式调用每个功能。
2. 实现了备忘录事件的增删改查。
3. 采用pickle实现文件的密文的保护，使用config为程序添加配置，有日志功能。
2. 采用了api的方式，json返回数据。
3. 使用了装饰器，在删除事件的时候，再一次鉴权。


v1.0  
1. 在原先的基础上增加了，登入与注册功能
2. 增加了配置文件功能，实现了每个账户的数据库的路径
3. 增加了备忘录导出功能，支持4中格式导出:pdf、txt、 word、 excle
4. 增加了日志功能，可以随意的关闭


# 2. 工程文件说明
    bin     函数入口
    conf    配置文件，每个账户的配置
    core    核心代码，存放adminMemo和Memo两个类
    db      数据库文件，每个用户一个数据库文件
    export  导出的文件，存放在这里
    log     日志存储的地方
    utils   自己写的工具，为主程序服务，主要有四个类
                color_me    添加颜色类
                config      配置类
                dataexport  将事件导出类
                log_ctrl    日志类

# 3. 学习的笔记
    详见个人博客，第四篇：文件与模块
    https://www.cnblogs.com/louhui/p/8709830.html

# 4. 程序版本与依赖说明
    python版本：3.6+
    所需第三方模块：
        openpyxl==2.5.3
        pdfkit==0.6.1
        PyPDF2==1.26.0
        python-docx==0.8.6
        reportlab==3.4.0
        dateutil

# 5. 使用帮助

1. 进入程序的bin目录下，在命令行python main.py 就可获取帮助 或 python main.py -r
2. 基本功能  
                        菜单帮助信息：
            获取帮助：  python main.py -h
            注册:       python main.py -r
            添加事件：  python main.py -u 用户名 -p 密码 -a
                        事件写法:两种：
                            1. 指定时间使用-分割
                                    2017 1 2-去买酒
                                    1 2-去买酒
                            2. 相对时间，支持如下
                                明天去买酒
                                后天去买酒
                                下个礼拜3去买酒
                                下个月5号去买酒
            删除事件:   python main.py -u 用户名 -p 密码 -d
            修改事件：  python main.py -y 用户名 -p 密码 -m
            
            导出事件：  python main.py -u 用户名 -p 密码 -e
                                支持pdf，txt，word，excel四种格式
            邮件事件：  python main.py -u 用户名 -p 密码 -email
            查询事件：  
                    所有事件:       python main.py -y 用户名 -p 密码 -p
                    模糊匹配thing:  python main.py -y 用户名 -p 密码 -s_thing
                    时间匹配事件:       python main.py -y 用户名 -p 密码 -s_date
                                          0  0 0 代表 全部
                                        2017 0 0 代表 2017年
                                        2017 3 0 代表 2017年3月份
                                        2017 3 3 代表 2017年3月3日