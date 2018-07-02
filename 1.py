import configparser

conf = configparser.ConfigParser(interpolation=configparser.ExtendedInterpolation())

# conf['DEFAULT'] = {}
# conf['DEFAULT']['path'] = 'c:/f/d'

# conf['lh'] = {}
# conf['lh']['path'] = '${path}/init.com'

# with open('1.txt', 'a', encoding='utf-8') as f:
#     conf.write(f)

conf.read('1.txt')
print(conf.get('lh','path'))