# -*- coding: utf-8 -*-

import pandas as pd
from pprint import pprint

df = pd.read_excel('spo.xlsx')

print('总数: %s' % len(df))
pprint(df['tag'].value_counts())

texts = []
for s, p, o, text in zip(df['s'].tolist(), df['p'].tolist(), df['o'].tolist(), df['text'].tolist()):
    text = '#'.join([s, p, o, text.replace(s, len(s)*'S').replace(p, len(p)*'P').replace(o, len(o)*'O')])
    texts.append(text)

df['text'] = texts

# df = df.iloc[:10, :] # 取前n条数据进行模型方面的测试

train_df = df.sample(frac=0.8, random_state=1024)
test_df = df.drop(train_df.index)

with open('train.txt', 'w', encoding='utf-8') as f:
    for text, rel in zip(train_df['text'].tolist(), train_df['tag'].tolist()):
        f.write(str(rel)+' '+text+'\n')

with open('test.txt', 'w', encoding='utf-8') as g:
    for text, rel in zip(test_df['text'].tolist(), test_df['tag'].tolist()):
        g.write(str(rel)+' '+text+'\n')




