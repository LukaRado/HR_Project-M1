#Import libraries


import streamlit as st
import pandas as pd
import numpy as np
import altair as alt


#Importing data
data1 = pd.read_csv('employee_survey_data.csv')
data2 = pd.read_csv('general_data.csv')
data3 = pd.read_csv('manager_survey_data.csv')

##PREPROCESSING

#Merge data
data = data3.merge(data2, on="EmployeeID", how="right").merge(data1, on="EmployeeID", how="right")

#Dropping NA values and unwanted variables
data = data.dropna()
data = data.drop(['MaritalStatus','StandardHours', 'EmployeeCount', 'Over18'], axis=1)

#Defining dataframe variables
data = data[['Attrition', 'BusinessTravel', 'Department','EducationField', 'Gender','JobRole', 'DistanceFromHome',
       'Education', 'EmployeeID', 'JobLevel',
        'MonthlyIncome', 'NumCompaniesWorked',
       'PercentSalaryHike', 'StockOptionLevel', 'TotalWorkingYears',
       'TrainingTimesLastYear', 'YearsAtCompany', 'YearsSinceLastPromotion',
       'YearsWithCurrManager', 'EnvironmentSatisfaction', 'JobSatisfaction',
       'WorkLifeBalance', 'JobInvolvement', 'PerformanceRating','Age']]

#Changing our unneccesary floats to integers
data['EnvironmentSatisfaction'] = data['EnvironmentSatisfaction'].astype(int)
data['JobSatisfaction'] = data['JobSatisfaction'].astype(int)
data['WorkLifeBalance'] = data['WorkLifeBalance'].astype(int)
data['NumCompaniesWorked'] = data['NumCompaniesWorked'].astype(int)
data['TotalWorkingYears'] = data['TotalWorkingYears'].astype(int)



#Streamlit interface:
st.title['Hello World!']
