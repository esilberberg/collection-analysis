#!/usr/bin/env python3
"""
Author : esilberberg
Contact: ericsilberberg.com
Date   : 2022-11-01
Purpose: Prepare Print Collection Spreadsheet for Analysis
"""
import argparse
import os
import pandas as pd

# --------------------------------------------------

def get_args():
    """Get command-line arguments"""
    parser = argparse.ArgumentParser(
        description='Prepare Print Collection Spreadsheet for Analysis',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
   
    parser.add_argument('titles',
                        metavar='titles_list.xlsx',
                        help='Excel file with columns "Title", "Publication_Date", & "Call_Number."')
    
    return parser.parse_args()

# --------------------------------------------------

def main():
    """Make a jazz noise here"""
    args = get_args()
    excel_file = args.titles
    
    if os.path.isfile(excel_file):
        df = pd.read_excel(excel_file)
        df.dropna(inplace=True)

        # Clean Publication Year -------
        # Use regex to remove all non-numeric characters from publication dates
        df['Publication_Date'] = df['Publication_Date'].str.replace(r'[^0-9]+', '')
        # Avoid publication dates presented as ranges. Takes first year in entry.
        df['Publication_Date'] = df['Publication_Date'].str.slice(0,4)

        # Clean Call Numbers -------
        # Revise decimal point call numbers. Split at decimal and select first index after split.
        df['Call_Number'] = df['Call_Number'].str.split('.').str[0]
        # Separate subseries letters from class numbers
        df[['Subclass', 'Topic_Number']] = df['Call_Number'].str.extract('([A-Za-z]+)([0-9]+)', expand = True)

        # Export
        print(df)
        base = os.path.basename(excel_file)
        file_name = os.path.splitext(base)[0]
        df.to_excel(f'{file_name}_CLEAN.xlsx', index=False)

# --------------------------------------------------

if __name__ == '__main__':
    main()