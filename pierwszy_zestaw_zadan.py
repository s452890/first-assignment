import pandas as pd
# zadanie 1
df = pd.read_csv(r'.\first-assignment\train.tsv',
                 sep='\t',
                 names=['price', 'rooms', 'msquares', 'floor', 'description'],
                 index_col=False)

avg_price = round(df.price.mean())

result_zad_1 = pd.DataFrame({'average_price': [avg_price]})
result_zad_1.to_csv('out0.csv')

# zadanie 2

df['price_per_msquared'] = df.price / df.msquares
avg_price_msquared = df.price_per_msquared.mean()
# oferty z liczbą pokoi większą równą 3
# i ceną za metr kwadrarowy  niższą niż średnia cena za metr kwadrarowy
result_zad_2 = df[(df.rooms >= 3) & (df.price_per_msquared < avg_price_msquared)]
# liczba pokoi, cena, cena za metr kwadrartowy  (bez nazw kolumn)
result_zad_2[['rooms', 'price', 'price_per_msquared']].to_csv('out1.csv', header=False)

# zadanie 3

descriptions = pd.read_csv(r'.\first-assignment\description.csv')
descriptions.rename(columns={'liczba': 'floor'}, inplace=True)  # zmiana nazwy, zeby odpowiadala drugiej tabeli
df3 = pd.read_csv(r'.\first-assignment\train.tsv',
                 sep='\t',
                 names=['price', 'rooms', 'msquares', 'floor', 'description'],
                 index_col=False)
result_zad_3 = pd.merge(df3, descriptions, on='floor', how='outer')
result_zad_3.to_csv('out2.csv')
