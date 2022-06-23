import pandas as pd

# Prepares a report that tallies total number of titles per range of LC call numbers
# Written by Eric Silberberg (c) 2022  |  ericsilberberg.com


df_titles = pd.read_csv('XXXX.csv')
df_lookup = pd.read_csv('LC-Classification-(XXXX).csv')

# Determine class and series from each call number
df_titles['Class'] = df_titles['Call Number'].astype(str).str[:2]
df_titles['Class'] = df_titles['Class'].str.replace(r'\d+', '')

df_titles['Series'] = df_titles['Call Number'].astype(str).str[:6]
df_titles['Series'] = df_titles['Series'].str.replace(r'\D', '').astype(int)


# Look up a title's topic by it's LC series number
def topic_lookup(class_number):
	for i, row in df_lookup.iterrows():
		if class_number >= df_lookup['Start'][i] and class_number <= df_lookup['Stop'][i]:
			return df_lookup['Topic'][i]

df_titles['Topic'] = df_titles['Series'].transform(topic_lookup)


# Tally the number of titles per topic
df_tally = df_titles['Topic'].value_counts().rename_axis(
            'Topic').reset_index(name='Count')

# Create new dataframe of class number ranges, topic, and topic tally
df_report = pd.merge(df_lookup, df_tally, on='Topic', how='outer')

df_report['Start'] = df_titles['Class'] + df_report['Start'].astype(str)
df_report['Stop'] = df_titles['Class'] + df_report['Stop'].astype(str)


# Print report to CSV
df_report.to_csv('call-number-count.csv', index=False, encoding='utf-8-sig')

print(df_report)
