import pandas as pd
import numpy as np
import string
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

def subject_lookup(topic_num, lookup):
    """Assign a subject to a title based on its LC call number."""
    for i, row in lookup.iterrows():
        if topic_num >= lookup['Start'][i] and topic_num <= lookup['Stop'][i]:
            return lookup['Subject'][i]

def strip_punctuations(text):
    """Remove punctuation marks."""
    for char in string.punctuation:
        text = text.replace(char, " ")
    return text

def get_keywords_tally(dataframe):
    """Build a tokenized list of keywords from book titles in dataframe."""
    titles = []
    for title in dataframe['Title']:
        title = strip_punctuations(title)
        titles.append(title.lower())
    
    stop_words = set(stopwords.words('english'))
    keywords = []
    for t in titles:
        words = word_tokenize(t)
        for w in words:
            if w not in stop_words:
                keywords.append(w)

    return pd.value_counts(np.array(keywords))


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
pre_1964 = lc_subclass.loc[lc_subclass['Publication_Date'] <= 1964]
post_1964 = lc_subclass.loc[(lc_subclass['Publication_Date'] > 1964) & (lc_subclass['Publication_Date'] <= 1975)]

pre_1964_keywords = get_keywords_tally(pre_1964)
post_1964_keywords = get_keywords_tally(post_1964)

print('Pre-1964----------------------------------------------')
print(pre_1964_keywords.head(40))
print('Post-1964----------------------------------------------')
print(post_1964_keywords.head(40))
