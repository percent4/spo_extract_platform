# -*- coding: utf-8 -*-
# time: 2019-03-14
# place: Xinbeiqiao, Beijing

import os

# 获取当前所在目录的txt文本的最大数值
def get_max_num(path):
    files = os.listdir(path)
    if files:
        numbers = list(map(lambda x: int(x.replace('.txt', '')), files))
        return max(numbers)
    else:
        return 0