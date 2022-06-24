import pandas as pd
import numpy as np

file_path = 'jobs.xlsx'

df_people = pd.read_excel(file_path, sheet_name='people')
df_key = pd.read_excel(file_path, sheet_name='key')

df_report = df_people.merge(df_key, left_on='Value', right_on='Value', how='left')

df_report = df_report.replace(np.nan, 0)
df_report['Price'] = df_report['Price'].astype(int)

print(df_report)