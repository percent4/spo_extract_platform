# -*- coding: utf-8 -*-

import os.path
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
from tornado.options import define, options

#定义端口为9000
define("port", default=9000, help="run on the given port", type=int)

import os
import pickle
import tensorflow as tf
from utils import create_model, get_logger
from model import Model
from loader import input_from_line
from train import FLAGS, load_config

def extract(event):
    tf.reset_default_graph()
    config = load_config(FLAGS.config_file)
    logger = get_logger(FLAGS.log_file)
    # limit GPU memory
    tf_config = tf.ConfigProto()
    tf_config.gpu_options.allow_growth = True
    with open(FLAGS.map_file, "rb") as f:
        tag_to_id, id_to_tag = pickle.load(f)
    with tf.Session(config=tf_config) as sess:
        model = create_model(sess, Model, FLAGS.ckpt_path, config, logger)
        result = model.evaluate_line(sess, input_from_line(event, FLAGS.max_seq_len, tag_to_id), id_to_tag)

    return result['entities']

# GET请求
class QueryHandler(tornado.web.RequestHandler):
    # get函数
    def get(self):
        self.render('index.html')

# POST请求
# POST请求参数：query_string
class PostHandler(tornado.web.RequestHandler):

    # post函数
    def post(self):

        # 前端展示
        event = self.get_argument('event')
        result = extract(event)

        print(result)
        time = ''
        title = ''
        obj = ''
        keyword = ''
        subj = ''
        for item in result:
            if item['type'] == 'TIME':
                if item['word'] not in time:
                    time += item['word']+'，'
            if item['type'] == 'TITLE':
                if item['word'] not in title:
                    title += item['word']+'，'
            if item['type'] == 'OBJ':
                if item['word'] not in obj:
                    obj += item['word']+'，'
            if item['type'] == 'KEYWORD':
                if item['word'] not in keyword:
                    keyword = item['word']+'，'
            if item['type'] == 'SUBJ':
                if item['word'] not in subj:
                    subj += item['word']+'，'

        print(time, title, obj, keyword, subj)
        self.render('event_extraction_result.html', event=event, time=time, title=title, obj=obj, subj=subj, keyword=keyword)


# 主函数
def main():
    # 开启tornado服务
    tornado.options.parse_command_line()
    # 定义app
    app = tornado.web.Application(
            handlers=[(r'/query', QueryHandler),
                      (r'/result', PostHandler)
                      ], #网页路径控制
            template_path=os.path.join(os.path.dirname(__file__), "templates") # 模板路径
          )
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()

main()