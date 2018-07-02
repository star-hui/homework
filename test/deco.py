# import time
# from functools import wraps

# class DecoAnything:
#     def __init__(self, funcname, filename='log-tets.name'):
#         self.funcname = funcname
#         self.filename = filename

#     def __call__(self, func):
#         def inner(*args, **kwargs):
#             if hasattr(self, self.funcname):
#                 myfuc = getattr(self, self.funcname)
#                 if myfuc(func):  # 当添加的功能运行成功返回True时，就执行传递过来的函数
#                     func(*args, **kwargs)

#         return inner

#     def log(self, func):
#         str_log = f'函数{func.__name__}开始运行了'
#         with open(self.filename, 'a', encoding='utf-8') as f:
#             print(str_log)
#             f.write(str_log)
#         return True
    
#     def check(self, func):
#         str_log = f'函数{func.__name__}开始运行了'
#         print(str_log)
#         username = input('请输入用户名')
#         password = input('请输入密码')
#         if username == 'lh' and password == '8888':
#             return True
#         else:
#             return False

# @DecoAnything('check')
# @DecoAnything('log')  # log传递到init中，tony传递到call中
# def tony():
#     print('我是tony在函数', tony.__name__)
        
# def main():
#     tony()
    
# if __name__ == '__main__':
#     main()

class Myapp:
    def __init__(self):
        self.func_map = {}

    def regist(self, name):
        '''
        完成 路径 与 函数的绑定
        '''
        def inner(func):
            self.func_map[name] = func
        return inner

    def call_method(self, name=None):
        '''使用字典直接查找到方法，直接运行'''
        func = self.func_map.get(name, None)
        if func is None:
            raise Exception('no function', 'name')
        return name, func()

app = Myapp()

@app.regist('/')  # 先运行regist函数得到了内部函数，再用装饰器语法糖,把内部函数传入进去，完成了整个函数
def main_page_func():
    return "This is the main page."

@app.regist('/next_page')
def next_page_func():
    return "This is the next page."


def main():
    print(app.call_method('/'))
    print(app.call_method('/next_page'))

if __name__ == '__main__':
    main()