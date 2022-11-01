# Collections Analysis
A suite of command line tools to analyze the scope and history of [Queens College Library](https://library.qc.cuny.edu/) print and ebook collections.

- **clean.py** Prepares print collection data for analysis. Requires that the input is an excel file that contain at minimum columns "Title", "Publication_Date", and "Call_Number."

## Parts of a LC Call Number
Terminology used to describe parts of [LC Classification](https://www.loc.gov/catdir/cpso/lcco/) in scripts during preparation and analysis.

Call Number: LB3013 .S29 2007

|Series             | Subseries | Class Number | Cutter | Year |
|-------------------|-----------|--------------|--------|------|
|   L (Education)   |     LB    |     3013     |  .S29  | 2007 |
