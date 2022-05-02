import pandas as pd

df = pd.read_csv('/Users/chris/Documents/Research/data/[DATA] 2nd-order transaction network of phishing nodes/Non-phishing/Non-phishing first-order nodes/0x0000000000000000000000000000000000000000.csv')
l = []

# Sum total 'Values' for each unique address
unique_addresses = df['From'].unique()
for i in range(len(unique_addresses)):

    val = df[df['From']==unique_addresses[i]]['Value']
    print(val)

    sum = df[df['From']==unique_addresses[i]]['Value'].sum()
    rec = {'From': unique_addresses[i], 'Value': sum}
    l.append(rec)

# print(l)  

