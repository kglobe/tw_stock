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
from sklearn import linear_model
from sklearn import svm
from sklearn.model_selection import GridSearchCV
from sklearn.externals import joblib

def getData(label_column):
    rows = np.loadtxt("dong_yang.csv", dtype=np.str, delimiter=",", skiprows=1)
    data = np.delete(np.array(rows),label_column,1)
    label = np.array(rows)[:,label_column]
    data = data.astype(float)
    label = label.astype(float)
    return data,label

def svc_param_selection(X, y, nfolds):
    Cs = [0.001, 0.01, 0.1, 1, 10, 100, 1000]
    gammas = [0.0001, 0.001, 0.01, 0.1, 1]
    coef0 = [0.0,0.1,0.5,1.0]
    degree = [3,4,5,6,7,8]
    param_grid = {'C': Cs, 'gamma' : gammas, 'coef0':coef0,'degree':degree}
    grid_search = GridSearchCV(svm.SVR(), param_grid, cv=nfolds)
    grid_search.fit(X, y)
    grid_search.best_params_
    return grid_search.best_params_

data,label = getData(1)
#X_train, X_test, y_train, y_test = train_test_split(data, label, test_size=0.2)
print("data:"+str(data.shape))
print("label:"+str(label.shape))

clf = svm.NuSVR(C=0.1, coef0=0.0, degree=3, gamma=1)
clf.fit(data, label)
#joblib.dump(clf, "model_data/svm_num_model.pkl")

# The mean squared error
mse = np.mean((clf.predict(data) - label) ** 2)
mse_sqrt = np.sqrt(mse)
print("Mean squared error: %.2f" % mse)
print("Mean squared error sqrt: %.2f" % mse_sqrt)
# Explained variance score: 1 is perfect prediction
print('Variance score: %.2f' % clf.score(data, label))

accept_scope=3
predRegression = clf.predict(data)
valiResult = np.absolute(predRegression - label)
in_scope_index = np.where(valiResult<=accept_scope)[0]
out_scope_index = np.where(valiResult>accept_scope)[0]
print("命中區間內的數量: %s" % len(in_scope_index))
print(len(in_scope_index)/len(label))
test = [7]
testArray = []
testArray.append(test)
predNew = clf.predict(np.array(testArray))
print("預測值： %.2f" % predNew)
upper = predNew[0]+mse_sqrt
print("上限： %.2f" % upper)
lower = predNew[0]-mse_sqrt
print("下限： %.2f" % lower)