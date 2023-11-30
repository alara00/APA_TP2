# Imports
import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import pickle
from matplotlib import pyplot
#%%
with open('sarimax_model.pickle', 'rb') as model:
    modelo = pickle.load(model)
    
# Write a page title
st.title('Prediccion de volumen de equipos')

df = pd.read_excel('LPG 28-11 [RE-GEO].xlsx')

inicio = st.date_input('Fecha Inicio', value = None, min_value = datetime.strptime("20231101", "%Y%m%d"), format= "YYYY-MM-DD")
fin = st.date_input('Fecha Fin', value = None, min_value = datetime.strptime("20231102", "%Y%m%d"), max_value = datetime.strptime("20231231", "%Y%m%d"), format= "YYYY-MM-DD")

#%%
# Definir la fecha inicial
fecha_inicial = datetime(2023, 11, 1)

# Crear un rango de fechas para los próximos 6 meses
rango_fechas = [fecha_inicial + timedelta(days=i) for i in range(6 * 30)]

# Crear un DataFrame con las fechas
dfdias = pd.DataFrame({'Fecha': rango_fechas})

dfdias.set_index('Fecha', inplace=True)
#%%
dfdias['dia_de_la_semana'] = dfdias.index.dayofweek.astype('int')  # 0 para lunes, 1 para martes, ..., 6 para domingo
dfdias['semana_del_año'] = dfdias.index.isocalendar().week.astype('int')
dfdias['mes'] = dfdias.index.month.astype('int')
#%%
# Obtener las predicciones para el conjunto de prueba
if inicio == None:
    predicciones = modelo.get_forecast(start="2023-11-01", end="2023-12-01", exog=dfdias[['dia_de_la_semana', 'semana_del_año', 'mes']])
else:
    predicciones = modelo.get_forecast(start=inicio, end=fin, exog=dfdias[['dia_de_la_semana', 'semana_del_año', 'mes']])
    
pyplot.plot(predicciones.predicted_mean, color='red')
pyplot.show()
