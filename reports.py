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
                        help='Excel file with columns "Title," "Publication_Date," "Subseries," & "Class_Number."')
    
    parser.add_argument('lookup',
                        metavar='lookup.csv',
                        help='CSV file with columns "Subseries," "Start," "Stop," & "Topic."')
    
    return parser.parse_args()

# --------------------------------------------------
def topic_lookup(class_num, lookup):
    """Assign a topic to a title based on its LC call number."""
    for i, row in lookup.iterrows():
        if class_num >= lookup['Start'][i] and class_num <= lookup['Stop'][i]:
            return lookup['Topic'][i]

def main():
    """Make a jazz noise here"""
    args = get_args()
    titles_file = args.titles
    lookup_file = args.lookup

    if os.path.isfile(titles_file) and os.path.isfile(lookup_file):
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


        # Export
        print(subseries_report)
        subseries_report.to_excel('Subseries_report.xlsx')

        print(yearly_report)
        yearly_report.to_excel('Yearly_report.xlsx')

        print(most_recent_purchase)
        most_recent_purchase.to_excel('Most_recent_book_report.xlsx')

# --------------------------------------------------

if __name__ == '__main__':
    main()