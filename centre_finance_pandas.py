import pandas as pd
import psycopg2
from sqlalchemy import create_engine
import matplotlib.pyplot as plt


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

df2017_18.to_sql('2017-18', engine, if_exists='replace', index=False)

column_names = list(df2017_18.columns)
print(column_names)

#how much in total is raised each year via Fundraiser and direct

dataframes = [df2017_18, df2018_19, df2019_20, df2020_21, df2021_22]
years = ['2017-18', '2018-19', '2019-20', '2020-21', '2021-22']
total_f = []
total_d = []
total_o = []

# Calculate the total amounts for each year
for year, df in zip(years, dataframes):
    total_fundraiser = df.iloc[:, 2].sum()  # Assuming 'Donation via Fundraiser' is the third column (index 2)
    total_direct = df.iloc[:, 3].sum()  # Assuming 'Donation Direct' is the fourth column (index 3)
    total_overall = total_fundraiser + total_direct
    total_f.append(total_fundraiser)
    total_d.append(total_direct)
    total_o.append(total_overall)
    print(f'Total Fundraiser for {year}: {total_fundraiser}. Total Direct for {year}: {total_direct}. Total Overall for {year}: {total_overall}')

# Create a pandas DataFrame for the totals
df_totals = pd.DataFrame({'Year': years, 'Total Fundraiser': total_f, 'Total Direct': total_d, 'Total Overall': total_o})

# Plotting the data
plt.plot(df_totals['Year'], df_totals['Total Fundraiser'], label='Total Fundraisers')
plt.plot(df_totals['Year'], df_totals['Total Direct'], label='Total Donations')
plt.plot(df_totals['Year'], df_totals['Total Overall'], label='Total Overall')

# Adding labels and title to the plot
plt.xlabel('Year')
plt.ylabel('Amount')
plt.title('Total Donations, Fundraisers, and Overall')

# Adding a legend
plt.legend()

# Displaying the plot
plt.show()

# Displaying the plot
plt.show()

#which source IDs donate every year, then via Fundraiser or Direct

# Concatenate the data frames into a single data frame
dfs = [df2017_18, df2018_19, df2019_20, df2020_21, df2021_22]
combined_df = pd.concat(dfs)

# Group the data by 'Source ID' column and count the occurrences
id_counts = combined_df['Source ID'].value_counts().reset_index()
id_counts.columns = ['Source ID', 'Count']

# Filter the values that appear in multiple data frames (with count > 1)
multiple_occurrences = id_counts[id_counts['Count'] > 1]

# Print the values and their frequencies
print(multiple_occurrences)


#list top largest donator source ID in descending order for each year, what proportion of these are via Fundraiser, are any of these in multible years

# Iterate over each data frame
for year, df in zip(years, dataframes):
    # Concatenate values from column C and D into a single series
    combined_values = pd.concat([df['C'], df['D']])

    # Sort the values in descending order and select the top 10
    top_10 = combined_values.nlargest(10)

    # Filter the data frame based on the top 10 values in column C or D
    filtered_df = df[df['C'].isin(top_10) | df['D'].isin(top_10)]

    # Sort the filtered data frame by ID column
    sorted_df = filtered_df.sort_values(by='C')

    # Print the results for the current year
    print(f"Top 10 values for {year}:")
    print(sorted_df[['ID', 'C', 'D']])
    print()