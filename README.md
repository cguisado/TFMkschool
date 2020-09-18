# Data Science aplicado a los mercados financieros

# Objetivo del estudio

El estudio tiene por finalidad hacer un análisis de las variables que mantienen una mayor correlación con la varianza de la Capitalización Bursátil de una empresa de un año para otro.

Entendemos que, dependiendo de la industria, estas variables serán diferentes, ya que los modelos de negocios son distintos.
Se utilizará la siguiente fuente de Datos para obtener los datos financieros históricos de más de 1.000 empresas que cotizan en el mercado bursátil.
- Cuenta premium Thomson Reuters.

# Metodología de Trabajo

Este estudio está dividido en diversas fases, desde la extracción del dato, la limpieza y estructuración del mismo, el estudio de las variables, la creación de modelos predictivos y la visualización final.


### 1. La extracción del dato
Se ha realizado a través de una herramienta de RPA (Robotics) llamada UiPath.
La función de esta herramienta ha sido la de hacer las siguientes actividades de manera automática:
- Entrar en mi cuenta de Thomson Reuters utilizando mi usuario y mi contraseña.
- Buscar en el buscador de la página web la empresa que queríamos analizar. (Se le pasa una lista por excel con las distintas empresas).
- Ir haciendo clicks en la aplicación de Thomson hasta llegar a los datos financieros.
- Seleccionar la modalidad de los datos, la periodicidad, etc.
- Descargar los datos en formato Excel a una ruta dada.
- Buscar otra empresa y ejecutar el mismo proceso.

Gracias a esta herramienta, hemos podido descargar de la página web de Thomson Reuters los datos financieros de un total de 1.066 empresas.

Se adjunta código UiPath. Archivo ("Thomsonv2.xaml").
PD: No se va a poder replicar el código, ya que tengo la variables del usuario y contraseña de Thomson Reuters guardados como credenciales en mi ordenador, y accedo a ellas a través de UiPath como variables para ponerlas en la página web.



### 2. Estructuración del dato
Los datos previamente descargados en UiPath no se encuentran estructurados, y son 1066 archivos diferentes. Hemos utilizado código VBA para recoger los datos financieros que nos interesaban de cada una de las empresas, guardando dichos datos en una pestaña con el nombre de "FinancialData".

Con este paso, conseguimos estructurar los datos financieros de cada una de las empresas. 

Se han realizado dos código diferentes. En el primero de ellos se consigue hacer la reestructuración de uno de los archivos. El segundo código es una llamada al primero dentro de un bucle for para que vaya recorriendo una ruta dada y estructurando todos los archivos. Si se quiere replicar, hay que fijarse en la variable "ruta" de este segundo código, ya que he trabajado en local.

Se adjunta código VBA de dos maneras:
  - Archivo "TFM_Kschool.xlsm" : el archivo está en blanco. El código se encuentra en dos módulos dentro del programador de VBA.
  - Archivos ".txt". Cada uno de ellos es un código distinto.

Al ser 1.066 empresas, no es posible subirlas todas en la misma carpeta de github. Adjunto una carpeta de prueba con distintos datsets individuales de empresas.

### 3. Limpieza del dato
Desde aquí, el lenguaje de programación a utilizar es el de python. Se han dejado archivos ".py" con el código en la carpeta "Python", al igual que también se ha subido el código a través de GitHub. Forman parte de este paso los siguientes módulos:
- 01 - Concatenación de datasets.
- 02 - Limpieza de datos, generación de variables y clasificación por industrias.

En el primer paso, el objetivo es el de concatenar todos los archivos excel de cada una de las empresas descargadas a un archivo común para poder trabajar con el. 
Este archivo se llamará "df.xlsx", el cuál se adjunta también en el repositorio. Hay que tener en cuenta que, al comenzar el código en este primer paso, declaro una variable como "path" y "archivo", las cuales deberían cambiar si se quiere replicar.

En el segundo paso, los objetivos son los siguientes:
- A partir de los datos financieros recopilados, crear un nuevo DataFrame en el que añadir los ratios financieros que queremos analizar. Para calcular algunos ratios ha sido necesario operar con distintos datos financieros a través de fórmulas financieras simples.
- Calcular, por cada uno de los ratios, la varianza que ha tenido con respecto al año anterior. Dado que el objetivo final del proyecto es analizar la correlación de los ratios con la varianza en el precio de mercado de una empresa de un año para otro, ha sido necesario este cálculo.
- Dividir el dataset resultante con todos los ratios entre tantas industrias como queramos analizar. Cada industria se guardará en un dataset en una ruta dada.
Este segundo paso lo comienzo abriendo uno de los archivos que adjuntopara que sea más fácil de replicar si se quiere. "df.xlsx".

### 4. Análisis de correlación entre variables financieras
El módulo en el que se hace este análisis es llamado "03 - Análisis de Datos". El objetivo de este paso es conocer qué ratios son los que tienen mayor relación con el incremento del valor de mercado de una empresa. Leemos el archivo de la industria utilizando una variable "ruta", la cual debería cambiar si se quiere replicar el código. 

Al hacer un primer análisis de la industria, nos damos cuenta que existe un problema de multicolinealidad entre las variables. Es decir, existen variables las cuales son dependientes entre sí y aportan la misma información al estudio.

La manera de solucionarlo es con un estudio del factor de inflación de la varianza. Aquellas variables con un alto "VIF" serán eliminadas de nuestro modelo, con el objetivo de conocer cuáles son aquellas con mayor correlación con respecto al "Market Value" e independencia entre las mismas.

Una vez ya tenemos los ratios correctos, los ordenamos y realizamos una matriz de correlación con respecto a la varianza de un año a otro en "Market Capitalization".

Para analizar la industria más profundamente, crearemos un dataframe con la media de los ratios durante los últimos años, para así, con un único vistazo, conocer cómo se está comportando la industria.



### 5. Modelos predictivos

El objetivo de este paso es crear un modelo que sea capaz de predecir la variación en el "Market Capitalization" dados unas variaciones dadas de sus ratios financieros.
El modelo predictivo se hará con cada dataset de la industria.
Los modelos que se han realizado son los siguientes:
- Regresión múltiple.
- Regresión Polinomial.
- Regresión Logística. Esta regresión devuelve si debería haber subido o bajado el valor en bolsa de acuerdo al movimiento de sus ratios financieros, pero no intenta predecir el porcentaje exacto de subida o bajada. 
- Árbol de decisión.



### 6. Visualización

La visualización consiste en aplicar todo lo realizado anteriormente a través de dos fórmulas:

- Formula 1: analysis_industria(industria)
  En esta fórmula hay que introducir el nombre de uno de los archivos de la industria que queramos analizar. Leemos el archivo de la industria utilizando una variable "ruta", la cual debería cambiar si se quiere replicar el código. Te devuelve lo siguiente:
    - Número de empresas en la industria.
    - Número de ratios que se pueden analizar. No se pueden analizar todos ya que las variables no son independientes entre si, como hemos comentado antes sobre el problema de   la multicolinealidad.
    - La evolución de los ratios de la industria en el tiempo.
    - Matriz de correlación de los ratios financieros con respecto a la varianza del "Market Capitalization".
    - Lista con las variables financieras con mayor relevancia.
    
 - Formula 2: analysis_empresa(empresa)
   El parámetro a pasar es el nombre de una de las empresas que tengamos dentro de nuestro Dataset. El nombre no tiene por qué estar al completo. El archivo que se lee al comenzar la definición de esta formula es el de "Ratios.xlsx", archivo el cual adjunto para que sea más fácil replicarlo si así se desea.  La función te devuelve lo siguiente:
     - Análisis de la industria a la que pertence la empresa (fórmula anterior).
     - Análisis de los ratios en el último año (2019).
     - Comparativa entre los ratios de la industria y los ratios de la empresa.
     - Resultados de los modelos predictivos.
     
    

# Datasets

Se incluyen los siguientes archivos.

1. "Tickers_1.0.xlsx" : Fuente de información desde donde he extraído los nombres de las empresas que se analizan en el estudio. Pestaña "USA".
2. Carpeta "Data": Al no ser posible subir 1.066 archivos, subimos 50 correspondientes a las empresas que se analizan en este estudio como ejemplo.
3. Carpeta Datasets Industrias: Archivos excel correspondiente a la clasificación de las empresas en sus respectivas industrias.
4. "df.xlsx" : Es el resultado de la concatenación de los datos financieros de las 1.066 empresas en un solo archivo.
5. "Ratios.xlsx": En él encontramos todas las empresas con las varianzas de los ratios financieros de un año a otro.
