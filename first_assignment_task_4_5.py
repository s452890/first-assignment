import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
# task 4
df_survey = pd.read_csv(r'.\first-assignment\survey_results_public.csv',
                        usecols=['Respondent', 'ConvertedComp', 'Age'],
                        index_col=['Respondent'])
df_survey.dropna(inplace=True)

plt.plot(df_survey['Age'], df_survey['ConvertedComp'], 'ro', markersize=0.3)
plt.xlabel('Age')
plt.ylabel('Salary in USD')
plt.show()

# task 5
df_survey2 = pd.read_csv(r'.\first-assignment\survey_results_public.csv',
                        usecols=['Respondent', 'CareerSat', 'ConvertedComp', 'Age'],
                        index_col=['Respondent'])
df_survey2.dropna(inplace=True)
sat_values = df_survey2[['CareerSat']].values
unique_sat_values = np.unique(sat_values)

for sat in unique_sat_values:
    plt.plot(df_survey2[df_survey2['CareerSat'] == sat]['Age'],
             df_survey2[df_survey2['CareerSat'] == sat]['ConvertedComp'],
             'ro', markersize=0.3)
    plt.xlabel('Age')
    plt.ylabel('Salary in USD')
    plt.title(sat)
    plt.show()
