import pandas as pd
import numpy as np
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.stattools import adfuller
from sklearn.metrics import mean_squared_error, mean_absolute_error
import warnings
warnings.filterwarnings('ignore')

def generar_datos_ventas(n_dias=180):
    """
    Genera datos de ventas realistas para n días
    
    Args:
        n_dias: Número de días a generar (por defecto 180 = 6 meses)
    
    Returns:
        pandas.Series: Serie temporal de ventas
    """
    # 6 meses de datos diarios
    fechas = pd.date_range(start='2024-01-01', periods=n_dias, freq='D')
    
    # Datos de ventas súper realistas
    np.random.seed(42)  # Para reproducibilidad
    
    # Base de ventas más realista (tienda mediana)
    base_ventas = 2500
    
    # Tendencia creciente con variaciones (crecimiento del 1.5% mensual)
    tendencia_base = np.linspace(0, 0.09, n_dias)  # 9% de crecimiento en 6 meses
    # Agregar variaciones en la tendencia
    variacion_tendencia = 0.02 * np.sin(2 * np.pi * np.arange(n_dias) / 60)  # Ciclo de 2 meses
    tendencia = tendencia_base + variacion_tendencia
    
    # Estacionalidad semanal más realista
    dia_semana = fechas.dayofweek
    estacionalidad_semanal = np.where(dia_semana == 0, -0.25,  # Lunes -25% (día más bajo)
                            np.where(dia_semana == 1, -0.10,   # Martes -10%
                            np.where(dia_semana == 2, -0.05,   # Miércoles -5%
                            np.where(dia_semana == 3, 0.05,    # Jueves +5%
                            np.where(dia_semana == 4, 0.20,    # Viernes +20% (día más alto)
                            np.where(dia_semana == 5, 0.15,    # Sábado +15%
                            -0.15))))))  # Domingo -15%
    
    # Estacionalidad mensual más compleja
    dia_mes = fechas.day
    estacionalidad_mensual = np.where(dia_mes >= 28, 0.30,  # Últimos 3 días +30%
                            np.where(dia_mes >= 25, 0.15,   # Días 25-27 +15%
                            np.where(dia_mes <= 3, 0.10,    # Primeros 3 días +10%
                            np.where(dia_mes <= 7, 0.05,    # Días 4-7 +5%
                            np.where(dia_mes >= 15, 0.08,   # Mitad del mes +8%
                            -0.05)))))  # Días intermedios -5%
    
    # Estacionalidad por mes (enero bajo, marzo alto, etc.)
    mes = fechas.month
    estacionalidad_anual = np.where(mes == 1, -0.10,   # Enero -10% (post-navidad)
                          np.where(mes == 2, -0.05,    # Febrero -5%
                          np.where(mes == 3, 0.15,     # Marzo +15% (primavera)
                          np.where(mes == 4, 0.08,     # Abril +8%
                          np.where(mes == 5, 0.12,     # Mayo +12%
                          np.where(mes == 6, 0.20,     # Junio +20% (verano)
                          0.0))))))
    
    # Eventos especiales más realistas
    eventos = np.zeros(n_dias)
    
    # Black Friday (última semana de enero) - simulando
    eventos[25:32] = 0.45
    
    # Día de San Valentín (14 de febrero)
    eventos[44:47] = 0.25
    
    # Promoción de primavera (marzo)
    eventos[75:85] = 0.30
    
    # Día de la Madre (segundo domingo de mayo - día 130-135)
    eventos[130:137] = 0.35
    
    # Promoción de verano (junio)
    eventos[150:160] = 0.40
    
    # Día del Padre (tercer domingo de junio - día 170-175)
    eventos[170:177] = 0.30
    
    # Ruido más realista (variabilidad diaria)
    ruido_diario = np.random.normal(0, 0.12, n_dias)
    
    # Ruido semanal (variaciones de semana a semana)
    ruido_semanal = np.repeat(np.random.normal(0, 0.08, n_dias // 7 + 1), 7)[:n_dias]
    
    # Ruido mensual (variaciones de mes a mes)
    ruido_mensual = np.repeat(np.random.normal(0, 0.05, 6), 30)[:n_dias]
    
    # Calcular ventas finales con todos los componentes
    valores = base_ventas * (1 + tendencia + estacionalidad_semanal + 
                           estacionalidad_mensual + estacionalidad_anual + 
                           eventos + ruido_diario + ruido_semanal + ruido_mensual)
    
    # Asegurar que no haya valores negativos y redondear a enteros
    valores = np.maximum(valores, 100)
    valores = np.round(valores).astype(int)
    
    # Agregar algunos outliers realistas (días excepcionales)
    outliers_indices = np.random.choice(n_dias, size=8, replace=False)
    for idx in outliers_indices:
        if np.random.random() > 0.5:  # 50% de probabilidad de outlier positivo
            valores[idx] = int(valores[idx] * np.random.uniform(1.5, 2.2))
        else:  # 50% de probabilidad de outlier negativo
            valores[idx] = int(valores[idx] * np.random.uniform(0.3, 0.7))
    
    return pd.Series(valores, index=fechas)

def analizar_estacionariedad(serie):
    """
    Realiza test de estacionariedad (ADF)
    
    Args:
        serie: Serie temporal pandas
        
    Returns:
        dict: Resultados del test ADF
    """
    resultado = adfuller(serie.dropna())
    
    return {
        'estadistico_adf': resultado[0],
        'p_valor': resultado[1],
        'valores_criticos': resultado[4],
        'es_estacionaria': resultado[1] < 0.05,
        'interpretacion': 'Serie estacionaria' if resultado[1] < 0.05 else 'Serie no estacionaria'
    }

def encontrar_parametros_arima(serie, max_p=5, max_d=2, max_q=5):
    """
    Encuentra los parámetros óptimos (p, d, q) usando AIC
    
    Args:
        serie: Serie temporal pandas
        max_p: Máximo valor para p
        max_d: Máximo valor para d  
        max_q: Máximo valor para q
        
    Returns:
        tuple: (p, d, q) óptimos y AIC
    """
    mejor_aic = float('inf')
    mejores_parametros = None
    
    for p in range(max_p + 1):
        for d in range(max_d + 1):
            for q in range(max_q + 1):
                try:
                    modelo = ARIMA(serie, order=(p, d, q))
                    modelo_fit = modelo.fit()
                    aic = modelo_fit.aic
                    
                    if aic < mejor_aic:
                        mejor_aic = aic
                        mejores_parametros = (p, d, q)
                except:
                    continue
    
    return mejores_parametros, mejor_aic

def entrenar_arima(serie, p, d, q):
    """
    Entrena el modelo ARIMA
    
    Args:
        serie: Serie temporal pandas
        p, d, q: Parámetros del modelo
        
    Returns:
        tuple: (modelo_entrenado, mensaje)
    """
    try:
        modelo = ARIMA(serie, order=(p, d, q))
        modelo_fit = modelo.fit()
        return modelo_fit, f"Modelo ARIMA({p},{d},{q}) entrenado exitosamente"
    except Exception as e:
        return None, f"Error al entrenar modelo: {str(e)}"

def predecir_arima(modelo, n_periodos=10):
    """
    Realiza predicciones con el modelo entrenado
    
    Args:
        modelo: Modelo ARIMA entrenado
        n_periodos: Número de períodos a predecir
        
    Returns:
        tuple: (predicciones, intervalos, mensaje)
    """
    try:
        prediccion = modelo.forecast(steps=n_periodos)
        intervalos = modelo.get_forecast(steps=n_periodos).conf_int()
        
        return {
            'prediccion': prediccion,
            'intervalo_inferior': intervalos.iloc[:, 0],
            'intervalo_superior': intervalos.iloc[:, 1]
        }, "Predicciones generadas exitosamente"
    except Exception as e:
        return None, f"Error al hacer predicciones: {str(e)}"

def calcular_metricas(serie_real, predicciones):
    """
    Calcula métricas de evaluación del modelo
    
    Args:
        serie_real: Valores reales
        predicciones: Valores predichos
        
    Returns:
        dict: Métricas de evaluación
    """
    mse = mean_squared_error(serie_real, predicciones)
    rmse = np.sqrt(mse)
    mae = mean_absolute_error(serie_real, predicciones)
    mape = np.mean(np.abs((serie_real - predicciones) / serie_real)) * 100
    
    return {
        'MSE': mse,
        'RMSE': rmse,
        'MAE': mae,
        'MAPE': mape
    }

def obtener_resumen_ventas(serie):
    """
    Obtiene resumen estadístico de las ventas
    
    Args:
        serie: Serie temporal de ventas
        
    Returns:
        dict: Resumen estadístico
    """
    return {
        'total_ventas': serie.sum(),
        'promedio_diario': serie.mean(),
        'desviacion_estandar': serie.std(),
        'ventas_max': serie.max(),
        'ventas_min': serie.min(),
        'crecimiento_total': ((serie.tail(30).mean() - serie.head(30).mean()) / serie.head(30).mean()) * 100,
        'volatilidad': (serie.std() / serie.mean()) * 100
    }