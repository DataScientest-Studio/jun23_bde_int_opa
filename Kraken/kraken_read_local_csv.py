import pandas as pd

# Define the chunk size (adjust as needed)
chunksize = 10000

pair_name = "AAVEUSD"

# Open the CSV file using with open
file_name = f"Kraken_Trading_History/{pair_name}.csv"

# we read in chunks to do it fast
with open(file_name,'r') as file:
    # Create an empty list to store the chunks
    chunks = []

    # Iterate over the file in chunks
    for chunk in pd.read_csv(file, chunksize=chunksize):
        # Process the chunk as needed
        chunks.append(chunk)

# Concatenate the chunks into a single DataFrame
df = pd.concat(chunks)

# Display the top 10 rows of the DataFrame
print(df.head(10))
