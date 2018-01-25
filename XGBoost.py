import pandas as pd
from xgboost.sklearn import XGBClassifier
import numpy as np
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import KFold

clf = XGBClassifier(
                learning_rate=0.02, n_estimators=400, max_depth=7, min_child_weight=1.5,
                gamma=0.3, subsample=0.8, colsample_bytree=0.8, objective='binary:logistic',
                n_jobs=-1, scale_pos_weight=1, max_delta_step=5, silent=False,num_class=3 )
fold_num = 5
df = pd.read_csv('test.csv')
df.fillna(-1)
data_array = df.values[:,1:]

kf = KFold(n_splits=fold_num)
count = 0
aucs = []
for train_index, test_index in kf.split(data_array):
    print "count = %d" % count
    count += 1
    clf.fit(data_array[list(train_index), :-1], data_array[list(train_index), -1])
    predict = clf.predict_proba(data_array[list(test_index), :-1])[:, 1]
    auc = roc_auc_score(data_array[list(test_index), -1], predict)
    aucs.append(auc)
    print "AUC is ", auc
print "avg auc",sum(aucs)/fold_num