import os
import sys


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)


from core.adminmemo import AdminMemo
from core.memo import Memo
from utils.log_ctrl import lh_log
from utils.color_me import ColorMe

def main():
    # 配置密码文件 与 配置文件的绝对路径
    log = lh_log('main')
    pwd_db_path = os.path.join(BASE_DIR, 'db', 'pwd.db')
    conf_path = os.path.join(BASE_DIR, 'conf', 'conf.txt')

    admin = AdminMemo(pwd_db_path, conf_path)  # 生成对象

    # 获取终端输入的命令:python 程序名 -u name -指令 使用装饰器来验证密码
    sys_li = sys.argv

    if len(sys_li) == 1 or sys_li[1] == '-h' :  # 如果参数为  -h 或 只有文件的时候，跳转到帮助文档
        admin.help()
    elif sys_li[1] == '-r':  # 注册函数
        admin.regist()
    else:                    # 登入进去进行各种操作
        login_result = admin.login(sys_li[2], sys_li[4])
        if login_result['status']:  # 账号密码验证通过
            if sys_li[5] in admin.menus:
                if hasattr(admin, admin.menus.get(sys_li[5])):
                    run = getattr(admin, admin.menus.get(sys_li[5], None))
                    if run:
                        run()
                else:
                    log.waring('系统menus错误，请检查')
            else:
                print('无该选项，请使用python main.py -h 核对后输入')

        else:  # 账号密码错误，不同的状态
            print(ColorMe(login_result['statusText']).red())

if __name__ == '__main__':
    main()