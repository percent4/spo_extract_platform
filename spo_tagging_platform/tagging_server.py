# -*- coding: utf-8 -*-
# author: Jclian91
# place: Pudong Shanghai
# time: 2020-02-25 20:27

import json
import requests
import os.path
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
from tornado.options import define, options
from utils import get_max_num

# 定义端口为9009
define("port", default=9009, help="run on the given port", type=int)


# Handler
class QueryHandler(tornado.web.RequestHandler):

    # get函数
    def get(self):
        self.render('index.html')

    # post函数
    def post(self):

        # 获取前端参数
        text = self.get_argument("event").replace(' ', '')
        subjs = self.get_argument("subject").split('#')
        preds = self.get_argument("pred").split('#')
        objs = self.get_argument("obj").split('#')

        print("subjs: %s" % subjs)
        print("preds: %s" % preds)
        print("objs: %s" % objs)

        # 前端显示序列标注信息
        tags = ['O'] * len(text)

        # 主语TAG
        for subj in subjs:
            t = len(subj)
            for i in range(0, len(text)-t+1):
                if text[i:i+t] == subj:
                    tags[i] = 'B-SUBJ'
                    for j in range(1, t):
                        tags[i+j] = 'I-SUBJ'

        # 谓语TAG
        for pred in preds:
            t = len(pred)
            for i in range(0, len(text)-t+1):
                if text[i:i + t] == pred:
                    tags[i] = 'B-PRED'
                    for j in range(1, t):
                        tags[i + j] = 'I-PRED'

        # 宾语TAG
        for obj in objs:
            t = len(obj)
            for i in range(0, len(text)-t+1):
                if text[i: i+t] == obj:
                    tags[i] = 'B-OBJ'
                    for j in range(1, t):
                        tags[i + j] = 'I-OBJ'

        # 保存为txt文件
        dir_path = 'tagging_output'
        with open('./%s/%s.txt' % (dir_path, get_max_num(dir_path)+1), 'w', encoding='utf-8') as f:
            for char, tag in zip(text, tags):
                f.write(char+'\t'+tag+'\n')

        # 保存spo三元组
        spos = self.get_argument("spo").split('\r\n')
        print(spos)

        dir_path = 'relation_output'
        with open('./%s/%s.txt' % (dir_path, get_max_num(dir_path) + 1), 'w', encoding='utf-8') as g:
            for spo in spos:
                g.write(spo + '#' + text + '\n')

        self.render('index.html')


# 预测页面
class PredictHandler(tornado.web.RequestHandler):

    def get(self, *args, **kwargs):

        # 读取sent.txt文件中的第一句作为预测结果展示

        with open("../sent.txt", "r", encoding="utf-8") as f:
            content = [_.strip().replace(' ', '') for _ in f.readlines()]

        sent = content[0]

        # 获取S，P，O以及三元组
        result_dict = json.loads(requests.post("http://localhost:12306/subj_extract", {"event": sent}).content)
        subjs = result_dict["subjs"]
        preds = result_dict["preds"]
        objs = result_dict["objs"]

        spo_list = [[subj, pred, obj, '0']
                    for subj in subjs
                    for pred in preds
                    for obj in objs
                    ]

        # 获取spo三元组结果，修改spo_list中的标签0为1
        relations = json.loads(requests.post("http://localhost:12308/spo_extract", {"text": sent}).content)

        for relation in relations:
            s, p, o = relation["subject"], relation["predicate"], relation["object"]
            # print(s, p, o)
            for i in range(len(spo_list)):
                if s == spo_list[i][0] and p == spo_list[i][1] and o == spo_list[i][2]:
                    spo_list[i][-1] = '1'

        self.render('predict.html',
                    sent=sent,
                    subjs='#'.join(subjs),
                    preds='#'.join(preds),
                    objs='#'.join(objs),
                    spos='\r\n'.join(['#'.join(_) for _ in spo_list])
                    )

    def post(self):

        # 获取前端参数
        text = self.get_argument("event").replace(' ', '')
        subjs = self.get_argument("subject").split('#')
        preds = self.get_argument("pred").split('#')
        objs = self.get_argument("obj").split('#')

        print("subjs: %s" % subjs)
        print("preds: %s" % preds)
        print("objs: %s" % objs)

        # 前端显示序列标注信息
        tags = ['O'] * len(text)

        # 主语TAG
        for subj in subjs:
            t = len(subj)
            for i in range(0, len(text) - t + 1):
                if text[i:i + t] == subj:
                    tags[i] = 'B-SUBJ'
                    for j in range(1, t):
                        tags[i + j] = 'I-SUBJ'

        # 谓语TAG
        for pred in preds:
            t = len(pred)
            for i in range(0, len(text) - t + 1):
                if text[i:i + t] == pred:
                    tags[i] = 'B-PRED'
                    for j in range(1, t):
                        tags[i + j] = 'I-PRED'

        # 宾语TAG
        for obj in objs:
            t = len(obj)
            for i in range(0, len(text) - t + 1):
                if text[i: i + t] == obj:
                    tags[i] = 'B-OBJ'
                    for j in range(1, t):
                        tags[i + j] = 'I-OBJ'

        # 保存为txt文件
        dir_path = 'tagging_output'
        with open('./%s/%s.txt' % (dir_path, get_max_num(dir_path) + 1), 'w', encoding='utf-8') as f:
            for char, tag in zip(text, tags):
                f.write(char + '\t' + tag + '\n')

        # 保存spo三元组
        spos = self.get_argument("spo").split('\r\n')
        print(spos)

        dir_path = 'relation_output'
        with open('./%s/%s.txt' % (dir_path, get_max_num(dir_path) + 1), 'w', encoding='utf-8') as g:
            for spo in spos:
                g.write(spo + '#' + text + '\n')

        with open("../sent.txt", "r", encoding="utf-8") as f:
            content = [_.strip().replace(' ', '') for _ in f.readlines()]

        content.remove(content[0])

        with open("../sent.txt", "w", encoding="utf-8") as g:
            for line in content:
                g.write(line+'\n')

        self.get()


# 主函数
def main():
    # 开启tornado服务
    tornado.options.parse_command_line()
    # 定义app
    app = tornado.web.Application(
            handlers=[(r'/query', QueryHandler),
                      (r'/predict', PredictHandler)
                      ], #网页路径控制
            template_path=os.path.join(os.path.dirname(__file__), "templates")  # 模板路径
          )
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()

main()