import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('temp_data.csv')
df.plot(x="Time", y="Celsius")
plt.show()
