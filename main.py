import pandas as pd
import os

# Read the CSV file
df = pd.read_csv(os.path.join(os.path.dirname(__file__), 'data', 'sp500_companies.csv'))

print(df.head(3).T)