# TFMkschool

Objetivo del estudio

El estudio tiene por finalidad hacer un análisis de las variables que mantienen una mayor correlación con la varianza de la Capitalización Bursátil de una empresa de un año para otro.

Entendemos que, dependiendo de la industria, estas variables serán diferentes, ya que los modelos de negocios son distintos.
Se utilizará la siguiente fuente de Datos para obtener los datos financieros históricos de más de 1.000 empresas que cotizan en el mercado bursátil.
- Cuenta premium Thomson Reuters.

#Metodología de Trabajo

Este estudio está dividido en diversas fases, desde la extracción del dato, la limpieza y estructuración del mismo, el estudio de las variables y la creación de modelos predictivos y la visualización final.

#1. La extracción del dato
Se ha realizado a través de una herramienta de RPA llamada UiPath.
La función de esta herramienta ha sido la de hacer estas actividades de manera automática:
- Entrar en mi cuenta de Thomson Reuters utilizando mi usuario y mi contraseña.
- Buscar en el buscador de la página web la empresa que queríamos analizar. (Se le pasa una lista por excel con las distintas empresas).
- Ir haciendo clicks en la aplicación de Thomson hasta llegar a los datos financieros.
- Seleccionar la modalidad de los datos, la periodicidad, etc.
- Descargar los datos en formato Excel a una ruta dada.
- Buscar otra empresa y ejecutar el mismo proceso.

Gracias a esta herramienta, he podido descargar de la página web de Thomson Reuters los datos financieros de un total de 1.066 empresas.


#
