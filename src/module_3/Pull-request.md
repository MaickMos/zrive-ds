# Push Notificactions  module #3
En esta PR se hará entrega de un modelo predictivo para posibles personas interesadas en un producto. Dado un usuario y producto, se predice si compraría ese producto si estuvieran comprando en ese momento. Condiciones: los usuarios deben ser aquellos que realizan una compra de mínimo 5 productos. Usar modelo lineal.  


## Preparación del dataset
A Partir del dataset feature_frame se cargaron los datos y se realizaron las modificaciones:


### Filtro para compradores de mas de 5 productos
Se realizó un filtrado para aquellos clientes que en una misma order_id hallan comprado igual o más de 5 productos, permitiendo trabajar el modelo solo con clientes que hayan comprado la cantidad de productos indicadas.


* A Partir de esta división se trabaja con un total de 2.163.953 filas donde el 1.4% son la clase objetivo
### División del dataset
Se intentaron dos formas de división:
1. De manera aleatoria, 10% datos para el testeo, aproximadamente 20% para la validación y un aprox. 80% para entrenamiento.
    Esta forma de división de los datos presenta el problema de que el modelo estará aprendiendo con datos o tendencias del futuro. Factores que directamente afectan al rendimiento del modelo cuando está en producción. Por esta razón se decidió no implementarla.  


2. De manera temporal, donde está seccionado de la siguiente manera:
 * Entrenamiento 70% -   2020-10-05 hasta 2021-02-04
 * Testeo 20%: 2021-02-04 hasta 2021-02-22
 * Validación 10%: 2021-02-22 hasta 2021-03-03
    Como se observa en la gráfica de comportamiento de número de ventas, el comportamiento del mercado presenta un cambio en la forma de comprar de los usuario, afectando directamente en las posibles predicciones del modelo.  
    ![graficas](https://github.com/MaickMos/zrive-ds/blob/686a77aed98b68f3ab4ad15dad5e737b30cef5ff/src/module_3/images/Image_1.png)


### Eliminación de variables
Se eliminaron variables que no aportan al modelo o que de ser implementadas, aumentaban innecesariamente la complejidad sin tener un rendimiento proporcional.
* Variant_Id: ID del producto
* user_id: ID del producto
* created_at: Fecha de creación de la orden de compra
* order_id: Número de la orden hecha
* product_type: categoría del producto
* order_date: Fecha y hora de la compra
* vendor: Nombre del proveedor


### Normalización
Para realizar la estandarizacion de los datos se implemento el StandarScaler(), usando la media y la desviación estándar.


## Métricas de evaluación
### Recall
Dado que el dataset es desbalanceado, siempre que se evalúa el modelo tendrá un porcentaje alto, por esta razón se usará principalmente la métrica de recall, permitiendo medir la proporción de verdaderos positivos.
### precision-recall curve
Por otro lado, para una mejor comprensión y comparación visual se implementa la curva de precision-recall, que compara la precisión con el recall.
### ROC Curve
Es otra curva la cual permite medir el recall o True positive Rate (TPR) y el False positive Rate. Esta curva mostrará un mejor rendimiento cuando la gráfica se acerque a la esquina superior izquierda (1.0,0.0), permitiendo comparar fácilmente entre modelos.


## Modelos
### Baseline
Primero se implementó un modelo básico sin usar algoritmos de machine learning. A partir de métricas ya existentes en el dataset se realizaron las predicciones de compra de cada producto a partir de la variable goblal_popularity. Se implementó una predicción binaria con un umbral de 0.5.
Realizando una predicción básica con estos parámetros obtenemos un recall de 0.0%, sin embargo la gráfica de precision-recall muestra un comportamiento aceptable en las predicciones. Como se puede ver en la siguiente gráfica. En la gráfica ROC curve obtiene un valor del 0.79, siendo aceptable. Estableciéndose como un buen baseline para comparar el rendimiento de otros modelos.
### Logistic Regression
Se implementó este modelo con los parámetros por defecto para evidenciar su rendimiento. Sin ningún tipo de regulación, sin algoritmo de optimización, número de iteraciones de 500 y ajuste para clases desbalanceadas.
#### Train
Los resultados para las predicciones realizadas con el dataset train. Se obtuvo una métrica de recall del 63%. En la gráfica precisión recall-curve esta gráfica se muestra por encima del baseline, evidenciando que tiene mejor comportamiento. Por otro lado, en la ROC curve se tiene un valor de 0.83. Confirmando la superioridad en el baseline. Mostrando que ha aprendido de los datos.
#### Test
Sin embargo al evaluar el modelo en con dataset test se evidencia que no ha sido capaz de generalizar las relaciones de los datos, mostrando un recall de 6%, en la gráfica precision-recall está por debajo de baseline muy cercano a cero y por último en ROC tenemos un valor de 0.6, inferior a baseline. Por lo tanto este modelo no es eficiente.




### Logistic Regression Ridge
Se entrenó nuevamente el modelo aplicando una regulación Ridge de 0.1. Se evidenciaron los mismos resultados que el modelo original tanto en test como en train. se graficó el comportamiento del train y el test comparado con el baseline, como se puede ver en la siguiente gráfica:


![graficas](https://github.com/MaickMos/zrive-ds/blob/686a77aed98b68f3ab4ad15dad5e737b30cef5ff/src/module_3/images/Image_2.png)  




Seguidamente se graficó el comportamiento frente a otros valores de regulación, usando la función plot_metrics() desde 1000 hasta 1e-8 en potencias de 100.


En el entrenamiento:
Se puede ver un comportamiento similar a el modelo base, teniendo un valor que cambia la dinámica c=0.000001, mostrando un mejor desempeño en ciertas áreas.
![graficas](https://github.com/MaickMos/zrive-ds/blob/686a77aed98b68f3ab4ad15dad5e737b30cef5ff/src/module_3/images/Image_3.png)  


En el test:
El modelo no demostró un buen rendimiento, estando aún debajo del Baseline. De nuevo el modelo de C=0.0000001 tiene un mejor rendimiento.


![graficas](https://github.com/MaickMos/zrive-ds/blob/686a77aed98b68f3ab4ad15dad5e737b30cef5ff/src/module_3/images/Image_4.png)  


### Logistic Regression Lasso
Se realizaron las mismas pruebas con la regulación de Lasso. Donde de manera general se obtienen mejores resultados superando al baseline. En específico el modelo de mayor con rendimiento es regulación lasso C = 0.0001 con un AUC en la gráfica ROC de 0.83.


![graficas](https://github.com/MaickMos/zrive-ds/blob/686a77aed98b68f3ab4ad15dad5e737b30cef5ff/src/module_3/images/Image_5.png)  


## Pesos de las variables
Usando el modelo de mejor rendimiento y dado que la regulación Lasso envía mas coeficientes a ceros y da importancias a otras variables, se miraron las principales variables que aportan al modelo. teniendo que las más importantes son:
* ordered_before
* global_popularity
* abandoned_before
Las demás variables tienen valor de cero, por lo tanto no aportan al entrenamiento del modelo. Y es posible prescindir de estas.


## Product type
Por último se realizó un entrenamiento con las tres variables que mas aportan al modelo y se implementó la variable de product type con categorical encoding. Esto para comprobar si se obtiene un mejor rendimiento usando esta variable que presenta una alta cardinalidad teniendo 62 valores únicos.
Se realiza la preparación del dataset, entrenamiento del modelo regresión logística con regulación Lasso y ridge de C=0.0001 y se comparó con este mismo modelo sin implementar la variable de producty type.
![graficas](https://github.com/MaickMos/zrive-ds/blob/686a77aed98b68f3ab4ad15dad5e737b30cef5ff/src/module_3/images/Image_6.png)  


En la gráfica Ridge muestra un comportamiento mejor que Baseline, sin embargo los que presentan un mayor desempeño son Lasso, mostrando el mismo comportamiento aunque se haya entrenado con categorical type. Se observa el peso de las categorías y dado que Lasso baja los coeficientes bajos a cero, nuevamente solo están presentes las tres mismas variables.


Por ultimo se guarda el modelo Lasso con C=0.0001 con las tres variables mencionadas anteriormente.


# Archivo para cargar el modelo
Se creó el script load_model.py, el cual permite realizar la carga del modelo y del normalizador.
* Tiene las funciones para:
* Cargar dataset, con la columnas del dataset original
* PreProcesar los datos: a partir de los datos dados: User y product, se entregan las variables del usuario y producto
* Cargar modelo desde el path
* Estandarización de los datos: con un objeto StandardScaler de Sklearn
* Predecir probabilidad: llama a las funciones necesarias para cargar el modelo y los datos y realizar la predicción.
