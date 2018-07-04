import getpass
import json
import os
import pickle
import sys
from datetime import datetime
from functools import wraps

from dateutil import parser
from dateutil.relativedelta import relativedelta

import utils.log_ctrl
from core.memo import Memo
from utils.color_me import ColorMe
from utils.config import MyConf
from utils.dataexport import Export
from utils.myemail import MailMaster

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

__auth__ = 'LH'


def auth(func):
    @wraps(func)
    def inner(*args, **kwargs):
        pwd = getpass.getpass('请输入删除密码(8888)，来确定删除:')
        if pwd == '8888':
            func(*args, **kwargs)
        else:
            print('密码错误')
    return inner

class AdminMemo:
    '管理备忘录类'
    menus = {
        '-a': 'add',
        '-r': 'rigist',
        '-d': 'delete',
        '-p': 'print_all',
        '-m': 'modify',
        '-e': 'export',
        '-email': 'send_email',
        '-s_date': 'search_date',
        '-s_thing': 'search_thing',
    }  # 定义全局菜单

    def __init__(self, pwd_path, conf_path):
        '启动自动加载备忘录列表,把每一个对象都存放在列表中'
        self.log = utils.log_ctrl.lh_log('AdminMemo')
        self.pwd_path = pwd_path  # 密码文件路径
        self.conf_path = conf_path  # 配置文件路径
        self.db_path = ''         # 数据库文件路径，在登入以后替换
        self.conf = MyConf(self.conf_path)  # 加载密码文件
        self.conf.set_default(os.path.join(BASE_DIR, 'db'))   # 每次启动，把base_dir存入到config，避免在程序移动目录出错，后续子章节都是用$这种使用方式
        self.__pwd = self.load_pwd()  # 加载密码配置文件配置文件
        self.memo_list = []
        self.welcome()

    def load_pwd(self):
        '打开账户pickle文件，加载账号表，返回一个账号，密码的字典'
        try:
            with open(self.pwd_path, 'rb') as f:
                self.log.info('加载配置文件')
                user_dic = pickle.load(f)
        except Exception as e:
            self.log.warning('配置信息不存在')
            # 当存储文件不存在时 或 pickle得到为空时 会报错，直接生成一个空列表
            user_dic = {}

        return user_dic

    def login(self, username, password):
        '''
        验证账号，密码是否匹配：
            匹配返回1，验证通过，则使用username 加载配置文件中指定的section。并加载数据
            不匹配返回0.
        '''
        ret = {'status':0, 'statusText':None}
        if username in self.__pwd.keys():
            if self.__pwd.get(username) == password:
                print(f'{username}欢迎登入!')
                self.db_path = self.conf.file_path(username)  # 验证通过之后，加载该用户的配置文件，读取该用户的数据库路径
                print(self.db_path)
                self.log.info(f'{username}登入成功')
                self.memo_list = self.load()  # 加载数据库文件
                ret['status'] = 1
                ret['statusText'] = '登入成功'
                return ret
            else:
                self.log.warning(f'{username}密码错误哈')
                ret['status'] = 0
                ret['statusText'] = '密码错误'
                return ret
        else:
            ret['status'] = 0
            ret['statusText'] = '用户名不存在'

            print('用户名不存在')
            return ret

    def send_email(self):
        '''调用查询接口'''
        body = self.search_date()
        mail = MailMaster()
        mail_to_addr = input('请输入收件人邮箱:')
        mail.add_emali_to_list(mail_to_addr)
        mail.send_email('LH备忘录数据', body=body)
        

    def regist(self):
        '注册账号,注册成功后，生产配置文件，并写入密码文件'
        while True:
            reg_username = input(ColorMe('请输入注册的用户名,按q退出').yellow())
            
            if reg_username == 'q':
                break

            elif self.__pwd.get(reg_username):
                print(ColorMe('用户名已经存在，请换一个用户名').red())
                continue
            
            reg_password1 = input(ColorMe('请输入注册的密码').yellow())
            reg_password2 = input(ColorMe('请再次输入注册的密码').yellow())
            if reg_password1 != reg_password2:
                print('两次密码不一致，请重新输入')
                continue
            self.__pwd[reg_username] = reg_password1
            self.pwd_save()  # 1.保存账号密码到pwd文件中

            self.log.info(f'{reg_username}-注册成功')
            dic = {
                reg_username:{
                    # 'path': os.path.join(BASE_DIR, 'db'),
                    'path' : '${base_dir}',
                    'file_name': reg_username,
                    'db_type': 'db'
                }
            }

            self.conf.write(dic)  # 2.保存数据库的路径到配置文件中
            self.conf.save()

            print('注册成功')
            break

    def pwd_save(self):
        '保存密码文件'
        with open(self.pwd_path, 'wb') as f:
            print(self.pwd_path)
            pickle.dump(self.__pwd, f)
            self.log.info('密码文件报错成功')
        
    def welcome(self):
        '打印欢迎语'
        print(f'欢迎来到{__auth__}的笔记本')
        self.log.info('进入欢迎函数')

    def print_menu(self):
        '打印菜单'
        for k, v in self.menus.items():
            print(ColorMe(f'    {k}     {v}').blue())
        self.log.info('打印菜单')

    def add_input(self, thing):
        '处理添加的输入,根据各种事件，处理成一个标准事件格式后，返回一个元祖(time,thing)'
        try:
            if thing.find('-') >-1:
                d, thing = thing.split('-')
                return parser.parse(d).strftime('%Y-%m-%d %X'), thing
            elif thing.find('明天') > -1:
                return (datetime.now() + relativedelta(days=1)).strftime('%Y-%m-%d %X'), thing[thing.find('天')+1:]
            
            elif thing.find('后天') > -1:
                return (datetime.now() + relativedelta(days=2)).strftime('%Y-%m-%d %X'), thing[thing.find('天')+1:]
            
            elif thing.find('下个礼拜') > -1:
            # 一个礼拜是从礼拜1开始计算的
                day = int(thing[thing.find('礼拜')+2: thing.find('礼拜')+3]) -1 
                print(day)
                return (datetime.now() + relativedelta(weeks=1, \
                weekday=day)).strftime('%Y-%m-%d %X'), thing[thing.find('礼拜')+3:]

            elif thing.find('下个月') > -1:
                day = int(thing[thing.find('月')+1:thing.find('号')])
                return (datetime.now() + relativedelta(months=1, day=day)).strftime('%Y-%m-%d %X'), thing[thing.find('号')+1:]

            
            else:
                return datetime.now().strftime('%Y-%m-%d %X')

        except Exception as e:
            self.log.warning('输入有误')
            return False
        
    def add(self):
        '添加一条数据，存储到Memo对象中'
        try:
            thing = input('请输入事件:')
            if self.add_input(thing):
                memo = Memo(*self.add_input(thing))
                print(memo.date, memo.thing)

            # 处理x.id 自增加，利用最后一条memo的id + 1
            if len(self.memo_list) == 0:
                memo.id = 0
            else:
                memo.id = int(self.memo_list[-1]._id) + 1

            self.memo_list.append(memo)
            self.save()
            self.log.info(ColorMe('添加一条数据成功').red())

        except Exception as e:
            self.log.warning('添加事件，出现未知错误')
            print(ColorMe('添加失败，请重新输入').red(), e)

    @auth
    def delete(self):
        '删除一条记录'
        try:
            if len(self.memo_list) == 0:
                print('已经没了，你还删')
            else:
                self.print_all()
                num = int(input('请输入要删除的编号'))
                for memo in self.memo_list:
                    if memo.id == num:
                        self.memo_list.remove(memo)
                        self.log.info('事件，删除成功')
                        print(ColorMe('删除成功').red())
                self.print_all()
                self.save()
        except Exception as e:
            print('删除出错，请重新输入')

    def save(self):
        '保存memo_list到文件中'
        self.log.debug(self.db_path)
        with open(self.db_path, 'wb') as f:
            f.write(pickle.dumps(self.memo_list))
            print(ColorMe('文件保存成功').red())
            self.log.info('文件保存成功')

    def help(self):
        print("""
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
        """)
            
    def load(self):
        '加载备忘录文件，当文件读入 和 序列化出错的时候，自动生成新的列表'
        try:
            with open(self.db_path, 'rb') as f:
                memo_list = pickle.loads(f.read())
        except Exception as e:
            # 当存储文件不存在时 或 pickle得到为空时 会报错，直接生成一个空列表
            memo_list = []
        self.log.info('加载数据库文件')
        return memo_list

    def print_all(self):
        '打印所有备忘录'
        if len(self.memo_list) == 0:
            print(ColorMe('备忘录中没有记录，请去添加纪录').red())
        for memo in self.memo_list:
            print(ColorMe(f'{memo.id}   {memo.date:5} --{memo.thing}').green())
        self.log.info('输出所有的日志')

    def export(self):
        '把备忘录内容导出成指定格式'
        try:
            memo_dic = {}  # 使用字典，优化速度
            if len(self.memo_list) == 0:
                print(ColorMe('备忘录中没有记录，请去添加纪录').red())
            else:
                for memo in self.memo_list:
                    # print(ColorMe(f'{memo.id}   {memo.date:5} -- {memo.name}--{memo.thing}').green())
                    memo_dic[memo.id] = [memo.date,  memo.thing]
                ex = Export(memo_dic)
                ex_path = {
                    'pdf': 'export_pdf',
                    'txt': 'export_txt',
                    'xlsx': 'export_excle',
                    'word': 'export_word'
                }
                print(ColorMe('''
                支持的格式为：
                    pdf、word、xlsx、txt
                ''').red())
                choice_input = input('请输入要到出的格式').strip()
                if choice_input in ex_path:
                    getattr(ex, ex_path.get(choice_input))()
                    self.log.info('导出成功')

                else:
                    self.log.warning('没有该选项')
        except:
            self.log.warning('导出失败')
        # todo 导出优化


    def search_date(self):
        '根据'
        memo_dic = {}
        input_time = input('请输入一个月份eg(2017 1 1)')
        year, month, day = input_time.split(' ')
        year, month, day = int(year), int(month), int(day)
        print(year, month, day)
        if year == 0:  #
            for memo in self.memo_list:
                memo_dic[memo.id] = {memo.date: memo.thing}
            print(json.dumps(memo_dic, ensure_ascii=False))
            return json.dumps(memo_dic, ensure_ascii=False)

        elif month == 0:
            for memo in self.memo_list:
                if parser.parse(memo.date).year == year:
                   memo_dic[memo.id] = {memo.date: memo.thing}
            print(json.dumps(memo_dic, ensure_ascii=False))
            return json.dumps(memo_dic, ensure_ascii=False)
        elif day == 0:
            for memo in self.memo_list:
                if parser.parse(memo.date).year == year and parser.parse(memo.date).month == month :
                   memo_dic[memo.id] = {memo.date: memo.thing}
            print(json.dumps(memo_dic, ensure_ascii=False))
            return json.dumps(memo_dic, ensure_ascii=False)
        elif year != 0 and month != 0 and day !=0:
            for memo in self.memo_list:
                if parser.parse(memo.date).year == year and parser.parse(memo.date).month == month and parser.parse(memo.date).day == day:
                   memo_dic[memo.id] = {memo.date: memo.thing}
            print(json.dumps(memo_dic, ensure_ascii=False))
            return json.dumps(memo_dic, ensure_ascii=False)

 
                     
        self.log.info('按照时间搜索日志')
        for memo in self.memo_list:
            if parser.parse(memo.date).month == input_time:
            # if input_time == memo.date :
                print(ColorMe(f'{memo.id}--{memo.date:5}--{memo.thing}').yellow())

    def search_thing(self):
        '搜索thing，根据输入来进行模糊匹配，查询备忘录'
        try:
            memo_dic = {}
            words_input = input('请输入事件').strip()
            for memo in self.memo_list:
                if memo.thing.find(words_input) > -1:
                    memo_dic[memo.id] = {memo.date: memo.thing}
                    # print(ColorMe(f'{memo.id}--{memo.date:5}--{memo.thing}').yellow())
            self.log.info('按照 事件 来搜索事件')
            print(json.dumps(memo_dic, ensure_ascii=False))
            return json.dumps(memo_dic)
        except Exception as e:
            print('未知错误')

    # def search_name(self):
    #     '搜索thing，根据输入来进行模糊匹配，查询备忘录'
    #     words_input = input('请输入姓名').strip()
    #     for memo in self.memo_list:
    #         if memo.name == words_input:
    #             print(ColorMe(f'{memo.id}--{memo.date:5}--{memo.name}-{memo.thing}').yellow())
    #     self.log.info('按照 名字 来搜索事件')

    def modify(self):
        '修改某条备忘录'
        self.print_all()
        self.log.info('修改备忘录')
        try:
            index_input = int(input('请输入需要修改的编号：').strip())
     
            flag = True  # for 循环结束标志位

            for memo in self.memo_list:
                if not flag:  # 在while退出的时候，就不再for循环了，节约计算时间。
                    break

                if index_input == memo.id:
                    while 1:
                        words_input = input('请输入要修改的字段(date或thing) q返回:').strip()

                        if words_input == 'thing':
                            new_thing = input('请输入一个新thing：')
                            memo.thing = new_thing
                            print('修改成功')
                            self.save()
                            return True
                        elif words_input == 'date':
                            new_date = input('请输入一个新date:2017-01-01：').strip()
                            memo.date = parser.parse(new_date).strftime('%Y-%m-%d %X')
                            print('修改成功')
                            self.save()
                            return True
                        # elif words_input == 'name':
                        #     new_name = input('请输入一个新name').strip()
                        #     memo.name = new_name
                        #     print('修改成功')
                        #     return True
                        elif words_input == 'q':
                            flag = False
                            break
                        else:
                            print(ColorMe('输入有误').red())
            else:  # 是fou的else
                print(ColorMe('没有该编号，请重新输入').red())
        except Exception as e:
            print('输入有误,请重新输入')

    def my_quit(self):
        '退出时，调用save自动保存'
        self.log.info('退出程序')
        self.pwd_save()
        self.save()
        self.conf.save()
        print('下次再见！')
        sys.exit()

def main():
    pwd_db_path = os.path.join(BASE_DIR, 'db', 'pwd.db')
    conf_path = os.path.join(BASE_DIR, 'conf', 'conf.txt')
    admin = AdminMemo(pwd_db_path, conf_path)
    admin.db_path = os.path.join(BASE_DIR,'db','test.db')
    admin.add()

if __name__ == '__main__':
    main()
