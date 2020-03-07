# -*- coding: utf-8 -*-

import os
import json
import time
import pickle
import traceback

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
from tornado.options import define, options

# tornado高并发
import tornado.web
import tornado.gen
import tornado.concurrent

import os, json
import numpy as np
# from bert.extract_feature import BertVector
from keras.models import load_model
from att import Attention
from albert_zh.extract_feature import BertVector


# 定义端口为12308
define("port", default=12308, help="run on the given port", type=int)

albert_model = BertVector(pooling_strategy="NONE", max_seq_len=128)

# 加载训练效果最好的模型
model_dir = './models'
files = os.listdir(model_dir)
models_path = [os.path.join(model_dir, _) for _ in files]
best_model_path = sorted(models_path, key=lambda x: float(x.split('-')[-1].replace('.h5', '')), reverse=True)[0]
classify_model = load_model(best_model_path, custom_objects={"Attention": Attention})


import requests


# 对句子进行编码
class EncodeHandler(tornado.web.RequestHandler):

    # 新增GET请求
    def get(self, *args, **kwargs):
        string = self.get_argument("text").replace(" ", "")

        respon_dict = json.loads(requests.post("http://localhost:12306/subj_extract", {"event": string}).content)

        subjs = respon_dict["subjs"]
        preds = respon_dict["preds"]
        objs = respon_dict["objs"]

        print(respon_dict)
        result_dict = {"原文": string}

        spo_list = []
        if subjs and preds and objs:
            for s in subjs:
                for p in preds:
                    for o in objs:

                        text = '#'.join(
                            [s, p, o,
                             string.replace(s, len(s) * 'S').replace(p, len(p) * 'P').replace(o, len(o) * 'O')])
                        # print(text)

                        # 利用BERT提取句子特征
                        vec = albert_model.encode([text])["encodes"][0]
                        x_train = np.array([vec])

                        # 模型预测并输出预测结果
                        predicted = classify_model.predict(x_train)
                        y = np.argmax(predicted[0])
                        if y:
                            spo_list.append({"subject": s, "predicate": p, "object": o})

        result_dict.update({"抽取结果": spo_list})
        print("请求: ", result_dict)
        self.write(json.dumps(result_dict, ensure_ascii=False, indent=2))

    def post(self):

        string = self.get_argument("text").replace(" ", "")

        result_dict = json.loads(requests.post("http://localhost:12306/subj_extract", {"event": string}).content)

        print(result_dict)
        subjs = result_dict["subjs"]
        preds = result_dict["preds"]
        objs = result_dict["objs"]

        spo_list = []
        if subjs and preds and objs:
            for s in subjs:
                for p in preds:
                    for o in objs:

                        text = '#'.join(
                            [s, p, o, string.replace(s, len(s) * 'S').replace(p, len(p) * 'P').replace(o, len(o) * 'O')])
                        # print(text)

                        # 利用BERT提取句子特征
                        vec = albert_model.encode([text])["encodes"][0]
                        x_train = np.array([vec])

                        # 模型预测并输出预测结果
                        predicted = classify_model.predict(x_train)
                        y = np.argmax(predicted[0])
                        if y:
                            spo_list.append({"subject": s, "predicate": p, "object": o})

        self.write(json.dumps(spo_list, ensure_ascii=False, indent=2))


# 主函数
def main():

    # 开启tornado服务
    tornado.options.parse_command_line()
    # 定义app
    app = tornado.web.Application(
            handlers=[(r'/spo_extract', EncodeHandler)] #网页路径控制
           )
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()

main()