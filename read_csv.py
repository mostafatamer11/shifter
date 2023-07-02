import pandas as pd

df = pd.read_csv("input.csv")

COLUMNS = [df.columns[x].strip() for x in range(len(df.columns))]
LOW_COLUMNS = [df.columns[x].lower().strip() for x in range(len(df.columns))]

