

#importing libraries
import pandas as pd
import numpy as np
import altair as alt


data1 = pd.read_csv('employee_survey_data.csv')
data2 = pd.read_csv('general_data.csv')
data3 = pd.read_csv('manager_survey_data.csv')
data1.info()
data2.info()
data3.info()
Merging the Data

#merging the data
data = data3.merge(data2, on="EmployeeID", how="right").merge(data1, on="EmployeeID", how="right") 
data.head()
data.info()
data.shape
data.duplicated().sum() # to see if there are duplicated columns
data.isna().sum() #overview if there are 0/ Nans
data = data.dropna()
data.isna().sum()
data.describe()
data=data.drop(['MaritalStatus','StandardHours', 'EmployeeCount', 'Over18'], axis=1)
data.info()
data=data[['Attrition', 'BusinessTravel', 'Department','EducationField', 'Gender','JobRole', 'DistanceFromHome',
       'Education', 'EmployeeID', 'JobLevel',
        'MonthlyIncome', 'NumCompaniesWorked',
       'PercentSalaryHike', 'StockOptionLevel', 'TotalWorkingYears',
       'TrainingTimesLastYear', 'YearsAtCompany', 'YearsSinceLastPromotion',
       'YearsWithCurrManager', 'EnvironmentSatisfaction', 'JobSatisfaction',
       'WorkLifeBalance', 'JobInvolvement', 'PerformanceRating','Age']]
data.info()

#Count people who left and stayed at the company
data["Attrition"].value_counts()

# State of the Art HR 
alt.Chart(data).mark_circle(size=60).encode( #we need to add properties for streamlit #its hard to interpret
    x='MonthlyIncome',
    y='TotalWorkingYears',
    color='JobRole',
    tooltip=['JobRole', 'MonthlyIncome', 'TotalWorkingYears']
).interactive()

source = data #figure something out! 

alt.Chart(source).mark_bar().encode(
    x='MonthlyIncome',
    y='TotalWorkingYears',
    color='JobRole')

#use value count for checking the outliers 
alt.Chart(data).mark_point().encode(
    alt.X('mean(Age):Q', scale=alt.Scale(zero=False)),
    y='JobRole:O',
    color='Gender:N',
    facet=alt.Facet('JobLevel:O', columns=2),
    tooltip=['Gender', 'JobRole']
).properties(
    width=200,
    height=100,
    )
alt.Chart(data).mark_rect().encode( #we would like to add more steps in JobSatisfaction
    x='JobLevel',
    y='JobRole',
    color='JobSatisfaction'
).properties(width=200)
alt.Chart(data).mark_bar().encode(x='Age',y='sum(Age)',color='Attrition').properties(width=700).interactive()


#selected_df = data[['Attrition','JobSatisfaction','YearsAtCompany','MonthlyIncome','Age','JobLevel','PerformanceRating','TrainingTimesLastYear']]
selected_df = data[['Attrition', 'Department','EducationField','Gender']]
X = selected_df.iloc[:,1:] #we select the X values from selected_df
Y = selected_df.Attrition #we select all rows and the column Attrition(index 0)
ohe_X = OneHotEncoder(sparse=False) #we are encoding values to save changes
X_ohe = ohe_X.fit_transform(X.iloc[:,:]) # we are not sure? 
X_ohe #lets check X_ohe
columns_X_ohe = list(itertools.chain(*ohe_X.categories_))
X_cat = pd.DataFrame(X_ohe, columns = columns_X_ohe)
X_cat
data['Department'].value_counts()
data['EducationField'].value_counts()
data.describe()
data.info()
data.head()
#changing our float values to integers
data['EnvironmentSatisfaction'] = data['EnvironmentSatisfaction'].astype(int)
data['JobSatisfaction'] = data['JobSatisfaction'].astype(int)
data['WorkLifeBalance'] = data['WorkLifeBalance'].astype(int)
data['NumCompaniesWorked'] = data['NumCompaniesWorked'].astype(int)
data['TotalWorkingYears'] = data['TotalWorkingYears'].astype(int)
#Retention Rate (percentage)
at_0 = data.loc[(data['Attrition'] == 'No')]

ret_rate = (at_0['Attrition'].count() / 4300) * 100

#Overall Performance (scale from 1-4)

o_per = data['PerformanceRating'].mean()
#mean age 

m_age = data['Age'].mean()

