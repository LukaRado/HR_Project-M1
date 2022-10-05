#Import libraries

import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
from xgboost import XGBRegressor
import pickle
import itertools

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

with st.sidebar.expander("Made By"):

    st.write("Michelle Gassner")
    st.write("Lina Tarasenko")
    st.write("Nikolaj Thulsted Vestergaard")
    st.write("Nicklas Korsholm Møller")
    st.write("Luka Radosavljevic")


tab1, tab2, tab3, tab4 = st.tabs(["Overview", "HR Managererial Tool", "SML", "UML"])

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

   ##setting up visualization for 
   col1, col2 = st.columns(2)
   with col1:
      st.write(alt.Chart(data).mark_bar().encode(
      x='Age',
      y='count(Age)',
      color='Attrition', 
      tooltip=['Age','count(Age)','Attrition'],).properties(width=600, title = 'Attrition Compared to Age').interactive())

   with col2:
      st.write(alt.Chart(data).mark_rect().encode(
       x='JobLevel',
       y='JobRole',
       color='JobSatisfaction').properties(width = 500, height = 360, title = 'Job Satisfaction Across Job Level and Department'))


   #calling the Boxplot
   colT1,colT2 = st.columns([1,10])
   with colT2:
      st.write(alt.Chart(data).mark_boxplot(extent='min-max').encode(
      x='Age:Q',
      y='JobRole:O',).properties(title = 'Age Spread Across Job Roles', width= 700))

with tab3:
   st.header("Predict Attrition")

   # use this decorator (--> @st.experimental_singleton) and 0-parameters function to only load and preprocess once in order to limit the processesing power of our application

   # Loading files through Pickle - Cat takes a series of iterables and returns a single one

   @st.experimental_singleton

   def read_objects():

       model_xgb = pickle.load(open('model_xgb.pkl','rb'))

       scaler = pickle.load(open('scaler.pkl','rb'))

       ohe = pickle.load(open('ohe.pkl','rb'))

       shap_values = pickle.load(open('shap_values.pkl','rb'))

       cats = list(itertools.chain(*ohe.categories_))

       return model_xgb, scaler, ohe, cats, shap_values



   model_xgb, scaler, ohe, cats, shap_values = read_objects()

   # Formatting for the application

   with st.expander("What's that app?"):

       st.markdown("""

       This app will help you predict attrition of the employee

       """)



   #Creating layout

   JobRole = st.selectbox('Select your Job Role', options=ohe.categories_[0])

   Gender = st.radio('What is your gender?', options=ohe.categories_[1])

   YearsAtCompany = st.number_input('How many years at this company? (1-10 years)', min_value=1, max_value=10)

   JobSatisfaction = st.number_input('Rate your Job satisfaction? (1-4)', min_value=1, max_value=4)

   NumCompaniesWorked = st.number_input('How many companies you worked at? (1-9)', min_value=0, max_value=9)

   if st.button('Predict! 🚀'):
       # make a DF for categories and transform with one-hot-encoder
       new_values_cat = pd.DataFrame(columns=['Healthcare Representative', 'Human Resources', 'Laboratory Technician',
          'Manager', 'Manufacturing Director', 'Research Director',
          'Research Scientist', 'Sales Executive', 'Sales Representative',
          'Female', 'Male'],dtype='object')

       new_values_cat['Healthcare Representative'] = 0
       new_values_cat['Human Resources'] = 0
       new_values_cat['Laboratory Technician'] = 0
       new_values_cat['Manager'] = 0
       new_values_cat['Manufacturing Director'] = 0
       new_values_cat['Research Director'] = 0
       new_values_cat['Research Scientist'] = 0
       new_values_cat['Sales Executive'] = 0
       new_values_cat['Sales Representative'] = 0
       new_values_cat['Female'] = 0
       new_values_cat['Male'] = 0
    
       new_values_cat[JobRole] = 1
       new_values_cat[Gender] = 1

       # make a DF for the numericals and standard scale
       new_df_num = pd.DataFrame({'YearsAtCompany': YearsAtCompany,
                        'JobSatisfaction':JobSatisfaction,
                        'NumCompaniesWorked':NumCompaniesWorked
                        }, index=[0])
       new_values_num = pd.DataFrame(scaler.transform(new_df_num), columns = new_df_num.columns, index=[0])  
    
       #bring all columns together
       line_to_pred = pd.concat([new_values_num, new_values_cat], axis=1)
    
       #run prediction for 1 new observation
       predicted_value = model_xgb.predict(line_to_pred)[0]



      #print out result to user
       st.metric(label="Probability of employee leave the company", value=f'{"{:.0%}".format(predicted_value)} ')


with tab4:
   st.header("Unsupervised Machine Learning")
   st.info("The UML did not work properly in the streamlit app. Therefore you get some pictures instead. For further information take a look in the notebook!")

   with st.expander("Feature Engineering"):

      st.image(image = "Feature Engineering 1 .png")

   with st.expander("PCA"):

      st.image(image = "PCA 1.png")

      st.image(image = "PCA 2.png")

      st.image(image = "PCA 3.png")

      st.image(image = "PCA 4.png")

   with st.expander("K-Means"):

      st.image(image = "KMeans.png")

      st.image(image = "KMeans 2.png")
