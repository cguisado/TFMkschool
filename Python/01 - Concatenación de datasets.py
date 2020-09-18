#!/usr/bin/env python
# coding: utf-8

# ## TFM. Paso 1 -  Concatenar Datasets

# Ya que tenemos todos los datasets en archivos excels diferentes, lo primero que haremos será unirlos en un mismo dataframe. Para ello, utilizaremos una función que vaya recorriendo el path donde están guardados todos los archivos y uniéndolos con un concat.

# In[1]:


import pandas as pd
import numpy as np
import os


# In[2]:


path = r"C:/Users/carlos.guisado/Documents/Thomson/Uipath/Descargas/Data/"
archivo = os.listdir(r"C:\Users\carlos.guisado\Documents\Thomson\Uipath\Descargas\Data")


# In[4]:


print("Contamos con " + str(len(archivo)) + " datasets, que equivalen a los datos financieros de " + str(len(archivo)) + " empresas que cotizan en la bolsa americana.")


# In[42]:


#Abrimos el primer excel de todos para comprobar que se ha cargado correctamente.
#Archivo Excel ajuntado en Github - df.xlsx
df = pd.read_excel(r"C:\Users\carlos.guisado\Documents\Thomson\Uipath\Descargas\Data\A.xlsx", sheet_name = "FinancialData")
df.head()


# In[43]:


#Añadimos, utilizando un 'concat', los datos de las demás empresas que queremos analizar, con el 
#objetivo de crear un dataset con todas las empresas y datos financieros.
for i in range (1,len(archivo)):
    file = path + archivo[i]
    temp_data = pd.read_excel(file, sheet_name = "FinancialData")
    df = pd.concat([df, temp_data], axis = 0, ignore_index = True, verify_integrity = True)
df = df.dropna(axis = 1, how = 'all')
df


# In[51]:


print("Tenemos un dataset compuesto por " + str(len(archivo)) + " empresas, con un shape = " + str(df.shape))
print("Esto se debe a que cada empresa, como hemos visto anteriormente al abrir el primero de los archivos, está compuesta por un historial variable de entre 1-10 años.")
print("Dependiendo de la industria, disponemos de unos datos financieros o de otros, por lo que el siguiente paso será la división por industria.")


# In[44]:


df.to_excel('df.xlsx', header=True, index=False)

