# -*- coding: utf-8 -*-
"""stacked.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1DhvdhPTiHSBmO8vjXBK7qTLCRPHZ_Br8
"""

import pandas as pd
import numpy as np
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
from sklearn.model_selection import GridSearchCV, RepeatedStratifiedKFold
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.model_selection import train_test_split
import seaborn as sns
from matplotlib import pyplot as plt
from matplotlib import style
from numpy import percentile
 
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV, RepeatedStratifiedKFold
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler,RobustScaler
from sklearn.metrics import f1_score, classification_report
from sklearn.impute import SimpleImputer
from sklearn.model_selection import train_test_split
 
# import XGBClassifier
from xgboost import XGBClassifier
 
#importing all the required ML packages
from sklearn.linear_model import LogisticRegression #logistic regression
from sklearn import svm #support vector Machine
from sklearn.ensemble import RandomForestClassifier #Random Forest
from sklearn.neighbors import KNeighborsClassifier #KNN
from sklearn.naive_bayes import GaussianNB #Naive bayes
from sklearn.tree import DecisionTreeClassifier #Decision Tree
from sklearn.model_selection import train_test_split #training and testing data split
from sklearn import metrics #accuracy measure
from sklearn.metrics import confusion_matrix #for confusion matrix
 
from xgboost import cv
 
 
# Classification algorithms
from sklearn.linear_model import LogisticRegression
from sklearn.svm import NuSVC, SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, StackingClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.ensemble import AdaBoostClassifier
# import Support Vector Classifier
from sklearn.svm import SVC
 
# Data preprocessing :
from sklearn.preprocessing import StandardScaler, LabelEncoder, OneHotEncoder,OrdinalEncoder
 
 
# Modeling helper functions
from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV , KFold , cross_val_score
 
 
# Classification metrices
from sklearn.metrics import accuracy_score
 
from sklearn.preprocessing import PowerTransformer
 
from sklearn.svm import SVC

df=pd.read_csv('/content/drive/MyDrive/ddddddd.csv')
df

df['Cath']=df['Cath'].map(lambda x : {'Normal':0 , 'Cad':1}.get(x, 0))
df['Cath']=pd.to_numeric(df['Cath'])
df=df.as_matrix()
X = df.drop('Cath', axis = 1)
y = df.Cath


preprocessor = ColumnTransformer(
    [
        ('onehot', OneHotEncoder(), ['Sex','Obesity','CRF','CVA','Airway disease','Thyroid Disease','CHF','DLP','Weak Peripheral Pulse','Lung rales','Systolic Murmur','Diastolic Murmur','Dyspnea','Atypical','Nonanginal','Exertional CP','LowTH Ang','LVH','Poor R Progression','BBB']),
        ('scaler', RobustScaler(), ['Age','Weight','Length','BMI','BP','FBS','TG','LDL','HDL','BUN','ESR','HB','K','Na','WBC','Lymph','Neut','PLT','EF-TTE']),
        ('ord',OrdinalEncoder(),['VHD']),
        ('power',PowerTransformer(method='box-cox'),['Age','Weight','Length','BMI','BP','FBS','TG','LDL','HDL','BUN','ESR','HB','K','Na','WBC','Lymph','Neut','PLT','EF-TTE'])
    ],
       remainder = 'passthrough'
) 
# transformer for categorical features
categorical_features = ['Sex','Obesity','CRF','CVA','Airway disease','Thyroid Disease','CHF','DLP','Weak Peripheral Pulse','Lung rales','Systolic Murmur','Diastolic Murmur','Dyspnea','Atypical','Nonanginal','Exertional CP','LowTH Ang','LVH','Poor R Progression','BBB','VHD']
categorical_transformer = Pipeline(
    [
        ('onehot', OneHotEncoder(handle_unknown = 'ignore')),
        ('ord',OrdinalEncoder())
    ])
# transformer for numerical features
numeric_features = ['Age','Weight','Length','BMI','BP','FBS','TG','LDL','HDL','BUN','ESR','HB','K','Na','WBC','Lymph','Neut','PLT','EF-TTE']
numeric_transformer = Pipeline(
    [
        ('scaler', RobustScaler()),
         ('power',PowerTransformer(method='box-cox'))
    ]
)
preprocessor = ColumnTransformer(
    [
        ('categoricals', categorical_transformer, 
          categorical_features),
        ('numericals', numeric_transformer, numeric_features)
    ],
    remainder = 'passthrough'
)
pipeline = Pipeline(
    [
        ('preprocessing', preprocessor),
        ('clf',SVC())
    ]
)
pipeline = Pipeline(
    [
        ('preprocessing', preprocessor),
        ('clf',SVC())
    ]
)
X= X.toarray()

X_train, X_holdout, y_train, y_holdout = train_test_split(X, y, stratify = y, test_size = 0.2, random_state = 42)

X_train

params = {
    'clf__kernel':['linear', 'poly', 'rbf', 'sigmoid', 'precomputed'],
    'clf__C':[1.0,0.1,0.01,0.001],
    'clf__random_state':[42],
}

rskf = RepeatedStratifiedKFold(n_splits = 10, n_repeats =20, random_state = 42)
cv = GridSearchCV(
  pipeline, 
  params, 
  cv = rskf, 
  scoring = ['f1' ,'accuracy'], 
 
  refit = 'accuracy', 
  n_jobs = -1
  )
cv.fit(X_train, y_train)
print(f'Best parameter set: {cv.best_params_}\n')
print(f'Best F1-score: {cv.best_score_:.3f}\n')
print(f'Scores: {classification_report(y_train, cv.predict(X_train))}')

preds = cv.predict(X_holdout)
print(f'Scores: {classification_report(y_holdout, preds)}\n')
print(f'F1-score: {f1_score(y_holdout, preds):.3f}')