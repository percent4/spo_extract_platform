# -*- coding: utf-8 -*-
# author: Jclian91
# place: Pudong Shanghai
# time: 2020-02-27 01:04
import json
import requests
import pandas as pd
from tqdm import tqdm
from pyltp import SentenceSplitter

# 小说的名称
book_name = 'santi'

# txt文件读取
with open('./corpus/%s.txt' % book_name, 'r', encoding='UTF-16') as f:
    content = f.read()

sents = [_.strip().replace(" ", "") for _ in list(SentenceSplitter.split(content)) if _.strip()]


# 逐句抽取并保留抽取结果至列表中
texts = []
subjs, preds, objs = [], [], []

bar = tqdm(sents)
for ch, line in zip(bar, sents):

    req = requests.post("http://localhost:12308/spo_extract", data={"text": line})
    res = json.loads(req.content)

    if res:
        print("\n原文: %s" % line)
        print("SPO: %s" % res)

        for item in res:
            subj = item["subject"]
            pred = item["predicate"]
            obj = item["object"]

            if subj != obj:
                subjs.append(subj)
                preds.append(pred)
                objs.append(obj)
                texts.append(line)

# 将抽取的三元组结果保存成EXCEL文件

df = pd.DataFrame({"S": subjs,
                   "P": preds,
                   "O": objs,
                   "text": texts
                   })

df.to_excel("./excels/%s.xlsx" % book_name, index=False)
