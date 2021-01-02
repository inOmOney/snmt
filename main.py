import time
import re
import os
from src.Control import Control

con = Control()

if __name__ == '__main__':
    a = """ 
苏宁抢购-功能列表：                                                                                
 1. 预约商品
 2. 秒杀抢购商品
"""
    print(a)
    num = input("请输入选项: ")

    if num == '1' or num == '2':
        con.main(num)
    else:
        print('退出')

