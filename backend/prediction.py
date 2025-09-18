# Importamos las herramientas que necesitamos de la librería scikit-learn.
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
import pandas as pd

def entrenar_modelo_regresion(df, variable_objetivo, caracteristicas):
    # Esta función entrena un modelo de Regresión Lineal.
    # Recibe el DataFrame, el nombre de la columna que queremos predecir (Y)
    # y una lista de las columnas que usaremos para predecir (X).
    
    # Separamos nuestros datos en "características" (X) y "variable objetivo" (y).
    X = df[caracteristicas]
    y = df[variable_objetivo]
    
    # Dividimos los datos en dos grupos: uno para entrenar el modelo (80%) y otro para probarlo (20%).
    # 'random_state=42' es para que la división sea siempre la misma y nuestros resultados se puedan repetir.
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Creamos una instancia del modelo de Regresión Lineal.
    modelo = LinearRegression()
    # Entrenamos el modelo con nuestros datos de entrenamiento.
    modelo.fit(X_train, y_train)
    
    # Ahora, usamos el modelo entrenado para hacer predicciones sobre los datos de prueba.
    predicciones = modelo.predict(X_test)
    # Calculamos dos métricas para ver qué tan bueno es nuestro modelo.
    mse = mean_squared_error(y_test, predicciones)
    r2 = r2_score(y_test, predicciones)
    
    # Devolvemos el modelo ya entrenado y las métricas que calculamos.
    return modelo, mse, r2