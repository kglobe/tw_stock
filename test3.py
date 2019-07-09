import requests
import datetime
import sys
import pandas as pd
from sklearn.svm import SVR
import xgboost as xgb
from sklearn.metrics import mean_squared_error
import numpy as np

rawData = pd.read_csv("1402_train.csv")
# cols = rawData.columns
# rawData[cols] = rawData[cols].apply(pd.to_numeric, errors='coerce')
target = rawData['Close']
train = rawData.drop(['Close'], axis=1)
# clf = SVR(gamma=0.001, C=1.0, epsilon=0.2)
# model = clf.fit(train, target)
# predict = model.predict(train)
xg_reg = xgb.XGBRegressor(objective ='reg:linear', colsample_bytree = 0.5, learning_rate = 0.8,
                max_depth = 50, alpha = 5, n_estimators = 50)
xg_reg.fit(train,target)
predict = xg_reg.predict(train)
rmse = np.sqrt(mean_squared_error(target, predict))
# print(predict)
print("RMSE: %f" % (rmse))
predInput = pd.read_csv('1402_pred.csv')
pred = xg_reg.predict(predInput)
print(pred)
# with open('9904_predict.csv', 'w') as f:
#     f.writelines(predict)