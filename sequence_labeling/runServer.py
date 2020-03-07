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

import tensorflow as tf
from utils import create_model, get_logger
from model import Model
from loader import input_from_line
from train import FLAGS, load_config, train

# tornado高并发
import tornado.web
import tornado.gen
import tornado.concurrent
from concurrent.futures import ThreadPoolExecutor

# 定义端口为12306
define("port", default=12306, help="run on the given port", type=int)

# 导入模型
config = load_config(FLAGS.config_file)
logger = get_logger(FLAGS.log_file)
# limit GPU memory
tf_config = tf.ConfigProto()
tf_config.gpu_options.allow_growth = False
with open(FLAGS.map_file, "rb") as f:
    tag_to_id, id_to_tag = pickle.load(f)

sess = tf.Session(config=tf_config)
model = create_model(sess, Model, FLAGS.ckpt_path, config, logger)


# 测试
class HelloHandler(tornado.web.RequestHandler):
    def get(self):
        self.write('Hello World!')


# 模型训练
class ModelTrainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write('begin training...')
        os.system('python3 train.py')
        self.write('end')


# 模型预测的HTTP接口
class ResultHandler(tornado.web.RequestHandler):

    # post函数
    def post(self):

        event = self.get_argument('event')

        result = model.evaluate_line(sess, input_from_line(event, FLAGS.max_seq_len, tag_to_id), id_to_tag)

        subjs, preds, objs = [], [], []
        for entity in result['entities']:
            if entity['type'] == 'SUBJ' and entity['word'] not in subjs:
                subjs.append(entity['word'])
            if entity['type'] == 'PRED' and entity['word'] not in preds:
                preds.append(entity['word'])
            if entity['type'] == 'OBJ' and entity['word'] not in objs:
                objs.append(entity['word'])

        result_dict = {"subjs": subjs,
                       "objs": objs,
                       "preds": preds}

        self.write(json.dumps(result_dict, ensure_ascii=False))


# 模型预测的HTTP接口
class AsyncResultHandler(tornado.web.RequestHandler):
    executor = ThreadPoolExecutor(max_workers=100)

    # get 函数
    @tornado.gen.coroutine
    # post 函数
    def post(self):
        event = self.get_argument('event')
        result = yield self.function(event)
        self.write(json.dumps(result))
        #self.write(str(round(t2 - t1, 4)))

    @tornado.concurrent.run_on_executor
    def function(self, event):
        result = model.evaluate_line(sess, input_from_line(event, FLAGS.max_seq_len, tag_to_id), id_to_tag)
        return result


# 主函数
def main():
    # 开启tornado服务
    tornado.options.parse_command_line()
    # 定义app
    app = tornado.web.Application(
            handlers=[(r'/model_train', ModelTrainHandler),
                      (r'/subj_extract', ResultHandler),
                      (r'/async_subj_extract', AsyncResultHandler),
                      (r'/hello', HelloHandler),
                     ], #网页路径控制
           )
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()

# main()