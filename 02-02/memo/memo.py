# /usr/bin/env python
# -*- coding=utf-8 -*-
# author = LH
# memo.py


import pickle
import sys
from color_me import ColorMe

__auth__ = 'LH'


class Memo:
    '备忘录类'
    def __init__(self, date: str, name: str, thing: str):
        '初始化方法，保存id,date,name,thing'
        self._id = 0
        self.name = name
        self.thing = thing
        self.date = date
    
    @property
    def id(self):
        '把私有属性供外部查看'
        return self._id

    @id.setter
    def id(self, val):
        '把私有属性供外部修改'
        self._id = val


class AdminMemo:
    '管理备忘录类'
    menus = {
        '1': 'add',
        '2': 'delete',
        '3': 'print_all',
        '4': 'search_date',
        '5': 'search_thing',
        '6': 'search_name',
        '7': 'modify',
        '8': 'save',
        '9': 'my_quit'
    }  # 定义全局菜单

    def __init__(self):
        '启动自动加载备忘录列表,把每一个对象都存放在列表中'
        self.memo_list = self.load()

    def welcome(self):
        '打印欢迎语'
        print(f'欢迎来到{__auth__}的笔记本')

    def print_menu(self):
        '打印菜单'
        for k, v in self.menus.items():
            print(ColorMe(f'    {k}     {v}').blue())

    def add_input(self):
        '处理添加的输入,返回一个列表[name,time,thing]'
        input_memo = input('请输入事件 eg(1.1-小8-学习python):').strip()
        input_list = input_memo.split('-')
        if len(input_list) == 3:
            return input_list
        else:
            print(ColorMe('输入有误').red())

    def add(self):
        '添加一条数据，存储到Memo对象中'
        try:
            memo = None
            memo = Memo(*self.add_input())
            print(memo.name, memo.date, memo.thing)

            # 处理x.id 自增加，利用最后一条memo的id + 1
            if len(self.memo_list) == 0:
                memo.id = 0
            else:
                memo.id = int(self.memo_list[-1]._id) + 1

            self.memo_list.append(memo)
            print(ColorMe('添加成功').red())
        except Exception as e:
            print(ColorMe('添加失败，请重新输入').red(), e)

    def delete(self, num: int):
        '删除一条记录'
        try:
            if len(self.memo_list) == 0:
                print('已经没了，你还删')
            else:
                for memo in self.memo_list:
                    if memo.id == num:
                        self.memo_list.remove(memo)

                print(ColorMe('删除成功').red())
        except Exception as e:
            print('删除出错，请重新输入')

    def save(self):
        '保存memo_list到文件中'
        with open('memo.pkl', 'wb') as f:
            f.write(pickle.dumps(self.memo_list))
            print(ColorMe('文件保存成功').red())
            
    def load(self):
        '加载文件，当文件读入 和 序列化出错的时候，自动生成新的列表'
        try:
            with open('memo.pkl', 'rb') as f:
                memo_list = pickle.loads(f.read())
        except Exception as e:
            # 当存储文件不存在时 或 pickle得到为空时 会报错，直接生成一个空列表
            memo_list = []
        
        return memo_list

    def print_all(self):
        '打印所有备忘录'
        if len(self.memo_list) == 0:
            print(ColorMe('备忘录中没有记录，请去添加纪录').red())
        for memo in self.memo_list:
            print(ColorMe(f'{memo.id}   {memo.date:5} -- {memo.name}--{memo.thing}').green())

    def search_date(self):
        '根据时间搜索备忘录'
        input_time = input('请输入一个时间eg(1.1 OR 11.22)')
        for memo in self.memo_list:
            if input_time == memo.date:
                print(ColorMe(f'{memo.id}--{memo.date:5}--{memo.name}-{memo.thing}').yellow())

    def search_thing(self):
        '搜索thing，根据输入来进行模糊匹配，查询备忘录'
        words_input = input('请输入事件').strip()
        for memo in self.memo_list:
            if memo.thing.find(words_input) > -1:
                print(ColorMe(f'{memo.id}--{memo.date:5}--{memo.name}-{memo.thing}').yellow())

    def search_name(self):
        '搜索thing，根据输入来进行模糊匹配，查询备忘录'
        words_input = input('请输入姓名').strip()
        for memo in self.memo_list:
            if memo.name == words_input:
                print(ColorMe(f'{memo.id}--{memo.date:5}--{memo.name}-{memo.thing}').yellow())

    def modify(self):
        '修改某条备忘录'
        self.print_all()
        try:
            index_input = int(input('请输入需要修改的编号').strip())
     
            flag = True  # for 循环结束标志位

            for memo in self.memo_list:
                if not flag:  # 在while退出的时候，就不再for循环了，节约计算时间。
                    break

                if index_input == memo.id:
                    while 1:
                        words_input = input('请输入要修改的字段(name或date或thing) q返回:').strip()

                        if words_input == 'thing':
                            new_thing = input('请输入一个新thing')
                            memo.thing = new_thing
                            print('修改成功')
                            return True
                        elif words_input == 'date':
                            new_date = input('请输入一个新date').strip()
                            memo.date = new_date
                            print('修改成功')
                            return True
                        elif words_input == 'name':
                            new_name = input('请输入一个新name').strip()
                            memo.name = new_name
                            print('修改成功')
                            return True
                        elif words_input == 'q':
                            flag = False
                            break
                        else:
                            print(ColorMe('输入有误').red())
            else:
                print(ColorMe('没有该编号，请重新输入').red())
        except Exception as e:
            print('输入有误,请重新输入')

    def my_quit(self):
        '退出时，调用save自动保存'
        self.save()
        print('下次再见！')
        sys.exit()


def main():
    admin = AdminMemo()
    while 1:
        admin.print_menu()
        select = input('请输入你的选择:')

        if select in admin.menus:
            run = getattr(admin, admin.menus.get(select), None)  # 如果不存在菜单，则返回None
            if run:
                if select == '2':
                    admin.print_all()
                    try:
                        index = int(input('请输入要删除的选项:'))
                        run(index)
                    except Exception as e:
                        print('删除出错，请输入正确的选项')
                else:
                    run()
            else:
                print('选项不存在,请检测菜单项添加是否正确')     
                
        else:
            print('请重新输入选项')
            
if __name__ == '__main__':
    main()