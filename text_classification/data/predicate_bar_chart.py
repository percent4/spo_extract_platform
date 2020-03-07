# -*- coding: utf-8 -*-
# author: Jclian91
# place: Pudong Shanghai
# time: 2020-02-27 11:51

import pandas as pd
import matplotlib.pyplot as plt

# 显示所有列
pd.set_option('display.max_columns', None)

# 读取EXCEL数据
df = pd.read_excel('spo.xlsx')
label_list = list(df[df.tag == 1]['p'].value_counts().index)[:20]
num_list = df[df.tag == 1]['p'].value_counts().tolist()[:20]

print("关系数量: %d" % len(df['p'].unique()))
print("所有关系: %s" % df['p'].unique())
print(df[df.tag == 1].head())

# Mac系统设置中文字体支持
plt.rcParams["font.family"] = 'Arial Unicode MS'

# 利用Matplotlib模块绘制条形图
x = range(len(num_list))
rects = plt.bar(left=x, height=num_list, width=0.6, color='blue', label="频数")
plt.ylim(0, 150)    # y轴范围
plt.ylabel("数量")
plt.xticks([index + 0.1 for index in x], label_list)
plt.xticks(rotation=45)  # x轴的标签旋转45度
plt.xlabel("人物关系")
plt.title("人物关系频数统计")
plt.legend()

# 条形图的文字说明
for rect in rects:
    height = rect.get_height()
    plt.text(rect.get_x() + rect.get_width() / 2, height+1, str(height), ha="center", va="bottom")

# plt.show()
plt.savefig('./predicate_val_count.png')

