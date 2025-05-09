import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('temp_data_multiple.csv')
if input("Celsius or Fahrenheit? (c/f)\n") == "f":
    for column in df.columns[1:]:
        df[column] = df[column] * 9/5 + 32
for i in range(1,len(df.columns)):
    df.plot(x="Time", y=df.columns[i], title=df.columns[i]+" vs. Time")
df.plot(x="Time", title="All Temperatures vs. Time")
plt.show()
