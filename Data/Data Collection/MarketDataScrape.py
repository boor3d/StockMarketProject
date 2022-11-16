import os

# Test environment I am in the Main Directory

# File path
file_path = os.listdir("Data/csv/")


# Create List of all tickers in the S&P 500 for records
# Iterate through directory to collect tickers 
ticker_list = []

def ticker_record(path):
    for x in path:
        if x.endswith(".csv"):
            # Slice .csv for list
            ticker_list.append(x[:-4])
    print(ticker_list)

def write_to_file (l):
    with open ("Data/Data Collection/SnP500_list.txt", "w") as f:
        for stock in l:
            f.write(f"{stock}\n")


ticker_record(file_path)
write_to_file(ticker_list)