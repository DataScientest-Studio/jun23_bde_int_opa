import pandas as pd
from yahoo_fin.stock_info import get_data   
from yahooquery import Screener
import psycopg2        # for mac try to install psycopg2-binary
import io

# Finding first 250 symbols in a list
s = Screener()
data = s.get_screeners('all_cryptocurrencies_us', count=20) # number of currencies you want to fetch

# retrieving a list of symbols
dicts = data['all_cryptocurrencies_us']['quotes']
symbols = [d['symbol'] for d in dicts]


# initialling Parameters
start_date= "01/01/2023"    # the date we want to start from
end_date = None             # the end date, None = today
index_as_date = False       # Set the date as index of the df
interval = "1d"             # retrieving the data on a daily basis

# 1- FUNCTION to retrieve the data of a single ticker (AND OPTIONAL) saving the csv files locally.
def ticker_data(symbol):
    # the get_data function is from yahoo_fin.stock_info 
    response = get_data(symbol, start_date, end_date, index_as_date, interval)
    # putting the response in a DataFrame
    df = pd.DataFrame(response)

    # selecting all the columns 
    df = df[['date', 'open', 'high', 'low', 'close', 'adjclose', 'volume', 'ticker']]

    # modify the date coluumn from object to date
    df['date'] = pd.to_datetime(df['date'])

    #cleaning the symobol name and columns names for sql use
    df.columns = [x.lower().replace(" ","").replace("-","_") for x in df.columns]
    df["currency_id"] = symbol.replace("-USD", "").lower()

    # make ticker also lower case, for sake of consistency 
    df["ticker"] = df["ticker"].str.lower()
    
    # Returning the DataFrame as file
    df.to_csv('~/Downloads/crypto_data_output_file.csv', index = False, encoding='utf-8', header= True)
    print ("Daily rates for", symbol, "starting", start_date, "fetched")
    
    return df


# 2- Changing the types of columns from dtypes(python) to SQL types

# 2.1 mapping
map_dict={"datetime64[ns]":"DATE",
              "float64": "NUMERIC",
              "object": "VARCHAR",
              "Int64": "INTEGER"}

table_name = "crypto_daily_rates_hist"

# 2.2 FUNCTION that gives out (columns corresponding to its type ',') in SQL data types: 
# EXAMPLE: date DATE, 
#          open NUMERIC, 
#          name VARCHAR,

def to_sql(df, map_dict):
    cols_map= zip(df.columns, df.dtypes.replace(map_dict))
    sql_cols= ", ".join("{} {}".format(n, d) for (n, d) in cols_map)
    return sql_cols


# 3- Function using query script to create the table on Postgessql
def table_create(table_name , sql_cols):
    cursor.execute(f"DROP TABLE IF EXISTS {table_name};")
    query = f""" 
            CREATE TABLE {table_name } (
            {sql_cols}
            )
            """
    cursor.execute(query)
    print("table created")
    
# 4- Function to convert the DF to csv on the RAM and copy it to the corresponding table
def upload(df, table_name ):
    schema_name = 'public'
    csv_file = io.StringIO()
    df.to_csv(csv_file, header = df.columns, index = False, encoding = 'utf-8')
    csv_file.seek(0)
    sql_statement = f"""
        COPY {schema_name}.{table_name} FROM STDIN WITH 
            CSV
            HEADER
            DELIMITER AS ','
        """
    cursor.copy_expert(sql=sql_statement, file=csv_file)
    csv_file.close()


##################  CONNECTION TO AWS_DB   #################
db_endpoint = "postgres-1.clmlqirmvrik.eu-central-1.rds.amazonaws.com"
db_port = 5432
db_name = "OPA_project"
db_user = "postgres"
db_password = "datascientest"


connection = psycopg2.connect(
    host=db_endpoint,
    port=db_port,
    dbname=db_name,
    user=db_user,
    password=db_password
)
cursor = connection.cursor()


########## Run the entire thing

# 5- IF connection is TRUE perform the following
if connection:

    big_df= pd.DataFrame()

    #Iterating over the list of symbols
    for symbol in symbols:
     
      df = ticker_data(symbol)
      big_df = pd.concat([big_df, df], ignore_index=True)

    print(big_df)
    big_df.to_csv('~/Downloads/crypto_data_output_file.csv', index = False, encoding='utf-8', header= True)
    sql_cols = to_sql(big_df, map_dict)          # Use sql_col function to to map the the SQL type of each column
    table_create(table_name, sql_cols)           # Create the table by SQL query ON AWS-Postgressql
    upload(big_df, table_name )                  # Upload the data to the created table ON AWS
    connection.commit()
    cursor.close()
    connection.close()
else:
    print("Connection to db error, please fix!")

