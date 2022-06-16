import pandas as pd

# Prepares a report that tallies total number of print titles per range of LC call numbers
# for Latin American & Caribbean History (F)
# Written by Eric Silberberg (c) 2022  |  ericsilberberg.com

data = input('Enter path to CSV of titles with LC call numbers ')

df_titles = pd.read_csv(data)
df_lookup = pd.read_csv('LC-Classification-(F).csv')

# Strip call numbers to class number and convert to integers
class_numbers = []
for n in df_titles['Call Number']:
    try:
        class_numbers.append(int(n[1:5]))
    except TypeError:
        pass

df_titles['Class Number'] = class_numbers

# Look up a title's topic by it's LC class number
def topic_lookup(class_number):
	for i, row in df_lookup.iterrows():
		if class_number >= df_lookup['Start'][i] and class_number <= df_lookup['Stop'][i]:
			return df_lookup['Topic'][i]

topics = []
for num in df_titles['Class Number']:
	x = topic_lookup(num)
	print(x)
	topics.append(x)

df_titles['Topic'] = topics

# Tally the number of titles per topic
df_tally = df_titles['Topic'].value_counts().rename_axis(
            'Topic').reset_index(name='Count')

# Create new dataframe of class number ranges, topic, and topic tally
df_report = pd.merge(df_lookup, df_tally, on='Topic', how='outer')

df_report['Start'] = 'F' + df_report['Start'].astype(str)
df_report['Stop'] = 'F' + df_report['Stop'].astype(str)

# Print report to CSV
df_report.to_csv('call-number-count.csv', index=False, encoding='utf-8-sig')

print(df_report)