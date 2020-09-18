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

4. 



