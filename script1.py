import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt 
from pandas import read_csv

dt = read_csv('sofiaxt-escuelaExamenes.csv')
#print(dt)
del dt['IdEvaluacion']
dt = dt.replace(np.nan, '0', regex=True)
print(dt)

def duracion_to_float(duracion_str):
    return float(duracion_str) / 3600

def convert_to_float(strValue):
    return float(strValue) 

#convierte los valores de las dos columnas a analizar a float
#en la duracion del tiempo se convierte a horas para que la escala en la grafica sea mas cercana a la calificacion
dt['DuracionSegundos'] = dt['DuracionSegundos'].apply(duracion_to_float)
dt['Califiacion'] = dt['Califiacion'].apply(convert_to_float)

dt = dt[dt.DuracionSegundos != 0]
#dt = dt[dt.Califiacion != 0]
print(dt)
d = dt.describe()
print(d)

#grafica los valores con outliers
dt.boxplot(return_type='dict')
plt.show()


#print(dt_filtered)

def find_anomalies(data, strColumn):
    #Settea el limite superior e inferior segun la deviacion estandar
    anomalies = []
    data_std = data[strColumn].std()
    data_mean = data[strColumn].mean()
    anomaly_cut_off = data_std * 2
    lower_limit  = data_mean - anomaly_cut_off 
    upper_limit = data_mean + anomaly_cut_off
 
    # Genera los outliers
    for index, row in data.iterrows():
        outlier = row[strColumn] # # obtiene el valor de la columna a analizar
        if (outlier > upper_limit) or (outlier < lower_limit):
            anomalies.append(index)
    return anomalies

#elimina los rows que contienen los outliers
def deleteAnomalies(df, a):
    for i in range(0,len(a)):
        df.drop([a[i]], inplace=True)

    return df

a = find_anomalies(dt,'DuracionSegundos')
dt = deleteAnomalies(dt,a)
print(dt)
b = find_anomalies(dt,'Califiacion')
print(b)
dt = deleteAnomalies(dt,b)

print(dt)

#grafica sin outliers
dt.boxplot(return_type='dict')
plt.show()
