import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

df_survey = pd.read_csv(r'.\survey_results_public.csv',
                        usecols=['Respondent', 'YearsCode', 'Age1stCode', 'WorkWeekHrs',
                                 'ConvertedComp', 'Age', 'JobSat', 'Student', 'Country'],
                        index_col=['Respondent'])
df_survey['Country'] = df_survey.Country.apply(lambda x: 0 if str(x).find("United States") == -1 else 1)
df_survey.rename(columns={'Country':'from_USA'}, inplace=True)
# deal with string values:
df_survey['JobSat'] = df_survey['JobSat'].astype('category')
df_survey['JobSatCat'] = df_survey['JobSat'].cat.codes
sat_dictionary = dict(enumerate(df_survey.JobSat.cat.categories)) # save infromation for later
df_survey = df_survey.drop('JobSat', 1)
df_survey = pd.get_dummies(df_survey, columns=['JobSatCat']) # one hot encode
df_survey['Student'] = df_survey['Student'].map({'Yes, part-time' : 1, 'Yes, full-time' : 1, 'No' : 0})
df_survey.dropna(inplace=True)
df_survey.YearsCode = pd.to_numeric(df_survey.YearsCode, errors='coerce')
df_survey.Age1stCode = pd.to_numeric(df_survey.Age1stCode, errors='coerce')
df_survey.WorkWeekHrs = pd.to_numeric(df_survey.WorkWeekHrs, errors='coerce')
# remove outliers:
outliers_columns = ['ConvertedComp', 'WorkWeekHrs', 'Age', 'Age1stCode']
for col in outliers_columns:
    df_survey = df_survey[np.abs(df_survey[col] - df_survey[col].mean()) <= 1*df_survey[col].std()]

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

