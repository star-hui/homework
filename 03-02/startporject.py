# 创建工程目录脚本

import os
import sys

__author__ = 'LH'
path = os.path.dirname(os.path.abspath(__file__))


def start_project():
    '从命令行建立新的工程名，默认是lh'
    project_name = 'lh_demo'
    if len(sys.argv) > 1:
        project_name = sys.argv[1]

    # 创建标准化目录 与 __init__文件
    folders = ['bin', 'conf', 'core', 'db', 'log', 'utils']
    for folder in folders:
        folder_path = os.path.join(path, project_name, folder)
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        with open(os.path.join(path, project_name, folder, '__init__.py'), 'w'):
            pass

    # 创建readme
    with open(os.path.join(path, project_name, 'readme.md'), 'w') as f:
        f.write('#'+project_name + '\n\n')
        f.write('> Author:' + __author__ + '\n')


def main():
    start_project()

if __name__ == '__main__':
    main()