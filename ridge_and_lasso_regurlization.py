# -*- coding: utf-8 -*-
"""Ridge and Lasso regurlization

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1UrK9oDin4x5aeU40WbpiL8OcrI4p48Fj
"""

from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error

import pandas as pd
import seaborn as sns
import numpy as np

import matplotlib.pyplot as plt
import math
from sklearn.linear_model import LassoCV
from sklearn.linear_model import RidgeCV

from sklearn.model_selection import train_test_split
from sklearn.model_selection import RepeatedKFold

from sklearn.preprocessing import StandardScaler

data=pd.read_csv("/content/Hitters (1).csv")

df_hitters=data.copy()

df_hitters

print(df_hitters['League'].unique())

df_hitters_num = pd.get_dummies(df_hitters,columns=['League','Division','NewLeague'],drop_first =True)

print(df_hitters['League'].unique())

df_hitters_num

df_hitters_num.isnull().sum()

df_hitters_num_nonnull=df_hitters_num.dropna()

df_hitters_num_nonnull.isnull().sum()

sns.displot(df_hitters_num_nonnull['Salary'])

"""This is show us how vars correlate so we can remove the negative correlation

"""

correlation = df_hitters_num_nonnull.corr()
correlation['Salary'].sort_values(ascending=True)

plt.figure(figsize=(13,6))
sns.heatmap(df_hitters.corr(),vmin=-1,vmax=1,cmap="GnBu",annot=True)
plt.show()

"""Apply Linear Regression"""

X = df_hitters_num_nonnull.drop('Salary', axis =1)
y = df_hitters_num_nonnull['Salary']

X_train,X_test,y_train,y_test = train_test_split(X,y,test_size=0.35,random_state=365)

scaler = StandardScaler()

X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

lin_reg = LinearRegression()
lin_reg.fit(X_train,y_train)

print(lin_reg.coef_)

print(lin_reg.intercept_)

lin_reg_pred=lin_reg.predict(X_test)
lin_reg_pred

lin_com=pd.DataFrame({'predicted':lin_reg_pred,'Actual':y_test})

lin_com

print(math.sqrt(mean_squared_error(y_test,lin_reg_pred)))

print(lin_reg.score(X_train,y_train))

print(lin_reg.score(X_test,y_test))

"""so there are MSE are so big so it may overvitting or multicolinearity """

cv = RepeatedKFold(n_splits=5,n_repeats=3,random_state=1)

ridge = RidgeCV(alphas=np.arange(.1,10,.1), cv=cv ,scoring='neg_mean_squared_error')

lasso = LassoCV(alphas=np.arange(.1,10,.1),cv=cv,tol=1)

lasso.fit(X_train,y_train)
lasso_reg_predict=lasso.predict(X_test)

"""So the lasso decrease the coff to zero """

print(lasso.alpha_)
print(lasso.coef_)
print(lasso.intercept_)

print(math.sqrt(mean_squared_error(y_test,lasso_reg_predict)))
print(lasso.score(X_train,y_train))
print(lasso.score(X_test,y_test))

"""so we used regulrization to prevent overfitting & multicolinearity
as: reg do perfect in  training data but in test data not well
in lasso & ridge do better in test data 
then we can choose the better model 
"""