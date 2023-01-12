import pandas as pd

path = 'E:/CARLA_0.9.5/PythonAPI/MyProject/'
columns = ['Center', 'Throttle', 'Steering', 'Brake', 'Gear']

#Reading the csv file
data = pd.read_csv((path+'raw_driving_log.csv'), names=columns)
#Droping the rows containing NaN values
df = data.apply (pd.to_numeric, errors='coerce')
df = df.dropna()
# print (df)
# df.to_csv('out2.csv',index=False)
#Droping the unexpected values
df_new = df[df['Center'] != 100000000]
df_new.to_csv('final_driving_log.csv',index=False)