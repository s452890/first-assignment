import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

df_survey = pd.read_csv(r'.\survey_results_public.csv',
                        usecols=['Respondent', 'YearsCode', 'Age1stCode', 'WorkWeekHrs', 'ConvertedComp', 'Age', 'Hobbyist', 'CareerSat'],
                        index_col=['Respondent'])
# deal with string values:
df_survey['CareerSat'] = df_survey['CareerSat'].astype('category')
df_survey['CareerSatCat'] = df_survey['CareerSat'].cat.codes
sat_dictionary = dict(enumerate(df_survey.CareerSat.cat.categories)) # save infromation for later
df_survey = df_survey.drop('CareerSat', 1)
df_survey = pd.get_dummies(df_survey, columns=['CareerSatCat']) # one hot encode
df_survey['Hobbyist'] = df_survey['Hobbyist'].map({'Yes': 1, 'No': 0})

df_survey.dropna(inplace=True)
df_survey.YearsCode = pd.to_numeric(df_survey.YearsCode, errors='coerce')
df_survey.Age1stCode = pd.to_numeric(df_survey.Age1stCode, errors='coerce')
df_survey.WorkWeekHrs = pd.to_numeric(df_survey.WorkWeekHrs, errors='coerce')
# remove outliers:
outliers_columns = ['ConvertedComp', 'WorkWeekHrs', 'Age', 'Age1stCode']
for col in outliers_columns:
    df_survey = df_survey[np.abs(df_survey[col] - df_survey[col].mean()) <= 3*df_survey[col].std()]

correlation = df_survey.corr()
sns.heatmap(correlation, annot=True)
plt.show()





