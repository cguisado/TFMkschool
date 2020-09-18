# TFMkschool

Objetivo del estudio

El estudio tiene por finalidad hacer un análisis de las variables que mantienen una mayor correlación con la varianza de la Capitalización Bursátil de una empresa de un año para otro.

Entendemos que, dependiendo de la industria, estas variables serán diferentes, ya que los modelos de negocios son distintos.
Se utilizará la siguiente fuente de Datos para obtener los datos financieros históricos de más de 1.000 empresas que cotizan en el mercado bursátil.
- Cuenta premium Thomson Reuters.

Metodología de Trabajo

Este estudio está dividido en diversas fases, desde la extracción del dato, la limpieza y estructuración del mismo, el estudio de las variables y la creación de modelos predictivos y la visualización final.


1. La extracción del dato
Se ha realizado a través de una herramienta de RPA llamada UiPath.
La función de esta herramienta ha sido la de hacer estas actividades de manera automática:
- Entrar en mi cuenta de Thomson Reuters utilizando mi usuario y mi contraseña.
- Buscar en el buscador de la página web la empresa que queríamos analizar. (Se le pasa una lista por excel con las distintas empresas).
- Ir haciendo clicks en la aplicación de Thomson hasta llegar a los datos financieros.
- Seleccionar la modalidad de los datos, la periodicidad, etc.
- Descargar los datos en formato Excel a una ruta dada.
- Buscar otra empresa y ejecutar el mismo proceso.

Gracias a esta herramienta, hemos podido descargar de la página web de Thomson Reuters los datos financieros de un total de 1.066 empresas.

Se adjunta código UiPath. 



2. Estructuración del dato
Los datos previamente descargados en UiPath no se encuentran estructurados, por lo que hemos utilizando código VBA para recoger los datos financieros que nos interesaban y guardarlos en una pestaña nueva dentro de cada uno de los archivos de las empresas. A esta pestaña se le da el nombre de "Financial Data".

Con este paso, conseguimos estructurar los datos financieros de cada una de las empresas. Esto se consigue realizando un bucle dentro de una ruta dada.

Se adjunta código VBA.



3. Limpieza del dato
Este paso se realiza a través de python, y forman parte del mismo los siguientes módulos:
- Paso 1 - concatenar.
- Paso 2 - Limpieza de datos, generación de variables y clasificación por industrias.

En el primer paso, el objetivo es el de concatenar todos los archivos excel de cada una de las empresas descargadas a una común para poder trabajar con ella.
Este archivo se llamará df.xlsx, el cuál se adjunta también en el repositorio.

En el segundo paso, los objetivos son los siguientes:
- A partir de los datos financieros recopilados, crear un nuevo DataFrame en el que añadir los ratios financieros que queremos analizar. Para calcular algunos ratios ha sido necesario operar con distintos datos financieros a través de fórmulas financieras simples.
- Calcular, por cada uno de los ratios, la varianza que ha tenido con respecto al año anterior. Dado que el objetivo final del proyecto es analizar la correlación de los ratios con la varianza en el precio de mercado de una empresa de un año para otro, ha sido necesario este cálculo.
- Dividir el dataset resultante con todos los ratios entre tantas industrias como queramos analizar. Cada industria se guardará en un dataset en una ruta dada.



4. Análisis de correlación entre variables financieras
El módulo en el que se hace este análisis es el que se llama "Paso 3-4- Análisis de datos y Modelo predictivo."El objetivo de este paso es conocer qué ratios son los que tienen mayor relación con el incremento del valor de mercado de una empresa.

Al hacer un primer análisis de la industria, nos damos cuenta que existe un problema de colinealidad. Es decir, existen variables las cuales son dependientes enre sí y aportan la misma información al estudio.

La manera de solucionarlo es con un estudio del factor de inflación de la varianza. Aquellas variables con un alto "VIF" serán eliminadas de nuestro modelo, con el objetivo de conocer cuáles son las que mayor correlación, ya sea positiva o negativa, tienen con respecto al "Market Value".

Una vez ya tenemos los ratios correctos, los ordenamos y realizamos una matriz de correlación con respecto a la varianza de un año a otro en "Market Capitalization".

Para analizar la industria más profundamente, crearemos un dataframe con la media de los ratios durante los últimos años, para así, con un único vistazo, conocer cómo se está comportando la industria.



5. Modelos predictivos

El objetivo de este paso es crear un modelo que sea eficaz a la hora de predecir la variación en el "Market Capitalization" dados unas variaciones dadas de sus ratios financieros.
El modelo predictivo se hará con cada dataset de la industria, y se aplicará el algoritmo a la empresa que se pretenda analizar.
Los modelos que se han realizado son los siguientes:
- Regresión múltiple.
- Regresión Polinomial.
- Regresión Logística. Esta regresión devuelve si debería haber subido o bajado el valor en bolsa de acuerdo al movimiento de sus ratios financieros, pero no intenta predecrir el porcentaje exacto de subida o bajada.
- Árbol de decisión



6. Visualización

La visualización consiste en aplicar todo lo realizado anteriormente a través de dos fórmulas:
- Formula 1: analysis_industria(industria)
  En esta fórmula hay que introducir el nombre de uno de los archivos de la industria que queramos analizar. Te devuelve lo siguiente:
    - Número de empresas en la industria.
    - Número de ratios que se pueden analizar. No se pueden analizar todos ya que las variables no son independientes entre si, como hemos comentado antes sobre el problema de   la multicolinealidad.
    - La evolución de los ratios de la industria en el tiempo.
    - Matriz de correlación de los ratios financieros con respecto a la varianza del "Market Capitalization".
    - Lista con las variables financieras con mayor relevancia.
 - Formula 2: analysis_empresa(empresa)
   El parámetro a pasar es el nombre de una de las empresas que tengamos dentro de nuestro Dataset. El nombre no tiene por qué estar al completo. Te devuelve:
     - Análisis de la industria a la que pertence la empresa (fórmula anterior).
     - Análisis de los ratios en el último año (2019).
     - Comparativa entre los ratios de la industria y los ratios de la empresa.
     - Comentario sobre si pensamos que la empresa está infravalorada o sobrevalorada en la actualidad. (El comentario responde al resultado de los modelos predictivos.
     
    









