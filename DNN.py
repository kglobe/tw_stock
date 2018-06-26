# -*- coding: utf-8 -*-
"""
Created on Fri Jun  8 15:45:48 2018

@author: I26436
"""

# -*- coding: utf-8 -*-
"""
Created on Tue May 29 16:23:09 2018

@author: I26436
"""
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.externals import joblib
import tflearn
import tensorflow as tf
tf.reset_default_graph()

def getData(label_column):
    rows = np.loadtxt("dong_yang.csv", dtype=np.str, delimiter=",", skiprows=1)
    data = np.delete(np.array(rows),label_column,1)
    label = np.array(rows)[:,label_column]
    data = data.astype(float)
    label = label.astype(float)
    return data,label

data,label = getData(1)
#X_train, X_test, y_train, y_test = train_test_split(data, label, test_size=0.2)
print("data:"+str(data.shape))
print("label:"+str(label.shape))

net = tflearn.input_data(shape=[None, data.shape[1]], name='input')
net = tflearn.single_unit(net)
#net = tflearn.layers.normalization.batch_normalization(net)
#net = tflearn.fully_connected(net, 3,name='dense1', activation='linear',regularizer='L2', weight_decay=0.001)
#net = tflearn.fully_connected(net, 512, name='dense2', activation='linear',regularizer='L2', weight_decay=0.001)
#net = tflearn.fully_connected(net, 1024, name='dense3', activation='linear',regularizer='L2', weight_decay=0.001)
#net = tflearn.fully_connected(net, 2048, name='dense4', activation='relu',regularizer='L2', weight_decay=0.001)
#net = tflearn.fully_connected(net, 512, name='dense5', activation='linear',regularizer='L2', weight_decay=0.001)
#net = tflearn.fully_connected(net, 128, name='dense6', activation='linear',regularizer='L2', weight_decay=0.001)
#net = tflearn.fully_connected(net, 1, activation='linear')
net = tflearn.regression(net,optimizer='SGD', learning_rate=0.01,metric='R2',loss='mean_square',)

model = tflearn.DNN(net,tensorboard_verbose=3)
model.fit(data, label, n_epoch=1500, show_metric=True)

test = [7]
testArray = []
testArray.append(test)
predict = model.predict(data)
# The mean squared error
mse = np.mean((predict - label) ** 2)
mse_sqrt = np.sqrt(mse)
print("Mean squared error: %.2f" % mse)
print("Mean squared error sqrt: %.2f" % mse_sqrt)

accept_scope=3
predRegression = predict
valiResult = np.absolute(predRegression - label)
in_scope_index = np.where(valiResult<=accept_scope)[0]
out_scope_index = np.where(valiResult>accept_scope)[0]
print("命中區間內的數量: %s" % len(in_scope_index))
print(len(in_scope_index)/len(label))
test = [7]
testArray = []
testArray.append(test)
predNew = model.predict(np.array(testArray))
print("預測值： %.2f" % predNew)
upper = predNew[0]+mse_sqrt
print("上限： %.2f" % upper)
lower = predNew[0]-mse_sqrt
print("下限： %.2f" % lower)