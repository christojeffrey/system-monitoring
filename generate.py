import pandas as pd
import random

def initiate():
    return pd.DataFrame(random.random() * 100, index=pd.date_range(start="2024-01-01 00:00:00", periods=1), columns=['Temperature'])

def generate(prev):
    new_index = prev.index[-1] + pd.Timedelta(seconds=1)
    prev.loc[new_index] = 2.3
    prev.loc[new_index] = random.random() * 100

    return prev
    