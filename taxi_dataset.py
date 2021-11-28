import pandas as pd

taxi_data = pd.read_csv('C:/Users/17302261195/Desktop/\
Laboratory_Work/2021_11_05/\
taxi_dataset/train.csv')
pd.set_option('display.max_columns', None)   #展开列
print(taxi_data)

