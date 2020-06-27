import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error

df_survey = pd.read_csv(r'.\survey_results_public.csv',
                        usecols=['Respondent', 'YearsCode', 'Age1stCode', 'WorkWeekHrs', 'Student',
                                 'ConvertedComp', 'Age', 'JobSat', 'Country'],
                        index_col=['Respondent'])
df_survey['Country'] = df_survey.Country.apply(lambda x: 0 if str(x).find("United States") == -1 else 1)
df_survey.rename(columns={'Country':'from_USA'}, inplace=True)
# deal with string values:
df_survey['JobSat'] = df_survey['JobSat'].map({'Slightly satisfied' : 'Satisfied',
                                               'Slightly dissatisfied' : 'Dissatisfied',
                                               'Neither satisfied nor dissatisfied' : 'Not specified',
                                               'Very satisfied' : 'Satisfied',
                                               'Very dissatisfied': 'Dissatisfied'})

df_survey['JobSat'] = df_survey['JobSat'].astype('category')
df_survey['JobSatCat'] = df_survey['JobSat'].cat.codes
sat_dictionary = dict(enumerate(df_survey.JobSat.cat.categories)) # save infromation for later
df_survey = df_survey.drop('JobSat', 1)
df_survey = pd.get_dummies(df_survey, columns=['JobSatCat']) # one hot encode
df_survey['Student'] = df_survey['Student'].map({'Yes, part-time' : 1, 'Yes, full-time' : 1, 'No' : 0})
for column in ['YearsCode', 'Age1stCode', 'WorkWeekHrs']:
    df_survey[column] = pd.to_numeric(df_survey[column], errors='coerce')
# remove outliers with quantile method:
Q1 = df_survey[['Age1stCode', 'YearsCode', 'ConvertedComp', 'WorkWeekHrs', 'Age']].quantile(0.25)
Q3 = df_survey[['Age1stCode', 'YearsCode', 'ConvertedComp', 'WorkWeekHrs', 'Age']].quantile(0.75)
IQR = Q3 - Q1
df_survey = df_survey[~((df_survey[['Age1stCode', 'YearsCode', 'ConvertedComp', 'WorkWeekHrs', 'Age']] < (Q1 - 1.5 * IQR)) 
                        | (df_survey[['Age1stCode', 'YearsCode', 'ConvertedComp', 'WorkWeekHrs', 'Age']] > (Q3 + 1.5 * IQR))).any(axis=1)]
df_survey.dropna(inplace=True)
# plot correlation matrix
corr = df_survey.corr()
fig = plt.figure()
ax = fig.add_subplot(111)
cax = ax.matshow(corr,cmap='coolwarm', vmin=-1, vmax=1)
fig.colorbar(cax)
ticks = np.arange(0,len(df_survey.columns),1)
ax.set_xticks(ticks)
plt.xticks(rotation=70)
ax.set_yticks(ticks)
ax.set_xticklabels(df_survey.columns)
ax.set_yticklabels(df_survey.columns)
plt.show()

#modelling linear regression
Y = df_survey[['ConvertedComp']]
X_train = df_survey[['YearsCode', 'from_USA', 'Student', 'JobSatCat_2', 'Age']]
model1 = LinearRegression()
model1.fit(X_train, Y)
Y_pred = model1.predict(X_train)
MSE = mean_squared_error(np.array(Y), Y_pred)
print(f"mean squared error = {MSE}") # a lot


#create random vector X of variables
#and predict values using the model
import random
random.seed(30)
random_data = {}
for category in ['YearsCode', 'from_USA', 'Student', 'JobSatCat_2', 'Age']:
    random_data[category] = random.sample(list(df_survey[category]), 50)
X_random = pd.DataFrame(random_data)

Y_pred_random = model1.predict(X_random)




