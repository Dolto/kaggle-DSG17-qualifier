import os

import pandas as pd
from sklearn import model_selection
from sklearn import pipeline
from sklearn.externals import joblib
import xam
import lightgbm as lgbm


# Load data
X_train = pd.read_csv('data/X_train.csv')
y_train = pd.read_csv('data/y_train.csv')['is_listened']

# Create a validation set with 20% of the training set
X_train, X_val, y_train, y_val = model_selection.train_test_split(X_train, y_train, test_size=0.1)

pipe = pipeline.Pipeline([
    ('gbm', lgbm.LGBMClassifier(
        num_leaves=2 ** 5,
        learning_rate=0.007,
        n_estimators=10000,
        colsample_bytree=0.8,
        subsample=0.8,
        scale_pos_weight=sum(y_train == 0) / sum(y_train == 1),
    ))
])

pipe.fit(
    X_train,
    y_train,
    gbm__eval_set=[(X_train, y_train), (X_val, y_val)],
    gbm__eval_metric=['auc'],
    gbm__early_stopping_rounds=20,
    gbm__verbose=True
)

directory = os.path.dirname(os.path.realpath(__file__))
joblib.dump(pipe, os.path.join(directory, 'pipeline.pkl'))
