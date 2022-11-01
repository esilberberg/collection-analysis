import pandas as pd

def topic_lookup(class_num, lookup):
    """Assign a topic to a title based on its LC call number."""
    for i, row in lookup.iterrows():
        if class_num >= lookup['Start'][i] and class_num <= lookup['Stop'][i]:
            return lookup['Topic'][i]

# Import.
titles_file = "L-Class Print Titles CLEAN.xlsx"
lookup_file = "L-Class-Ranges.xlsx"

df = pd.read_excel(titles_file)
df_lookup = pd.read_csv(lookup_file) 

# List of all subseries.
subseries_list = df_lookup['Subseries'].unique()

# Iterate through all subseries and get LC topic for each title.
df_out = pd.DataFrame()
for series in subseries_list:
    # 'reset_index()' quells SettingWithCopyWarning.
    titles = df.loc[df['Subseries'] == series].reset_index(drop=True)
    lookup = df_lookup.loc[df_lookup['Subseries'] == series]

    titles['Topic'] = titles['Class_Number'].apply(topic_lookup, lookup=lookup)
    
    df_out = pd.concat([df_out, titles])

# Subseries report ----------
subseries_groups = df_out.groupby(['Subseries'])
subseries_report = subseries_groups['Topic'].value_counts()

# Yearly report ----------
yearly_summary = df['Publication_Date'].describe()
yearly_tally = df['Publication_Date'].value_counts()
yearly_report = pd.concat([yearly_summary, yearly_tally])

# Most recent book by topic report ---------
most_recent_purchase = df_out.groupby('Topic')['Publication_Date'].max()
