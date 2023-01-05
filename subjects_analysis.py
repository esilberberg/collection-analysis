import pandas as pd
import string

def subject_lookup(topic_num, lookup):
    """Assign a subject to a title based on its LC call number."""
    for i, row in lookup.iterrows():
        if topic_num >= lookup['Start'][i] and topic_num <= lookup['Stop'][i]:
            return lookup['Subject'][i]

def strip_punctuations(text):
    for char in string.punctuation:
        text = text.replace(char, "")
    return text

df_lookup = pd.read_csv('LC-Classification-(L).csv')
df = pd.read_excel('L-Class_Print_Titles_CLEAN.xlsx')

# List of all subclasses.
subclass_list = df_lookup['Subclass'].unique()

# Iterate through all subclass and get LC subject for each title.
df_out = pd.DataFrame()
for subclass in subclass_list:
    # 'reset_index()' quells SettingWithCopyWarning.
    titles = df.loc[df['Subclass'] == subclass].reset_index(drop=True)
    lookup = df_lookup.loc[df_lookup['Subclass'] == subclass]

    titles['Subject'] = titles['Topic_Number'].apply(subject_lookup, lookup=lookup)

    df_out = pd.concat([df_out, titles])

lc_subclass = df_out.loc[df_out['Subclass'] == 'LC']

pre_1964 = lc_subclass.loc[lc_subclass['Publication_Date'] < 1964]

print(pre_1964)