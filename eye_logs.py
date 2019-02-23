__author__ = 'Administrator'
import logging
import os
import sys


logger=logging.getLogger('__main__')
logger.setLevel(logging.INFO)
a=os.path.dirname(os.getcwd())
print(a)
if not os.path.exists('logs'):
    os.mkdir('\logs')
else:
    print('文件夹已存在')
file=os.getcwd()+'\logs'+'\logs.txt'
hander=logging.FileHandler(file,encoding='utf-8')
hander.setLevel(logging.DEBUG)
formatter=logging.Formatter('%(asctime)s - %(levelname)s:%(message)s - %(filename)s[line:%(lineno)d] - %(pathname)s')
hander.setFormatter(formatter)
sonsole=logging.StreamHandler()
sonsole.setLevel(logging.INFO)
sonsole.setFormatter(formatter)
logger.addHandler(hander)
logger.addHandler(sonsole)
