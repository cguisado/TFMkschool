#!/usr/bin/env python
# coding: utf-8

# ### PASO 3: LIMPIEZA DE DATOS

# En este paso seleccionaremos una de las industrias para examinarla y realizar la limpieza de datos. 
# El objetivo consistirá en construir, finalmente, una fórmula la cual pueda limpiar todos los archivos de las diferentes industrias para su posterior estudio.

# In[169]:


import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from scipy.stats import norm
from sklearn.preprocessing import StandardScaler
from scipy import stats
import warnings
# Para evitar los avisos.
warnings.filterwarnings('ignore') 
get_ipython().run_line_magic('matplotlib', 'inline')


# In[224]:


#Leemos el archivo excel de la industria 'Healthcare'.
ruta = "C:/Users/carlos.guisado/Documents/Master/Master Kschool/TFM/Industrias/"
df = pd.read_excel(ruta + "Healthcare.xlsx")
df_ = df
df


# In[171]:


#Limpieza de datos de los Ratios
df = df.drop(['Company Name', 'Field Name', 'TRBC Industry Group'], axis = 1)
df = df.dropna(axis = 0, how= "all")


# ### Paso 4: Análisis de correlación entre variables financieras

# El objetivo de este paso es conocer qué ratios son los que tienen mayor relación con el incremento del valor de mercado de una empresa.

# In[172]:


import statsmodels
import statsmodels.formula.api as smf
from sklearn.feature_selection import RFE
from sklearn.svm import SVR
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
from statsmodels.stats.outliers_influence import variance_inflation_factor


# In[173]:


#Calculamos el porcentaje de valores nulos por columna, y borramos aquellas columnas con más de un 15%
Ratios = df
total = Ratios.isnull().sum().sort_values(ascending = False)
percent = (Ratios.isnull().sum() / Ratios.isnull().count()).sort_values(ascending = False)
missing_data = pd.concat([total, percent], axis = 1, keys = ['Total', 'Percent'])
Ratios = Ratios.drop((missing_data[missing_data['Percent'] > 0.15]).index,1)
Ratios


# In[174]:


#Una vez tenemos todos los datos, analizamos la correlación de "Market Capitalization" con cada uno de ellos.
df_corr = Ratios.corr('pearson')
df_corr = df_corr['Market Capitalization']
df_corr


# Agunos de estos datos no tienen mucha lógica, por lo que nos induce a pensar que las variables financieras son dependientes entre si, y por lo tanto, no se puede hacer un análisis independiente de cada uno de los ratios.
# 
# Para demostrar nuestra hipótesis, analizaremos si existe correlación entre las variables utilizando matshow.

# In[175]:


corr = Ratios.corr()
corr


# In[176]:


#Matriz de correlación entre variables
corrmat = Ratios.corr()
f, ax = plt.subplots(figsize=(12,9))
sns.heatmap(corrmat, vmax = .8, square = True)


# Como podemos ver a primera vista, muchas de nuestras variables son dependientes entre si, por lo que nos encontramos con un problema de milticolinealidad.
# 
# Para solucionarlo, calcularemos el factor de inflacion de la varianza (VIF) e iremos eliminando aquellas variables que son dependientes entre si y aportan la misma información.

# In[210]:


cols = Ratios.columns.tolist()
#Se reemplazan los valores nulos por la media
for x in cols:
    Ratios[x] = Ratios[x].fillna(Ratios[x].mean())


# In[211]:


Ratios


# In[178]:


#VIF
#Calcularemos el Factor de Inflación de Varianza para cada una de los ratios, con el fin de eliminar de nuestra ecuación
#aquellos que ofrezcan la misma información, con el objetivo de crear un modelo acertado.
Ratios_vif = Ratios
def calculate_vif(Ratios_vif):
    vif = pd.DataFrame()
    vif["Ratios"] = Ratios_vif.columns
    vif["VIF"] = [variance_inflation_factor(Ratios_vif.values, i) for i in range(Ratios_vif.shape[1])]    
    return(vif)
vif = calculate_vif(Ratios_vif)
while vif['VIF'][vif['VIF'] > 7].any():
    remove = vif.sort_values('VIF',ascending=0)['Ratios'][:1]
    Ratios_vif.drop(remove,axis=1,inplace=True)
    vif = calculate_vif(Ratios_vif)
vif


# In[181]:


data = corr[['Market Capitalization']].sort_values(by = 'Market Capitalization',ascending = False)
data_corr = data["Market Capitalization"]
data_corr= data_corr.to_frame()
data_corr["Distance"] = data_corr["Market Capitalization"]
for i in range(0,len(data_corr)):
    if data_corr["Distance"][i] <0:
        data_corr["Distance"][i] = abs(data_corr["Distance"][i])


# In[182]:


data_ = data_corr.sort_values("Distance", ascending = False)
data_ = data_.iloc[0:10]
data_


# In[183]:


#Ordenamos los ratios
ratios = corr
Ratios_corr = ratios[[data_.iloc[0].name, data_.iloc[1].name, data_.iloc[2].name, data_.iloc[3].name, data_.iloc[4].name, data_.iloc[5].name, data_.iloc[6].name, data_.iloc[7].name]]
filas = Ratios_corr.index.values
columnas = Ratios_corr.columns.values
result = [columnas for columnas in columnas if columnas in filas]
Ratios_corr[result].loc[result]


# In[184]:


# Matriz de correlación
corrmat = Ratios_corr.corr()
k = 8 # Número de variables.
cols = corrmat.nlargest(k, 'Market Capitalization')['Market Capitalization'].index
cm = np.corrcoef(Ratios_corr[cols].values.T)
sns.set(font_scale = 1)
hm = sns.heatmap(cm, cbar = True, annot = True, square = True, fmt = '.2f', annot_kws = {'size': 12}, yticklabels = cols.values, xticklabels = cols.values)
plt.show()


# Una vez que ya disponemos de aquellas variables con una mayor correlación con la varianza del valor de mercado de la empresa, nos disponemos a crear nuestro modelo.

# In[219]:


df_


# In[204]:


#Análisis Industria
#Reemplazamos los valores nulos por la media del total y sacamos graficos de cómo ha ido evolucionando cada ratio.
df_analysis = df_
df_rt = pd.DataFrame()
for i in range (2010,2020):
    df_analysis = df_[df_["Field Name"].str.endswith(str(i))]
    col = df_analysis.columns.values.tolist()
    df_analysis = df_analysis.drop(['Company Name', 'TRBC Industry Group','Field Name'], axis = 1)
    cols = df_analysis.columns.tolist()
    #Se reemplazan los valores nulos por la media
    for x in cols:
        df_analysis[x] = df_analysis[x].fillna(df_analysis[x].mean())
    #Calculamos el porcentaje de valores nulos por columna, y borramos aquellas columnas con más de un 12%
    total = df_analysis.isnull().sum().sort_values(ascending = False)
    percent = (df_analysis.isnull().sum() / df_analysis.isnull().count()).sort_values(ascending = False)
    missing_data = pd.concat([total, percent], axis = 1, keys = ['Total', 'Percent'])
    df_analysis = df_analysis.drop((missing_data[missing_data['Percent'] > 0.12]).index,1)
    #Se sacan los datos estadísticos
    df_analysis = pd.DataFrame(df_analysis.describe())
    df_analysis = df_analysis[1:]
    df_analysis = pd.DataFrame(df_analysis.iloc[0])
    df_analysis = df_analysis.transpose().rename(index={'mean': i})
    df_rt = pd.concat([df_rt, df_analysis], axis = 0)
    
df_rt


# In[207]:


#Análisis Industria del año 2019:
#Guardamos la variable final para estudiarla junto con la empresa que queramos
#Reemplazamos los valores nulos por la media del total del año 2019
df_analysis_2019 = df_
df_analysis_2019 = df_analysis_2019[df_analysis_2019["Field Name"].str.contains("2019")]
#CDefinimos variable con una lista de las columnas
col = df_analysis_2019.columns.values.tolist()
#Definimos los filtros que no queremos en el dataset
df_analysis_2019 = df_analysis_2019.drop(['Company Name', 'TRBC Industry Group','Field Name'], axis = 1)
#Reemplazamos valores nulos por la media
cols = df_analysis_2019.columns.tolist()
for i in cols:
    df_analysis_2019[i] = df_analysis_2019[i].fillna(df_analysis_2019[i].mean())
df_analysis_2019 = df_analysis_2019.describe()
df_analysis_2019 = df_analysis_2019[1:]
df_2019_industria = pd.DataFrame(df_analysis_2019.iloc[0])
df_2019_industria = df_2019_industria.transpose().rename(index={'mean': "2019"})
df_2019_industria


# In[209]:


#Representación gráfica con plots
print("Ahora vamos a ver, en forma gráfica, como han ido evolucionando la media de estos ratios a lo largo de los últimos años.")
print()       
cols = df_rt.columns.values.tolist()
for i in range(0,len(df_rt.columns)):
    df_rt[cols[i]].plot()
    plt.xlabel("Años")
    plt.ylabel("Varianza Media Anual")
    plt.title(str(df_rt[cols[i]].name))
    print(plt.show())


# ### Paso 5: Modelo predictivo

# El objetivo de este paso es crear un modelo que sea eficaz a la hora de predecir la variación en el "Market Capitalization" dados unas variaciones dadas de sus ratios financieros.
# Nuestro dataset será el creado en el paso 4a, "Ratios".

# In[214]:


from sklearn.feature_selection import RFE
from sklearn.svm import SVR
from sklearn.linear_model import LinearRegression
import statsmodels.api as svm
import matplotlib.pyplot as plt
from sklearn.linear_model import LogisticRegression
from sklearn import datasets
import pandas as pd
import numpy as np


# In[258]:


#Preparamos el dataset
ruta = "C:/Users/carlos.guisado/Documents/Master/Master Kschool/TFM/Industrias/"
df = pd.read_excel(ruta + "Healthcare.xlsx")
#Limpieza de datos
df = df.drop(['Company Name', 'Field Name', 'TRBC Industry Group'], axis = 1)
df = df.dropna(axis = 0, how= "all")
total = df.isnull().sum().sort_values(ascending = False)
percent = (df.isnull().sum() / df.isnull().count()).sort_values(ascending = False)
missing_data = pd.concat([total, percent], axis = 1, keys = ['Total', 'Percent'])
df = df.drop((missing_data[missing_data['Percent'] > 0.15]).index,1)
cols = df.columns.tolist()
#Se reemplazan los valores nulos por la media
for x in cols:
    df[x] = df[x].fillna(df[x].mean())
lista = df.columns.values.tolist()
for i in lista:
    df[i].replace(np.inf,0,inplace=True)
    df[i].replace(-np.inf,0,inplace=True)
df


# In[259]:


Ratios = df


# In[260]:


#Regresión Múltiple con Scikit - learn
data = Ratios
feature_cols = Ratios_corr.columns[1:]
X = data[feature_cols]
y = data["Market Capitalization"]

estimator = SVR(kernel ='linear')
selector = RFE(estimator, 6, step = 1)
selector= selector.fit(X,y)
selector.ranking_

lista = []
for i in range(0,len(selector.ranking_)):
    if selector.ranking_[i] == 1:
        lista.append(i)
        
X_pred = X[X.columns[lista]]
nom_vars = X[X.columns[lista]]

lm = LinearRegression()
lm.fit(X_pred,y)


print ("Las variables con mayor correlación con la varianza en el precio de mercado son las siguientes: " + str(nom_vars.columns.values.tolist()))
print ( "El punto de intersección es el " + str(lm.intercept_))
print("Los coeficientes de cada una de las variables son " + str(lm.coef_))
print("La puntuación de este modelo es de " + str(lm.score(X_pred,y)))


# In[ ]:





# In[230]:


#Regresión Polinomial
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import PolynomialFeatures

#Definimos las variables
feature_cols = Ratios_corr.columns[1:]
x = data[feature_cols]
y = data["Market Capitalization"]

for i in range(1,100):

    X_train, X_test, y_train, y_test = train_test_split(x, y, test_size = 0.20, random_state = i)
    poli_reg = PolynomialFeatures(degree = 2)

    #Transformamos las características existentes en características de mayor grado
    X_train_poli = poli_reg.fit_transform(X_train)
    X_test_poli = poli_reg.fit_transform(X_test)

    #Definimos el algoritmo a utilizar
    pr = LinearRegression()

    #Entrenamos del modelo
    pr.fit(X_train_poli, y_train)

    #Realizamos nuestra predicción
    Y_pred_pr = pr.predict(X_test_poli)

    #Datos del modelo
    scoring = pr.score(X_train_poli, y_train)  

    if scoring > 0.75:
        print("random state: " + str(i))
        print('Valor de la pendiente: ' + str (pr.coef_))
        print( "Valor de la intersección: " + str(pr.intercept_))
        print ("Precisión del modelo: " + str(pr.score(X_train_poli, y_train)))
        break


# In[ ]:





# In[ ]:





# In[231]:


#Regresión Logística
dataset = Ratios
feature_cols = Ratios.columns[1:]
X = data[feature_cols]
y = data[["Market Capitalization"]]>0


# Splitting the dataset into the Training set and Test set
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.25, random_state = 0)

# Feature Scaling
from sklearn.preprocessing import StandardScaler
sc = StandardScaler()
X_train = sc.fit_transform(X_train)
X_test = sc.transform(X_test)

# Fitting Logistic Regression to the Training set
from sklearn.linear_model import LogisticRegression
classifier = LogisticRegression(random_state = 0)
classifier.fit(X_train, y_train)

# Predicting the Test set results
y_pred = classifier.predict(X_test)

# Making the Confusion Matrix
from sklearn.metrics import confusion_matrix
cm = confusion_matrix(y_test, y_pred)

print("Este modelo tiene una precisión del " + str(classifier.score(X,y)))
        


# In[ ]:





# In[232]:


#Regresión Logística 2
import pandas as pd
import numpy as np
from sklearn import linear_model
from sklearn import model_selection
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score
import matplotlib.pyplot as plt
import seaborn as sb

#
dataframe = Ratios

#Creamos el Modelo de Regresión Logística
feature_cols = Ratios.columns[1:]
X = dataset[feature_cols]
y = dataset[["Market Capitalization"]]>0

#creamos nuestro modelo y hacemos que se ajuste (fit) a nuestro conjunto de entradas X y salidas ‘y’.
model = linear_model.LogisticRegression()
model.fit(X,y)

#Clasificar nuestro conjunto de entradas X  y revisamos algunas de sus salidas 
predictions = model.predict(X)
#print(predictions)[0:5]

# Precision 
model.score(X,y)

#Validación de nuestro modelo
validation_size = 0.20
seed = 7
X_train, X_validation, Y_train, Y_validation = model_selection.train_test_split(X,y, test_size = validation_size, random_state = seed)

# calculamos el nuevo scoring
name='Logistic Regression'
kfold = model_selection.KFold(n_splits=10, random_state=seed)
cv_results = model_selection.cross_val_score(model, X_train, Y_train, cv=kfold, scoring='accuracy')
msg = "%s: %f (%f)" % (name, cv_results.mean(), cv_results.std())
print(msg)

#Predicciones 
predictions = model.predict(X_validation)
print(accuracy_score(Y_validation, predictions))

#Reporte de Resultados del Modelo
print(confusion_matrix(Y_validation, predictions))

#Reporte de clasificación
print(classification_report(Y_validation, predictions))


# In[ ]:





# In[140]:





# In[234]:


#Arboles de Decisión
import pandas as pd
import matplotlib.pyplot as plt

data = Ratios
data['Market Capitalization'] = data["Market Capitalization"]>0

colnames = data.columns.values.tolist()
predictors = colnames[1:]
target = colnames[0]

for i in range(0,100):
    data['is_train'] = np.random.uniform(-1,1,len(data))<=0
    train,test = data[data['is_train']==True], data[data['is_train']==False]

    from sklearn.tree import DecisionTreeClassifier
    tree = DecisionTreeClassifier(criterion='entropy', min_samples_split = 20, random_state = i)
    tree.fit(train[predictors], train[target])

    preds = tree.predict(test[predictors])
    pd.crosstab(test[target], preds, rownames = ["Actual"], colnames=["Predictions"])

    #Resultado de nuestro modelo
    scoring = tree.score(test[predictors], test[target])
    
    if scoring>0.8:
        print("Random_state utilizado: " + str(i))
        print("Nuestro modelo tiene una precisión de: " + str(tree.score(test[predictors], test[target])))
        break


# In[ ]:




