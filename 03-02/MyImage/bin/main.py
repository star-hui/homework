import os
import sys


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

from core.myimage import ImageUtils
from utils.log_ctrl import lh_log


def main():
    try:
        ima = ImageUtils()
        log = lh_log('main')
        menus = ima.menus
        sys_li = sys.argv
        if len(sys_li) == 1:
            ima.help()
            sys.exit()
        cmd = sys_li[1]

        if cmd in menus:
            run = getattr(ima, menus.get(cmd, None), None)
            if run:
                if cmd == '-r':
                    run(sys_li[2], sys_li[3], int(sys_li[4]))
                elif cmd == '-c':
                    run(sys_li[2], int(sys_li[3]), int(sys_li[4]),int(sys_li[5]),int(sys_li[6]) )
                elif cmd == '-t':
                    run(sys_li[2], float(sys_li[3]))
                elif cmd == '-t_all':
                    run(float(sys_li[2]))
                elif cmd == '-size':
                    run(sys_li[2], int(sys_li[3]), int(sys_li[3]))
                elif cmd == '-size_all':
                    run(int(sys_li[2]), int(sys_li[3]))
                else:
                    run()
            else:
                print('请联系管理员，菜单项不正确')
        else:
            print('选项不存在，请使用帮助信息(-h)核对后输入')
    except Exception as e:
        log.warning('发生了错误:')
        print(e)

if __name__ == '__main__':
    main()