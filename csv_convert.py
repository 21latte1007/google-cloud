import pandas as pd

df = pd.read_csv('business-financial-data-september-2022-quarter.csv')
df['Period'] = df["Period"].astype(dtype='string')
df['Period'] = df["Period"].str.replace(".", "", )
df['Period'] = pd.to_datetime(df['Period'], format='%Y%m')

df['Period'] = df['Period'].dt.strftime('%Y-%m')
df["Period"] = pd.to_datetime(df["Period"] + "-01", format="%Y-%m-%d").dt.date.astype(str)

print(df['Period'])

df.to_csv('updated_csv_file.csv', index=True)
