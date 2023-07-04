import pandas as pd
import psycopg2
from sqlalchemy import create_engine



print('test')

#read in excel file income_alias with six sheets
excel_file = '/Users/katherinecunniffe/Desktop/pandas_project/youth_centre_project/youth_centre/income_alias.xlsx'

excel_data = pd.read_excel(excel_file, sheet_name=None)
df2017_18 = excel_data['2017-18']
df2018_19 = excel_data['2018-19']
df2019_20 = excel_data['2019-20']
df2020_21 = excel_data['2020-21']
df2021_22 = excel_data['2021-22']


#test
print(df2017_18.head())

#connect 
try:
    pgconn = psycopg2.connect(
        host='localhost',
        user='postgres',
        password='postgres',
        database='postgres')
    print("connected!")
except: 
    print("error")

conn_string = f'postgresql+psycopg2://postgres:postgres@localhost/postgres'
engine = create_engine(conn_string)

#create six tables in the postgres db
df2017_18.to_sql('2017-18', engine, if_exists='replace', index=False)
df2018_19.to_sql('2018-19', engine, if_exists='replace', index=False)
df2019_20.to_sql('2019-20', engine, if_exists='replace', index=False)
df2020_21.to_sql('2020-21', engine, if_exists='replace', index=False)
df2021_22.to_sql('2021-22', engine, if_exists='replace', index=False)

#calculate mean ammount for fundraiser each year
years = ['2017-18', '2018-19', '2019-20', '2020-21', '2021-22']
for year in years:
    query = f"SELECT AVG(\"Donation via Fundraiser\") AS mean_amount FROM \"{year}\""
    result = pd.read_sql_query(query, engine)
    mean_amount = result.iloc[0]['mean_amount']
    print(f"Mean amount for {year}: {mean_amount}")

# Create a cursor object to execute SQL queries
cursor = pgconn.cursor()

# Execute SQL queries to create/update the 'Total Donation' column in each table
years = ['2017-18', '2018-19', '2019-20', '2020-21', '2021-22']
for year in years:
    query = f"ALTER TABLE \"{year}\" ADD COLUMN \"Total Donation\" numeric"
    cursor.execute(query)

    query = f"UPDATE \"{year}\" SET \"Total Donation\" = \"Donation via Fundraiser\" + \"Direct Donation\""
    cursor.execute(query)

    # Commit the changes to the database
    pgconn.commit()

    # Close the cursor and database connection
cursor.close()
pgconn.close()