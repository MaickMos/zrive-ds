# Push Notificactions  module #4
En esta PR se hara entrega de la continuacion del modelo predictivo para posibles personas interesadas en un producto. Dado un usuario y producto, se predice si compraria ese producto si estuvieran comprando en ese momento. Condiciones: los usuarios deben ser aquellos que realizan una compra de minimo 5 productos. Esta vez usaron modelos no lineales 

## Preparacion del dataset
Se usaron el mismos dataset de la practica anterior y una variacion donde se obesrvaron las principales caracteristicas que toma un random forest para escoger las mas importantes, quedando con 9.
## Metricas de evaluacion
Se aplicaron las misma metricas de evaluacion dentro de una funcion y se implemento una nueva con las metricas de 
- roc_auc_score
- log_loss
- average_precision_score
Se conservan las anteriores:
- Recall
- precision-recall curve
- ROC Curve

## Modelos
Se concervan los mejores modeles de baseline y regresion logistica para futuras compraciones
### Random Forest
Se realiza una prueba con el random forest con el dataset completo, se obtienen resultados malos con una average_precision de 0.014 y unAUC en precision recall curve de 0.02 para el dataset de test.
Se escogen las feautures con un valor mayor a 3%, se crea un nuevo data set con 9 variables.
Se compara este dataset con el anterior de 3 varaibles.
Se obtienen mejores resultados, siendo el mejor el de tres variables en test con un AUC de 0.10 y  average_precision de 0.027.
por ultimo se testea con el numero de arboles de 5, 10 y 100, usando el dataset de 3 variables.
Se obtievieron resultados similares en test siendo el mejor el de 10 arboles, con AUC de 0.14 y average precision de 0.046.
Se seleciona este ultimo modelo ya que tiene un rendimiento similar al de 100 de arboles pque tiene el modelo por defecto.
### Gradient Boosting Trees
Se realiza una prueba con hiperparametro de n_estimators=100, learning_rate=0.05, y max_depth=5.
Se obtiene resultados similares al de random forest.
Se realiza una variacion entre el learning rate y la profundida de los arboles.
El que mejor rendimientotiene es de 0.05 learn rate y 5 de profundidad.
### Comparacion
Se comparan los 4 cuatro modelos y se concluye.

La regresión logística con regularización Ridge fue el mejor modelo en este caso para valores de recall en el rango de 0,1 a 0,3, logrando un AUC de 0,16 en la curva de precisión-recall.

Se probaron diferentes versiones del conjunto de datos: el conjunto de datos numérico completo, el conjunto de datos con solo coeficientes superiores a 0,03 y el conjunto de datos con las tres variables más importantes. En todos los modelos, el mejor rendimiento se obtuvo utilizando las tres variables más importantes. Irónicamente, esto también fue cierto para los modelos basados ​​en árboles, pero ningún ajuste mejoró su rendimiento significativamente.

Todos los modelos superaron la línea base, lo que confirma su valor predictivo. La regresión logística sigue siendo la mejor opción en este caso. Quizás los modelos basados ​​en árboles requieren un ajuste más profundo de los hiperparámetros, o la relación entre las variables es más lineal, lo que favorece la regresión.

# Archivo para cargar el modelo
## Fit
Se creo el script de fit.py, permite cargar la parametrizacion para un modelo de regresion logistica con la fecha y hora generada y lo guarda en un path, retorna el lugar(path) donde se guardo
## Predict
script que llama a un modelo guardado en un path, transforma los datos para ingresarlos en el modelo y obtener las prediciones.
