# -*- coding: utf-8 -*-
# 模型预测

import os, json
import numpy as np
# from bert.extract_feature import BertVector
from keras.models import load_model
from att import Attention

from albert_zh.extract_feature import BertVector

# 加载训练效果最好的模型
model_dir = './models'
files = os.listdir(model_dir)
models_path = [os.path.join(model_dir, _) for _ in files]
best_model_path = sorted(models_path, key=lambda x: float(x.split('-')[-1].replace('.h5', '')), reverse=True)[0]
print(best_model_path)
model = load_model(best_model_path, custom_objects={"Attention": Attention})

# 示例语句及预处理
text1 = '伊朗卫生部#副部长#哈里奇#外媒称，伊朗卫生部副部长哈里奇确诊感染新型冠状病毒。'
s, p, o, doc = text1.split('#')
text = '#'.join([s, p, o, doc.replace(s, len(s)*'S').replace(p, len(p)*'P').replace(o, len(o)*'O')])
print(text)


# 利用BERT提取句子特征
bert_model = BertVector(pooling_strategy="NONE", max_seq_len=100)
vec = bert_model.encode([text])["encodes"][0]
x_train = np.array([vec])

# 模型预测并输出预测结果
predicted = model.predict(x_train)
y = np.argmax(predicted[0])
print(y)
