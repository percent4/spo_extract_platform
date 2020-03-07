# -*- coding: utf-8 -*-
# author: Jclian91
# place: Pudong Shanghai
# time: 2020-02-29 11:19

import pandas as pd
from py2neo import Graph, Node, Relationship, NodeMatcher

# 读取Excel文件
df = pd.read_excel('./excels/santi.xlsx')

# 取前610行作为图谱数据
# df = df.iloc[:706, :]

# 连接Neo4j服务
graph = Graph(host="localhost://7474", auth=("neo4j", "jc147369"))

# 创建节点
nodes = set(df['S'].tolist()+df['O'].tolist())
for node in nodes:
    node = Node("Node", name=node)
    graph.create(node)

print('create nodes successfully!')

# 创建关系
matcher = NodeMatcher(graph)
for i in range(df.shape[0]):
    S = df.iloc[i, :]['S']  # S节点
    O = df.iloc[i, :]['O']  # O节点
    s_node = matcher.match("Node", name=S).first()
    o_node = matcher.match("Node", name=O).first()

    # 创建关系
    P = df.iloc[i, :]['P']
    relationship = Relationship(s_node, P, o_node)
    graph.create(relationship)

print('create relationships successfully!')
print('You can check Neo4j now!')