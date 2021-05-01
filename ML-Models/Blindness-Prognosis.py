# -*- coding: utf-8 -*-
"""Blindness-Prognosis

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1ZYCiKwTzFD6Jwu2VyxBS42mLqRS1x0Mb
"""

# pip install -U pip setuptools

# pip install scikit-survival

#All the imports
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
import pandas as pd
import sklearn as sk

from sksurv.linear_model import CoxnetSurvivalAnalysis
from sklearn.model_selection import train_test_split


#-----------Other-----------
# Make numpy printouts easier to read.
np.set_printoptions(precision=3, suppress=True)

#IO for the files
from google.colab import files
import io

#Clear output
from IPython.display import clear_output

uploaded = files.upload()

column_names = ['ID', 'Laser Type', 'Eye', 'Age', 'Type', 'Treated Group', 'Treated Status', 'Treated Time', 'Untreated Group', 'Untreated Status', 'Untreated Time']
raw_ds = pd.read_csv('drdata.csv', na_values="NaN")
raw_ds.columns = column_names

dataset = raw_ds.copy()
dataset2 = raw_ds.copy()

dataset = dataset.drop(columns=['ID','Treated Group', 'Treated Status', 'Treated Time', 'Laser Type'])
dataset['Untreated Status'] = (dataset['Untreated Status'] == 1).astype(bool)

dataset2 = dataset2.drop(columns=['ID','Untreated Group', 'Untreated Status', 'Untreated Time'])
dataset2['Treated Status'] = (dataset2['Treated Status'] == 1).astype(bool)

dataset

dataset2

X = dataset.iloc[:,:-2]
Y = dataset.iloc[:,-2:]
Y = Y.to_records(index=False)

X2 = dataset2.iloc[:,:-2]
Y2 = dataset2.iloc[:,-2:]
Y2 = Y2.to_records(index=False)

# One Hot Encodings
non_dummy_cols = ['Age'] 
dummy_cols = list(set(X.columns) - set(non_dummy_cols))
X = pd.get_dummies(X, columns=dummy_cols)

dummy_cols2 = list(set(X2.columns) - set(non_dummy_cols))
X2 = pd.get_dummies(X2, columns=dummy_cols2)

X2

random_state = 20

X_train, X_test, Y_train, Y_test = train_test_split(
    X, Y, test_size=0.2, random_state=random_state)

random_state = 20

X2_train, X2_test, Y2_train, Y2_test = train_test_split(
    X2, Y2, test_size=0.2, random_state=random_state)

X_train

X2_train

coxnetUT = CoxnetSurvivalAnalysis(l1_ratio=0.9, fit_baseline_model=True)
coxnetUT.fit(X_train, Y_train)

coxnetTR = CoxnetSurvivalAnalysis(l1_ratio=0.9, fit_baseline_model=True)
coxnetTR.fit(X2_train, Y2_train)

import pickle

pickle_out = open("coxnetUT.pkl","wb")
pickle.dump(coxnetUT, pickle_out)
pickle_out.close()

pickle_out = open("coxnetTR.pkl","wb")
pickle.dump(coxnetTR, pickle_out)
pickle_out.close()

from joblib import dump, load
dump(coxnetUT, 'coxnetUT.joblib') 
dump(coxnetTR, 'coxnetTR.joblib')

surv_funcs = {}
for alpha in coxnetUT.alphas_[:5]:
    surv_funcs[alpha] = coxnetUT.predict_survival_function(
        X_train.iloc[150:151], alpha=alpha)
    
surv_funcs2 = {}
for alpha in coxnetTR.alphas_[:5]:
    surv_funcs2[alpha] = coxnetTR.predict_survival_function(
        X2_train.iloc[150:151], alpha=alpha)

X_train.iloc[150:151].shape

for alpha, surv_alpha in surv_funcs.items():
    for fn in surv_alpha:
        plt.step(fn.x, fn(fn.x), where="post")

for alpha, surv_alpha in surv_funcs2.items():
    for fn in surv_alpha:
        plt.step(fn.x, fn(fn.x), where="post")

plt.ylim(0, 1)
plt.legend()
plt.show()

def funcUT(age,type,UT_group,eye_type):
  if(eye_type=='left'):
    eye1=1
    eye2=0
  if(eye_type=='right'):
    eye1=0
    eye2=1
  if(type==1):
    type1=1
    type2=0
  if(type==2):
    type1=0
    type2=1
  if(UT_group==6):
    ug6=1
    ug8=0
    ug9=0
    ug10=0
    ug11=0
    ug12=0
  if(UT_group==8):
    ug6=0
    ug8=1
    ug9=0
    ug10=0
    ug11=0
    ug12=0
  if(UT_group==9):
    ug6=0
    ug8=0
    ug9=1
    ug10=0
    ug11=0
    ug12=0
  if(UT_group==10):
    ug6=0
    ug8=0
    ug9=0
    ug10=1
    ug11=0
    ug12=0
  if(UT_group==11):
    ug6=0
    ug8=0
    ug9=0
    ug10=0
    ug11=1
    ug12=0
  if(UT_group==12):
    ug6=0
    ug8=0
    ug9=0
    ug10=0
    ug11=0
    ug12=1
  
  return [[age,type1,type2,ug6,ug8,ug9,ug10,ug11,ug12,eye1,eye2]]

print(funcUT(18,1,8,'left'))

def funcTR(age,laser_type,type,TR_group,eye_type):
  if(eye_type=='left'):
    eye1=1
    eye2=0
  if(eye_type=='right'):
    eye1=0
    eye2=1
  if(laser_type=='Xenon'):
    laser_type1=1
    laser_type2=0
  if(laser_type=='Argon'):
    laser_type1=0
    laser_type2=1
  if(type==1):
    type1=1
    type2=0
  if(type==2):
    type1=0
    type2=1
  if(TR_group==6):
    ug6=1
    ug8=0
    ug9=0
    ug10=0
    ug11=0
    ug12=0
  if(TR_group==8):
    ug6=0
    ug8=1
    ug9=0
    ug10=0
    ug11=0
    ug12=0
  if(TR_group==9):
    ug6=0
    ug8=0
    ug9=1
    ug10=0
    ug11=0
    ug12=0
  if(TR_group==10):
    ug6=0
    ug8=0
    ug9=0
    ug10=1
    ug11=0
    ug12=0
  if(TR_group==11):
    ug6=0
    ug8=0
    ug9=0
    ug10=0
    ug11=1
    ug12=0
  if(TR_group==12):
    ug6=0
    ug8=0
    ug9=0
    ug10=0
    ug11=0
    ug12=1
  
  return [[age,laser_type1,laser_type2,type1,type2,ug6,ug8,ug9,ug10,ug11,ug12,eye1,eye2]]

#age, laser_type('Xenon','Argon'), type(1,2), treated_group(6,8,9,10,11,12), untreated_group(6,8,9,10,11,12),eye('left','right')

surv_funcs = {}
for alpha in coxnetUT.alphas_[:5]:
    surv_funcs[alpha] = coxnetUT.predict_survival_function(
       funcUT(18,1,8,'left') , alpha=alpha)
    
surv_funcs2 = {}
for alpha in coxnetTR.alphas_[:5]:
    surv_funcs2[alpha] = coxnetTR.predict_survival_function(
        funcTR(18,'Xenon',1,8,'left'), alpha=alpha)

for alpha, surv_alpha in surv_funcs.items():
    for fn in surv_alpha:
        plt.step(fn.x, fn(fn.x), where="post")

for alpha, surv_alpha in surv_funcs2.items():
    for fn in surv_alpha:
        plt.step(fn.x, fn(fn.x), where="post")

plt.ylim(0, 1)
plt.legend()
plt.show()

