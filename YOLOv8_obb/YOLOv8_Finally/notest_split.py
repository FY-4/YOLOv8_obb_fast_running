import os
import random

# 设置参数
train_percent = 0.95  # 训练集占总数据集的比例
xmlfilepath = 'my_data_1/Annotations'
txtsavepath = 'my_data_1/ImageSets'
total_xml = os.listdir(xmlfilepath)

num = len(total_xml)
list_index = range(num)
tv = int(num * train_percent)  # 只有训练集和验证集
train_index = random.sample(list_index, tv)

if not os.path.exists(txtsavepath):
    os.makedirs(txtsavepath)

ftrain = open(os.path.join(txtsavepath, 'train.txt'), 'w')
fval = open(os.path.join(txtsavepath, 'val.txt'), 'w')

for i in list_index:
    name = total_xml[i][:-4] + '\n'
    if i in train_index:
        ftrain.write(name)
    else:
        fval.write(name)

ftrain.close()
fval.close()