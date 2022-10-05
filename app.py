#Import libraries


import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
from xgboost import XGBRegressor



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
at_1 = data.loc[(data['Attrition'] == 'Yes')]
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

colT1,colT2 = st.columns([10,20])
with colT2:
   st.title('HR Managing Tool Project')

with st.sidebar.expander("Learn more about the Visualization"):

    st.write("hey")



with st.sidebar.expander("Learn More about the Unsupervised Machine Learning "):

    st.write("hey")



with st.sidebar.expander("Learn More about the Supervised Machine Learning "):

    st.write("hey")

tab1, tab2, tab3 = st.tabs(["Overview", "HR Managererial Tool", "SML"])

with tab1:
   st.header("Overview")
   st.write("We have created a tool, which main purpose is for the HR department to gain an overview of the company.")
   st.text("")
   st.write("We have done this through the use of important KPI's which we have supplimented with useful graphs and information required to gain a proper insight into the state of the company.")
   st.text("")
   st.write("We have also used supervised machine learning to predict probability of attrition while showing specific indicators for a picked employee and unsupervised learning to help us understand clusters which might be formed within the company, as these clusters could signal action is required")


with tab2:
   st.header("HR Managerial Informational Tool")   

   ret_met, ret_per, ret_age = st.columns(3)
   ret_met.metric(label = "Retention rate (%)", value = limited_float_ret)
   ret_per.metric(label = "Overall Performance (Scale 1-4)", value = limited_float_per)
   ret_age.metric(label = "Mean Workforce Age", value = limited_float_age)

   ##setting up plots

   #Boxplot
   st.write(alt.Chart(data).mark_boxplot(extent='min-max').encode(
   x='Age:Q',
   y='JobRole:O'
   ))


   st.write(alt.Chart(data).mark_rect().encode(

       alt.X('YearsWithCurrManager:O', bin=alt.Bin(maxbins=60)),

       alt.Y('sum(PerformanceRating):Q', bin=alt.Bin(maxbins=40)),

       alt.Color('PerformanceRating:Q', scale=alt.Scale(scheme='greenblue'))))

   
   


   selection = alt.selection_multi(fields=['series'], bind='legend')

   st.write(alt.Chart(data).mark_area().encode(

       alt.X('YearsWithCurrManager:O', axis=alt.Axis(domain=False, format='%Y', tickSize=0)),

       alt.Y('PerformanceRating:Q', stack='center', axis=None),

       alt.Color('Department:N', scale=alt.Scale(scheme='category20b')),

       opacity=alt.condition(selection, alt.value(1), alt.value(0.2))

   ).add_selection(

       selection
   ))

   col1, col2 = st.columns(2)
   with col1:
      st.write(alt.Chart(data).mark_bar().encode(
      x='Age',
      y='sum(Age)',
      color='Attrition').properties(width=500).interactive())

   with col2:
      st.write(alt.Chart(data).mark_rect().encode( #we would like to add more steps in JobSatisfaction
       x='JobLevel',
       y='JobRole',
       color='JobSatisfaction'
      ).properties(width = 500, height = 500))




with tab3:
   st.header("SML")