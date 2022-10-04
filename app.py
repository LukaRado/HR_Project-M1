#Import libraries

import pandas as pd
import numpy as np
import altair as alt


#Importing data
data1 = pd.read_csv('/content/employee_survey_data.csv')
data2 = pd.read_csv('/content/general_data.csv')
data3 = pd.read_csv('/content/manager_survey_data.csv')

#Merge data
data = data3.merge(data2, on="EmployeeID", how="right").merge(data1, on="EmployeeID", how="right")


