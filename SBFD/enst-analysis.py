import pandas as pd

file = 'ENST Library Catalog.xlsx'

df = pd.read_excel(file)

books_by_year = df['AÑO PUBLICACION'].value_counts()
books_by_author = df['AUTOR'].value_counts()
books_by_publisher = df['EDITORIAL'].value_counts()

df['LC_Category'] = df['CLASIFICACION(LC)'].apply(lambda x: ''.join(filter(str.isalpha, x))[:2])
books_by_lc = df['LC_Category'].value_counts()

print(books_by_publisher)