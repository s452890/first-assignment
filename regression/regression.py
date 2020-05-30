import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

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
df_survey.dropna(inplace=True)
for column in ['YearsCode', 'Age1stCode', 'WorkWeekHrs']:
    df_survey[column] = pd.to_numeric(df_survey[column], errors='coerce')
# remove outliers with quantile method:
Q1 = df_survey[['ConvertedComp', 'WorkWeekHrs']].quantile(0.25)
Q3 = df_survey[['ConvertedComp', 'WorkWeekHrs']].quantile(0.75)
IQR = Q3 - Q1
df_survey = df_survey[~((df_survey[['ConvertedComp', 'WorkWeekHrs']] < (Q1 - 1.5 * IQR)) 
                        | (df_survey[['ConvertedComp', 'WorkWeekHrs']] > (Q3 + 1.5 * IQR))).any(axis=1)]
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

