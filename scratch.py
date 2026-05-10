import pandas as pd
import numpy as np

df = pd.read_csv('Company_X_Audience.csv')

def count_outliers(col):
    Q1 = df[col].quantile(0.25)
    Q3 = df[col].quantile(0.75)
    IQR = Q3 - Q1
    upper = Q3 + 1.5 * IQR
    lower = Q1 - 1.5 * IQR
    return ((df[col] < lower) | (df[col] > upper)).sum()

print("Merch Outliers:", count_outliers('Merchandise_Spend'))
print("Drink Outliers:", count_outliers('Drink_Spend'))
print("Max Total Spend:", (df['Ticket_Price'] * df['Num_Tickets'] + df['Merchandise_Spend'] + df['Drink_Spend']).max())

