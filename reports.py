#!/usr/bin/env python3
"""
Author : esilberberg
Contact: ericsilberberg.com
Date   : 2022-11-01
Purpose: Generates Reports on Library Print Collections
"""
import argparse
import os
import pandas as pd

# --------------------------------------------------

def get_args():
    """Get command-line arguments"""
    parser = argparse.ArgumentParser(
        description='Generates Reports on Library Print Collections',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
   
    parser.add_argument('titles',
                        metavar='titles.xlsx',
                        help='Excel file with columns "Title," "Publication_Date," "Subclass," & "Topic_Number."')
    
    parser.add_argument('lookup',
                        metavar='lookup.csv',
                        help='CSV file with columns "Subclass," "Start," "Stop," & "Subject."')
    
    return parser.parse_args()

# --------------------------------------------------
def subject_lookup(topic_num, lookup):
    """Assign a subject to a title based on its LC call number."""
    for i, row in lookup.iterrows():
        if topic_num >= lookup['Start'][i] and topic_num <= lookup['Stop'][i]:
            return lookup['Subject'][i]

def main():
    """Make a jazz noise here"""
    args = get_args()
    titles_file = args.titles
    lookup_file = args.lookup

    if os.path.isfile(titles_file) and os.path.isfile(lookup_file):
        df = pd.read_excel(titles_file)
        df_lookup = pd.read_csv(lookup_file) 
        
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

        # Subclass report ----------
        subclass_groups = df_out.groupby(['Subclass'])
        subclass_report = subclass_groups['Subject'].value_counts()
        

        # Yearly report ----------
        yearly_summary = df['Publication_Date'].describe()
        yearly_tally = df['Publication_Date'].value_counts()
        yearly_report = pd.concat([yearly_summary, yearly_tally])

        # Most recent book by subject report ---------
        most_recent_purchase = df_out.groupby('Subject')['Publication_Date'].max()


        # Export
        print(subclass_report)
        subclass_report.to_excel('Subclass_report.xlsx')

        print(yearly_report)
        yearly_report.to_excel('Yearly_report.xlsx')

        print(most_recent_purchase)
        most_recent_purchase.to_excel('Most_recent_book_report.xlsx')

# --------------------------------------------------

if __name__ == '__main__':
    main()