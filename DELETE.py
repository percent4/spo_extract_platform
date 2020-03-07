# -*- coding: utf-8 -*-
# author: Jclian91
# place: Pudong Shanghai
# time: 2020-03-01 23:42
import os, re, json, traceback
from tqdm import tqdm
import time

lst = ["a", "b", "c", "d"]
bar = tqdm(lst)
for letter, char in zip(lst, bar):

    time.sleep(1)
    bar.set_description("Processing %s" % char)