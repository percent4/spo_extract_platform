# -*- coding: utf-8 -*-
# author: Jclian91
# place: Pudong Shanghai
# time: 2020-02-26 14:13
import os, re, json, traceback
import pandas as pd

if __name__ == '__main__':

    dir = '../../spo_tagging_platform/relation_output'
    files = os.listdir(dir)

    s, p, o = [], [], []
    tag = []
    text = []
    for file in files:
        file_path = os.path.join(dir, file)
        with open(file_path, 'r', encoding='utf-8') as f:
            content = [_.strip() for _ in f.readlines()]

        for line in content:
            s.append(line.split('#')[0])
            p.append(line.split('#')[1])
            o.append(line.split('#')[2])
            tag.append(line.split('#')[3])
            text.append(line.split('#')[-1])

    df = pd.DataFrame({"s": s,
                       "p": p,
                       "o": o,
                       "tag": tag,
                       "text": text
                       })

    df.to_excel("./spo.xlsx", index=False)