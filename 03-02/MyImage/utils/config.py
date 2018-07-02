import configparser
import os


class MyConf:
    def __init__(self, path: str):
        '初始化的时候读取配置文件'
        self.path = path
        self.conf = configparser.ConfigParser(interpolation=configparser.ExtendedInterpolation())
        self.conf.read(self.path, encoding='utf-8')  # 空文件也不会出错,使用UTF-8，不会报错

    def set_default(self,base_dir):
        '''设置DEFAULT章节，以便于程序移动目录也能正常的加载数据'''
        self.conf['DEFAULT'] ={}
        self.conf['DEFAULT']['base_dir'] = base_dir
        self.save()

    def add(self, section):
        '增加一个章节'
        if self.conf.has_section(section):
            print('改章节已经存在')
        else:
            self.conf.add_section(section)

    def read_val(self, section, option):
        return self.conf.get(section, option)

    def write(self, dic: dict):
        '直接写入一个字典'
        for k, v in dic.items():
            self.conf[k] = v

    def file_path(self, section):
        user_section = self.conf[section]
        return os.path.join(user_section['path'], user_section['file_name'] + '.' + user_section['db_type'])

    def del_section(self, section):
        '删除section'
        if self.conf.has_section(section):
            self.conf.remove_section(section)
        else:
            print('该章节不存在')

    def modify_val(self, section, option, val):
        if self.conf.has_section(section) and self.conf.has_option(section, option):
            self.conf.set(section, option, val)
            print('修改成功')
        else:
            print('修改失败')

    def delete_option(self, section, option):
        '删除指定的section下的option'
        if self.conf.has_section(section) and self.conf.has_option(section, option):
            self.conf.remove_option(section, option)
        else:
            print('section or option is wrong!')

    def save(self):
        '保存到配置文件中'
        with open(self.path, 'w', encoding='utf-8') as f:
            self.conf.write(f)

    def check_all(self):
        '打印全部'
        for k, v in self.conf.items():
            print(f'[{k}]')
            for key, val in self.conf.items(k):
                print(key, val)


def main():
    data = {
        'DEFAULT': {
            'base_dir': 'c:/Users/sothi/Desktop/py2018/02-auto/data',
            'db_type': 'db'
        },
        'de8ug': {
            'path': 'c:/Users/sothi/Desktop/py2018/02-auto/data',
            'file_name': 'de8ug',
            'db_type': 'pkl'
        }
    }

    data.get('lh', False)
    base_dir = r'C:\Users\LH\Desktop\data'
    path = os.path.join(base_dir, 'comeon123.ini')
    myconf = MyConf(path)
    myconf.write(data)
    print(myconf.file_path('de8ug'))

if __name__ == '__main__':
    main()

