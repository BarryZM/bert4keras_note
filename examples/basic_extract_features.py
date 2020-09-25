#! -*- coding: utf-8 -*-
# 测试代码可用性: 提取特征

from bert4keras.backend import keras
from bert4keras.models import build_transformer_model
from bert4keras.tokenizers import Tokenizer
from bert4keras.snippets import to_array
import numpy as np

# 自行下载Bert预训练模型，将三个文件改成自己下载好之后所在的路径，比如我的就是如下路径
config_path = 'D:/DP/config/chinese_L-12_H-768_A-12/bert_config.json'
checkpoint_path = 'D:/DP/config/chinese_L-12_H-768_A-12/bert_model.ckpt'
dict_path = 'D:/DP/config/chinese_L-12_H-768_A-12/vocab.txt'

# 建立分词器，包括转成bert输入的形式，字转id等功能
tokenizer = Tokenizer(dict_path, do_lower_case=True)  # 建立分词器
# 主函数，想了解原理可以看bert4keras源码，可以看我对源码的注释ZJJDJJ/bert4keras_note/bert4keras_explain
model = build_transformer_model(config_path, checkpoint_path)  # 建立模型，加载权重

# 编码测试
# token_ids: [101, 6427, 6241, 3563, 1798, 102]
# segment_ids: [0, 0, 0, 0, 0, 0]
token_ids, segment_ids = tokenizer.encode(u'语言模型')

# 因为最终输进model.predict的token_ids shape=(btz,seq_len),所以提前在这加入btz维度，因为只有一句话，也就是1维
# token_ids: [[ 101 6427 6241 3563 1798  102]]
# segment_ids: [[0 0 0 0 0 0]]
token_ids, segment_ids = to_array([token_ids], [segment_ids])

print('\n ===== predicting =====\n')
print(model.predict([token_ids, segment_ids])) # 在token_ids和segment_ids都是shape=(btz,seq_len)基础上，用list把两个合在一起。
"""
输出：shape=(btz,seq_len,768)，也就是(1,6,768)
[[[-0.63251007  0.2030236   0.07936534 ...  0.49122632 -0.20493352
    0.2575253 ]
  [-0.7588351   0.09651865  1.0718756  ... -0.6109694   0.04312154
    0.03881441]
  [ 0.5477043  -0.792117    0.44435206 ...  0.42449304  0.41105673
    0.08222899]
  [-0.2924238   0.6052722   0.49968526 ...  0.8604137  -0.6533166
    0.5369075 ]
  [-0.7473459   0.49431565  0.7185162  ...  0.3848612  -0.74090636
    0.39056838]
  [-0.8741375  -0.21650358  1.338839   ...  0.5816864  -0.4373226
    0.56181806]]]
"""

print('\n ===== reloading and predicting =====\n')
model.save('test.model')
del model
model = keras.models.load_model('test.model')
print(model.predict([token_ids, segment_ids])) # 同上 