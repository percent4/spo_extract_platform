# 开放领域的关系抽取的一次尝试

### 平台组成

1. 标注平台（前端网页），对应目录`spo_tagging_platform`；
2. 标注内容： S,P,O, is_tagging, 原文以及SPO的关系。
3. 模型：

- S,P,O: 序列标注算法（ALBERT+BiLSTM+CRF），对应目录`sequence_labeling`，在测试集上的F1大约为81%；
- 关系抽取: 文本二分类(ALBERT+BiGRU+ATT)，对应目录`text_classification`，在测试集上的准确率大约为96%。

标注语料来源于新闻内容和小说内容。

4. 该项目在提取小说、新闻以及其他无结构文本方面的应用，对应目录为`extract_example`。

### 数据介绍

&emsp;&emsp;现阶段的序列标注算法的样本为3211个，关系抽取的标注数据为9279，共有关系1365个，数量最多的前20个关系如下图：

![](https://github.com/percent4/spo_extract_platform/blob/master/text_classification/data/predicate_val_count.png)


### 平台使用前的准备工作

- 该平台采用Python3开发，需要安装的模块参考requirements.txt


### 如何使用该平台？

`序列标注算法`和`文本二分类`已经训练好，可以直接clone下来使用。

1. 运行`sequence_labeling/run.py`，该HTTP服务运行端口为12306；

2. 运行`text_classification/extract_server.py`，该HTTP服务运行端口为12308；

在Postman中输入如下（输入为一个句子，句子不宜过长，建议句子长度不超过128个字）：

![](https://github.com/percent4/spo_extract_platform/blob/master/extract_example/example1.png)

![](https://github.com/percent4/spo_extract_platform/blob/master/extract_example/example2.png)

![](https://github.com/percent4/spo_extract_platform/blob/master/extract_example/example3.png)

### 平台效果

&emsp;&emsp;该平台标注的时候，标注内容大部分为人物头衔，人物关系，公司与人的关系，影视剧主演、导演信息等。

&emsp;&emsp;当句子有只有一对三元组的时候，效果相对较好。

&emsp;&emsp;`extract_example`目录中为抽取的效果，包括几本小说和一些新闻上的效果，关于这方面的演示，可以参考另一个项目：[https://github.com/percent4/knowledge_graph_demo](https://github.com/percent4/knowledge_graph_demo) 。

&emsp;&emsp;一些句子也存在抽取出无用的三元组的情况，导致召回率偏高，这是因为本项目针对的是开放领域的三元组抽取，因此效果比不会有想象中的那么好，提升抽取效果的办法如下：

- 增加数据标注量，目前序列标注算法的样本仅3211多个；
- 模型方面：现在是pipeline形式，各自的效果还行，但总体上不如Joint形式好；
- 对于自己想抽的其他三元组的情形，建议增加这方面的标注；
- 文本预测耗时长（该问题已经解决）。

### 交流

&emsp;&emsp;本项目作为笔者在开放领域的三元组抽取的一次尝试，在此之前关于这方面的文章或者项目还很少，因此可以说是探索阶段。

&emsp;&emsp;源码和数据已经在项目中给出。

&emsp;&emsp;如需要更深一步的交流，请发送消息至邮箱`1137061634@qq.com`，或者在Github上直接留言。

&emsp;&emsp;本人的微信公众号为`Python爬虫与算法`，欢迎关注~


