#Import libraries

import pandas as pd
import numpy as np
import altair as alt
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import OneHotEncoder
import itertools
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import shap
import pickle

#Importing data
data1 = pd.read_csv('/content/employee_survey_data.csv')
data2 = pd.read_csv('/content/general_data.csv')
data3 = pd.read_csv('/content/manager_survey_data.csv')

#Merge data
data = data3.merge(data2, on="EmployeeID", how="right").merge(data1, on="EmployeeID", how="right")


