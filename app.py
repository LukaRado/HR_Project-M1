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


#Primary KPI calculations (Retention rate, Overall performance, mean age)
at_0 = data.loc[(data['Attrition'] == 'No')]
ret_rate = (at_0['Attrition'].count() / 4300) * 100
limited_float_ret = round(ret_rate, 1)


o_per = data['PerformanceRating'].mean()
limited_float_per = round(o_per, 1)

m_age = data['Age'].mean()
limited_float_age = round(m_age, 1)

##Streamlit interface:
st.set_page_config(page_title='HR Managing Tool',
                    page_icon="🛠",
                    layout='wide')

colT1,colT2 = st.columns([1,12])
with colT2:
   st.title('HR Managing Tool Project')

tab1, tab2, tab3 = st.tabs(["Overview", "HR Manager", "SML"])

with tab1:
   st.header("Overview")
   st.write("Hello motherfuckers..")


with tab2:
   st.header("HR Managers Informational Sheet")   

   ret_met, ret_per, ret_age = st.columns(3)
   ret_met.metric(label = "Retention rate (%)", value = limited_float_ret)
   ret_per.metric(label = "Overall Performance (Scale 1-4)", value = limited_float_per)
   ret_age.metric(label = "Mean Workforce Age", value = limited_float_age)

   #first plot


with tab3:
   st.header("SML")