'''
1. 如果时间不存在，
2.如果时间存在
'''
from datetime import datetime

from dateutil import parser
from dateutil.relativedelta import relativedelta


def resolve_thing(thing):
    '''根据各种时间，返回标准时间'''
    try:
        if thing.find('明天') > -1:
            return (datetime.now() + relativedelta(days=1)).strftime('%Y-%m-%d %X'), thing[thing.find('天')+1:]
        
        if thing.find('后天') > -1:
            return (datetime.now() + relativedelta(days=2)).strftime('%Y-%m-%d %X'), thing[thing.find('天')+1:]

        if thing.find('下个月') > -1:
            day = int(thing[thing.find('月')+1:thing.find('号')])
            return (datetime.now() + relativedelta(months=1, day=day)).strftime('%Y-%m-%d %X'), thing[thing.find('号')+1:]
        if thing.find('下个礼拜') > -1:
            # 一个礼拜是从礼拜1开始计算的
            print('解析星期')
            day = int(thing[thing.find('礼拜')+2: thing.find('礼拜')+3]) -1 
            print(day)
            return (datetime.now() + relativedelta(weeks=1, weekday=day)).strftime('%Y-%m-%d %X'), thing[thing.find('礼拜')+3:]

    except Exception as e:
        print(e)

    
def main():
    # s = '明天去买西瓜'
    # s = '后天去买西瓜'
    s = '下个礼拜3去买习惯'
    print(resolve_thing(s))
    # input_time = input('请输入一个月份eg(2017 1 1)')
    # year, month, day = input_time.split(' ')
    # print(year, month, day)
    
if __name__ == '__main__':
    main()


flag = True

while flag:
    name = input('12312').strip()
    if name == 'q':
        flag == ''
