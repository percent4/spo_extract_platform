# -*- coding: utf-8 -*-
# author: Jclian91
# place: Pudong Shanghai
# time: 2020-02-26 16:21
import os, re, json, traceback
from random import shuffle

if __name__ == '__main__':

    dir = '../../spo_tagging_platform/tagging_output'
    files = os.listdir(dir)
    shuffle(files)

    train_ratio = 0.8
    train_index = int(train_ratio*len(files))

    train_files = files[:train_index]
    test_files = files[train_index:]

    with open("spo.train", "w", encoding="utf-8") as f:

        for file in train_files:
            file_path = os.path.join(dir, file)
            with open(file_path, "r", encoding="utf-8") as g:
                content = g.read().replace('\t', ' ')

            f.write(content)
            f.write('\n')

    with open("spo.test", "w", encoding="utf-8") as f:

        for file in test_files:
            file_path = os.path.join(dir, file)
            with open(file_path, "r", encoding="utf-8") as g:
                content = g.read().replace('\t', ' ')

            f.write(content)
            f.write('\n')

    with open("spo.dev", "w", encoding="utf-8") as f:

        for file in test_files:
            file_path = os.path.join(dir, file)
            with open(file_path, "r", encoding="utf-8") as g:
                content = g.read().replace('\t', ' ')

            f.write(content)
            f.write('\n')

    print("ok!")