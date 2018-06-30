# 使用人工神经网络实现手写体数字识别
# 数据的读取与整理
# 加载数据
from numpy import *
import operator
from os import listdir
import numpy as npy
import pandas as pda
import numpy
from keras.models import Sequential
from keras.layers.core import Dense,Activation


def datatoarray(fname):
    arr = []
    fh = open(fname)
    for i in range(0, 32):
        thisline = fh.readline()
        for j in range(0, 32):
            arr.append(int(thisline[j]))
    return arr


# 建立一个函数取文件名前缀
def seplabel(fname):
    filestr = fname.split(".")[0]
    label = int(filestr.split("_")[0])
    return label


# 建立训练数据
def traindata():
    labels = []
    trainfile = listdir("D:/13.NerveNet/traindata")
    num = len(trainfile)
    # 长度1024（列），每一行存储一个文件
    # 用一个数组存储所有训练数据，行：文件总数，列：1024
    trainarr=zeros((num, 1024))
    for i in range(0, num):
        thisfname = trainfile[i]
        thislabel = seplabel(thisfname)
        labels.append(thislabel)
        trainarr[i, :] = datatoarray("D:/13.NerveNet/traindata/"+thisfname)
    return trainarr, labels
trainarr, labels = traindata()

# 数据类型和存储格式的转换
xf = pda.DataFrame(trainarr)
yf = pda.DataFrame(labels)
tx2 = xf.as_matrix().astype(int)
ty2 = yf.as_matrix().astype(int)

# 使用人工神经网络模型
model = Sequential()
# 输入层
model.add(Dense(10, input_dim=1024))
model.add(Activation("relu"))
# 输出层
model.add(Dense(1, input_dim=1))
model.add(Activation("sigmoid"))
# 模型的编译
model.compile(loss="mean_squared_error", optimizer="adam")
# 训练
model.fit(tx2, ty2, nb_epoch=10000, batch_size=6)
# 预测分类
rst = model.predict_classes(tx2).reshape(len(tx2))
x = 0
for i in range(0, len(tx2)):
    if rst[i] != ty2[i]:
        x += 1
print(1-x/len(tx2))
