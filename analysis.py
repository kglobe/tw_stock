# -*- coding: utf-8 -*-
"""
Created on 2019/03/06
 
@author: I26436
"""
import os
import pandas as pd
import numpy as np
import datetime
from sklearn.model_selection import train_test_split
import pandas_profiling
from sklearn.model_selection import cross_val_score
from sklearn.metrics import mean_squared_error
from sklearn.metrics import mean_absolute_error
from sklearn.metrics import accuracy_score
from sklearn.metrics import r2_score
from xgboost.sklearn import XGBRegressor
from sklearn.svm import SVR as skSVR
from sklearn import preprocessing
from sklearn import ensemble
import lightgbm as lgb
from sklearn.model_selection import GridSearchCV
import matplotlib.pylab as plt
import joblib
 
def getData():
   host = 'localhost'
   port = '5432'
   databaseName = 'passbda'
   username = 'postgres'
   password = ''
  
   column_names = []
   label_name = []
   try:
       conn = psycopg2.connect(host=host, port=port, dbname=databaseName, user=username, password=password)
       cur = conn.cursor()
      
       query_sql = "select out_ratio,COIL_NO_ICWK ,MTRL_COIL_NO_ICWK ,IS_CUT_ICWK ,COIL_WGT_IN_ICWK ,ORD_ITEM_ICWK ,ORD_THK_ICWK ,MIC_NO_ICWK ,MIC_LINE_NO_ICWK ,BACKLOG_CODE_ICWK ,PSR_NO_ICWK ,APN_CODE_ICWK ,STEEL_GRADE_4_ICWK ,QLTY_CODE_ICWK ,INSP_CODE_ICWK ,ROUGH_CODE_ICWK ,SPEC_N_ICWK ,CUST_NO_ICWK ,LAST_MILL_ICWK ,COIL_THK_IN_ICWK ,COIL_WDH_IN_ICWK ,INSP_DISP_ICWK ,SIDE_TRIM_ICWK ,HARNESS_ICWK ,IS_HFP_ICWK from db.W7Data20190730 Where substring(MIC_NO_ICWK,1,1)='4' and substring(MIC_NO_ICWK,1,2)<>'47'"
       cur.execute(query_sql)
       rows = cur.fetchall()
      
       if len(rows)==0:
           raise Exception('沒有訓練資料，無法進行模型分析!!!請查看取資料的條件')
 
       for idx,desc in enumerate(cur.description):
           if(idx==0):
               label_name.append(desc[0])
           else:
               column_names.append(desc[0])
      
       label = np.array(rows)[:,0]
       data = np.delete(np.array(rows),0,1)
       data = pd.DataFrame(data, columns=np.asarray(column_names))
       label = pd.DataFrame(label, columns=np.asarray(label_name))
       return data,label
   except psycopg2.OperationalError as e:
       conn.close()
       raise e
   except Exception as e:
       conn.close()
       raise e
   finally:
       try:
           conn.close()
       except Exception as e:
           print(str(e))
  
def setLabelEncode(inputData):
   le = preprocessing.LabelEncoder()
   le.fit(inputData)
   return le.transform(inputData), le
 
def custom_asymmetric_objective(y_true, y_pred):
   residual = (y_true - y_pred).astype("float")
   grad = np.where(residual<0, -2*10.0*residual, -2)
   hess = np.where(residual<0, 2*10.0, 0)
   return grad, hess
 
def mining():
   resultDir = 'out_ratio_Result'
   if os.path.exists(resultDir)==False:
       os.makedirs(resultDir)
   data,label = getData()
   coil_no_icwk, coil_no_icwk_le = setLabelEncode(data['coil_no_icwk'].astype('category'))
   data['coil_no_icwk'] = coil_no_icwk
 
   mtrl_coil_no_icwk, mtrl_coil_no_icwk_le = setLabelEncode(data['mtrl_coil_no_icwk'].astype('category'))
   data['mtrl_coil_no_icwk'] = mtrl_coil_no_icwk
 
   is_cut_icwk, is_cut_icwk_le = setLabelEncode(data['is_cut_icwk'].astype('category'))
   data['is_cut_icwk'] = is_cut_icwk
 
   ord_item_icwk, ord_item_icwk_le = setLabelEncode(data['ord_item_icwk'].astype('category'))
   data['ord_item_icwk'] = ord_item_icwk
 
   data['ord_thk_icwk'] = data['ord_thk_icwk'].astype(float)
 
   # data['ord_wth_icwk'] = data['ord_wth_icwk'].astype(float)
 
   mic_no_icwk, mic_no_icwk_le = setLabelEncode(data['mic_no_icwk'].astype('category'))
   data['mic_no_icwk'] = mic_no_icwk
 
   mic_line_no_icwk, mic_line_no_icwk_le = setLabelEncode(data['mic_line_no_icwk'].astype('category'))
   data['mic_line_no_icwk'] = mic_line_no_icwk
 
   backlog_code_icwk, backlog_code_icwk_le = setLabelEncode(data['backlog_code_icwk'].astype('category'))
   data['backlog_code_icwk'] = backlog_code_icwk
 
   psr_no_icwk, psr_no_icwk_le = setLabelEncode(data['psr_no_icwk'].astype('category'))
   data['psr_no_icwk'] = psr_no_icwk
 
   apn_code_icwk, apn_code_icwk_le = setLabelEncode(data['apn_code_icwk'].astype('category'))
   data['apn_code_icwk'] = apn_code_icwk
 
   steel_grade_4_icwk, steel_grade_4_icwk_le = setLabelEncode(data['steel_grade_4_icwk'].astype('category'))
   data['steel_grade_4_icwk'] = steel_grade_4_icwk
 
   qlty_code_icwk, qlty_code_icwk_le = setLabelEncode(data['qlty_code_icwk'].astype('category'))
   data['qlty_code_icwk'] = qlty_code_icwk
 
   insp_code_icwk, insp_code_icwk_le = setLabelEncode(data['insp_code_icwk'].astype('category'))
   data['insp_code_icwk'] = insp_code_icwk
 
   rough_code_icwk, rough_code_icwk_le = setLabelEncode(data['rough_code_icwk'].astype('category'))
   data['rough_code_icwk'] = rough_code_icwk
 
   spec_n_icwk, spec_n_icwk_le = setLabelEncode(data['spec_n_icwk'].astype('category'))
   data['spec_n_icwk'] = spec_n_icwk
 
   cust_no_icwk, cust_no_icwk_le = setLabelEncode(data['cust_no_icwk'].astype('category'))
   data['cust_no_icwk'] = cust_no_icwk
  
   # data['prod_date_icwk'] = setLabelEncode(data['prod_date_icwk'].astype('category'))
 
   last_mill_icwk, last_mill_icwk_le = setLabelEncode(data['last_mill_icwk'].astype('category'))
   data['last_mill_icwk'] = last_mill_icwk
 
   data['coil_thk_in_icwk'] = data['coil_thk_in_icwk'].astype(float)
   data['coil_wdh_in_icwk'] = data['coil_wdh_in_icwk'].astype(float)
 
   insp_disp_icwk, insp_disp_icwk_le = setLabelEncode(data['insp_disp_icwk'].astype('category'))
   data['insp_disp_icwk'] = insp_disp_icwk
 
   # data['insp_disp_date_icwk'] = setLabelEncode(data['insp_disp_date_icwk'].astype('category'))
  
   side_trim_icwk, side_trim_icwk_le = setLabelEncode(data['side_trim_icwk'].astype('category'))
   data['side_trim_icwk'] = side_trim_icwk
 
   harness_icwk, harness_icwk_le = setLabelEncode(data['harness_icwk'].astype('category'))
   data['harness_icwk'] = harness_icwk
 
   is_hfp_icwk, is_hfp_icwk_le = setLabelEncode(data['is_hfp_icwk'].astype('category'))
   data['is_hfp_icwk'] = is_hfp_icwk
 
   data['coil_wgt_in_icwk'] = data['coil_wgt_in_icwk'].astype(float)
   label['out_ratio'] = label['out_ratio'].astype(float)
   print(data.describe())
 
   # report = pandas_profiling.ProfileReport(data)
   # report.to_file("report.html")
 
   x_train, x_test, y_train, y_test = train_test_split(data, label, train_size=(int(80)/100),random_state=8)
 
   estimator = lgb.LGBMRegressor(max_depth=10,metric='l2_root',bagging_fraction = 0.8,feature_fraction = 0.8)
   param_grid = {
       'objective':['huber','regression_l2'],
       'learning_rate': [0.05, 0.1],
       'num_leaves': [100,200,500],
       'n_estimators': [50, 100, 200,500]
   }
   gbm = GridSearchCV(estimator, param_grid)
   gbm.fit(x_train, y_train,eval_set=[(x_test, y_test)])
   print('Best parameters found by grid search are:', gbm.best_params_)
 
   updatedate = datetime.datetime.now().strftime('%Y%m%d')
   updatetime = datetime.datetime.now().strftime('%H%M%S')
   with open(resultDir+'/Tune_result_'+updatedate+'_'+updatetime+'.txt', "w", newline="") as txt_file:
       txt_file.write('Best parameters:'+str(gbm.best_params_)+'\n')
   return
 
def main():
   mining()
  
if __name__ == "__main__":
   main()