import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

df_survey = pd.read_csv(r'.\survey_results_public.csv',
                        usecols=['Respondent', 'YearsCode', 'Age1stCode', 'WorkWeekHrs', 'ConvertedComp', 'Age', 'Hobbyist', 'MainBranch', 'CareerSat'],
                        index_col=['Respondent'])
df_survey.dropna(inplace=True)
df_survey.YearsCode = pd.to_numeric(df_survey.YearsCode, errors='coerce')
df_survey.Age1stCode = pd.to_numeric(df_survey.Age1stCode, errors='coerce')
df_survey.WorkWeekHrs = pd.to_numeric(df_survey.WorkWeekHrs, errors='coerce')
correlation = df_survey.corr()
sns.heatmap(correlation, annot=True)
plt.show()



