import glob
import os
import pandas as pd

# Read in ticker list
inFile = open('tickerList.txt', 'r')
tickerList = inFile.read()
tickerList = tickerList.split(', ')

# Change directory to FTD data
os.chdir('./FTD Data')
directory = os.getcwd()

for ticker in tickerList:
    # Join CSV files in directory
    csvFiles = glob.glob(os.path.join(directory, '*.txt'))

    # Read files into Panda DF, filtering by ticker
    dataframes = []
    for csvFile in csvFiles:
        df = pd.read_csv(csvFile, delimiter='|', error_bad_lines=False)
        filtered = df[df['SYMBOL']==ticker]
        dataframes.append(filtered)

    # Concatenate dataframes into one file object
    result = pd.concat(dataframes, ignore_index=True)

    # Deleting unneccessary columns
    del result['CUSIP']
    del result['DESCRIPTION']
    del result['PRICE']

    # Formatting dates
    result['SETTLEMENT DATE'] = result['SETTLEMENT DATE'].astype(str).astype(int)
    result['SETTLEMENT DATE'] = pd.to_datetime(result['SETTLEMENT DATE'], format = '%Y%m%d')

    # Write to new CSV file
    os.chdir('../Outputs')
    result.to_csv('%s_output.csv' %ticker)
    os.chdir('../FTD Data')
