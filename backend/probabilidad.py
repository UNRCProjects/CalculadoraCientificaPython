import pandas as pd
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
import seaborn as sns
from typing import List, Tuple, Dict, Any
import io
import base64

def cargar_datos(archivo) -> pd.DataFrame:
    """
    Carga datos desde un archivo CSV o Excel
    """
    try:
        if archivo.name.endswith('.csv'):
            df = pd.read_csv(archivo)
        elif archivo.name.endswith(('.xlsx', '.xls')):
            df = pd.read_excel(archivo)
        else:
            raise ValueError("Formato de archivo no soportado")
        return df
    except Exception as e:
        raise Exception(f"Error al cargar el archivo: {str(e)}")

def estadisticas_descriptivas(df: pd.DataFrame, columna: str) -> Dict[str, float]:
    """
    Calcula estadísticas descriptivas básicas de una columna
    """
    datos = df[columna].dropna()
    return {
        'media': datos.mean(),
        'mediana': datos.median(),
        'desviacion_estandar': datos.std(),
        'varianza': datos.var(),
        'minimo': datos.min(),
        'maximo': datos.max(),
        'cuartil_25': datos.quantile(0.25),
        'cuartil_75': datos.quantile(0.75),
        'asimetria': stats.skew(datos),
        'curtosis': stats.kurtosis(datos)
    }

def ajustar_distribucion_normal(datos: pd.Series) -> Dict[str, Any]:
    """
    Ajusta una distribución normal a los datos
    """
    datos_limpios = datos.dropna()
    media, desv_std = stats.norm.fit(datos_limpios)
    
    return {
        'tipo': 'Normal',
        'parametros': {'media': media, 'desviacion_estandar': desv_std},
        'pdf': lambda x: stats.norm.pdf(x, media, desv_std),
        'cdf': lambda x: stats.norm.cdf(x, media, desv_std),
        'ppf': lambda x: stats.norm.ppf(x, media, desv_std)
    }

def ajustar_distribucion_exponencial(datos: pd.Series) -> Dict[str, Any]:
    """
    Ajusta una distribución exponencial a los datos
    """
    datos_limpios = datos.dropna()
    # Ajustar parámetro de escala (lambda = 1/scale)
    scale = stats.expon.fit(datos_limpios)[1]
    
    return {
        'tipo': 'Exponencial',
        'parametros': {'lambda': 1/scale, 'scale': scale},
        'pdf': lambda x: stats.expon.pdf(x, scale=scale),
        'cdf': lambda x: stats.expon.cdf(x, scale=scale),
        'ppf': lambda x: stats.expon.ppf(x, scale=scale)
    }

def ajustar_distribucion_gamma(datos: pd.Series) -> Dict[str, Any]:
    """
    Ajusta una distribución gamma a los datos
    """
    datos_limpios = datos.dropna()
    shape, scale = stats.gamma.fit(datos_limpios)
    
    return {
        'tipo': 'Gamma',
        'parametros': {'shape': shape, 'scale': scale},
        'pdf': lambda x: stats.gamma.pdf(x, shape, scale=scale),
        'cdf': lambda x: stats.gamma.cdf(x, shape, scale=scale),
        'ppf': lambda x: stats.gamma.ppf(x, shape, scale=scale)
    }

def ajustar_distribucion_beta(datos: pd.Series) -> Dict[str, Any]:
    """
    Ajusta una distribución beta a los datos (normalizados entre 0 y 1)
    """
    datos_limpios = datos.dropna()
    # Normalizar datos entre 0 y 1
    datos_norm = (datos_limpios - datos_limpios.min()) / (datos_limpios.max() - datos_limpios.min())
    a, b, loc, scale = stats.beta.fit(datos_norm)
    
    return {
        'tipo': 'Beta',
        'parametros': {'alpha': a, 'beta': b, 'loc': loc, 'scale': scale},
        'pdf': lambda x: stats.beta.pdf(x, a, b, loc, scale),
        'cdf': lambda x: stats.beta.cdf(x, a, b, loc, scale),
        'ppf': lambda x: stats.beta.ppf(x, a, b, loc, scale)
    }

def ajustar_distribucion_lognormal(datos: pd.Series) -> Dict[str, Any]:
    """
    Ajusta una distribución log-normal a los datos
    """
    datos_limpios = datos.dropna()
    # Asegurar que todos los valores sean positivos
    datos_positivos = datos_limpios[datos_limpios > 0]
    if len(datos_positivos) == 0:
        raise ValueError("No hay valores positivos para ajustar distribución log-normal")
    
    s, loc, scale = stats.lognorm.fit(datos_positivos)
    
    return {
        'tipo': 'Log-Normal',
        'parametros': {'s': s, 'loc': loc, 'scale': scale},
        'pdf': lambda x: stats.lognorm.pdf(x, s, loc, scale),
        'cdf': lambda x: stats.lognorm.cdf(x, s, loc, scale),
        'ppf': lambda x: stats.lognorm.ppf(x, s, loc, scale)
    }

def ajustar_distribucion_weibull(datos: pd.Series) -> Dict[str, Any]:
    """
    Ajusta una distribución Weibull a los datos
    """
    datos_limpios = datos.dropna()
    c, loc, scale = stats.weibull_min.fit(datos_limpios)
    
    return {
        'tipo': 'Weibull',
        'parametros': {'c': c, 'loc': loc, 'scale': scale},
        'pdf': lambda x: stats.weibull_min.pdf(x, c, loc, scale),
        'cdf': lambda x: stats.weibull_min.cdf(x, c, loc, scale),
        'ppf': lambda x: stats.weibull_min.ppf(x, c, loc, scale)
    }

def test_bondad_ajuste(datos: pd.Series, distribucion: Dict[str, Any]) -> Dict[str, float]:
    """
    Realiza test de bondad de ajuste (Kolmogorov-Smirnov)
    """
    datos_limpios = datos.dropna()
    
    if distribucion['tipo'] == 'Normal':
        media = distribucion['parametros']['media']
        desv_std = distribucion['parametros']['desviacion_estandar']
        ks_stat, p_value = stats.kstest(datos_limpios, lambda x: stats.norm.cdf(x, media, desv_std))
    elif distribucion['tipo'] == 'Exponencial':
        scale = distribucion['parametros']['scale']
        ks_stat, p_value = stats.kstest(datos_limpios, lambda x: stats.expon.cdf(x, scale=scale))
    elif distribucion['tipo'] == 'Gamma':
        shape = distribucion['parametros']['shape']
        scale = distribucion['parametros']['scale']
        ks_stat, p_value = stats.kstest(datos_limpios, lambda x: stats.gamma.cdf(x, shape, scale=scale))
    elif distribucion['tipo'] == 'Beta':
        a = distribucion['parametros']['alpha']
        b = distribucion['parametros']['beta']
        loc = distribucion['parametros']['loc']
        scale = distribucion['parametros']['scale']
        ks_stat, p_value = stats.kstest(datos_limpios, lambda x: stats.beta.cdf(x, a, b, loc, scale))
    elif distribucion['tipo'] == 'Log-Normal':
        s = distribucion['parametros']['s']
        loc = distribucion['parametros']['loc']
        scale = distribucion['parametros']['scale']
        ks_stat, p_value = stats.kstest(datos_limpios, lambda x: stats.lognorm.cdf(x, s, loc, scale))
    elif distribucion['tipo'] == 'Weibull':
        c = distribucion['parametros']['c']
        loc = distribucion['parametros']['loc']
        scale = distribucion['parametros']['scale']
        ks_stat, p_value = stats.kstest(datos_limpios, lambda x: stats.weibull_min.cdf(x, c, loc, scale))
    
    return {
        'ks_statistic': ks_stat,
        'p_value': p_value,
        'rechaza_h0': p_value < 0.05
    }

def comparar_distribuciones(datos: pd.Series) -> List[Dict[str, Any]]:
    """
    Compara múltiples distribuciones y devuelve las mejores
    """
    distribuciones = []
    
    try:
        dist_normal = ajustar_distribucion_normal(datos)
        test_normal = test_bondad_ajuste(datos, dist_normal)
        dist_normal['test'] = test_normal
        distribuciones.append(dist_normal)
    except:
        pass
    
    try:
        dist_exp = ajustar_distribucion_exponencial(datos)
        test_exp = test_bondad_ajuste(datos, dist_exp)
        dist_exp['test'] = test_exp
        distribuciones.append(dist_exp)
    except:
        pass
    
    try:
        dist_gamma = ajustar_distribucion_gamma(datos)
        test_gamma = test_bondad_ajuste(datos, dist_gamma)
        dist_gamma['test'] = test_gamma
        distribuciones.append(dist_gamma)
    except:
        pass
    
    try:
        dist_beta = ajustar_distribucion_beta(datos)
        test_beta = test_bondad_ajuste(datos, dist_beta)
        dist_beta['test'] = test_beta
        distribuciones.append(dist_beta)
    except:
        pass
    
    try:
        dist_lognorm = ajustar_distribucion_lognormal(datos)
        test_lognorm = test_bondad_ajuste(datos, dist_lognorm)
        dist_lognorm['test'] = test_lognorm
        distribuciones.append(dist_lognorm)
    except:
        pass
    
    try:
        dist_weibull = ajustar_distribucion_weibull(datos)
        test_weibull = test_bondad_ajuste(datos, dist_weibull)
        dist_weibull['test'] = test_weibull
        distribuciones.append(dist_weibull)
    except:
        pass
    
    # Ordenar por p-value (mayor es mejor)
    distribuciones.sort(key=lambda x: x['test']['p_value'], reverse=True)
    
    return distribuciones

def generar_grafico_distribucion(datos: pd.Series, distribucion: Dict[str, Any]) -> str:
    """
    Genera un gráfico de la distribución ajustada
    """
    plt.figure(figsize=(10, 6))
    
    # Histograma de los datos
    plt.hist(datos.dropna(), bins=30, density=True, alpha=0.7, color='skyblue', label='Datos')
    
    # Curva de la distribución ajustada
    x = np.linspace(datos.min(), datos.max(), 1000)
    y = distribucion['pdf'](x)
    plt.plot(x, y, 'r-', linewidth=2, label=f"Distribución {distribucion['tipo']}")
    
    plt.xlabel('Valores')
    plt.ylabel('Densidad')
    plt.title(f'Ajuste de Distribución {distribucion["tipo"]}')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    # Convertir a base64 para mostrar en Streamlit
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png', dpi=300, bbox_inches='tight')
    buffer.seek(0)
    image_base64 = base64.b64encode(buffer.getvalue()).decode()
    plt.close()
    
    return image_base64

def calcular_probabilidad_acumulada(distribucion: Dict[str, Any], valor: float) -> float:
    """
    Calcula la probabilidad acumulada P(X <= valor)
    """
    return distribucion['cdf'](valor)

def calcular_percentil(distribucion: Dict[str, Any], probabilidad: float) -> float:
    """
    Calcula el percentil para una probabilidad dada
    """
    return distribucion['ppf'](probabilidad)

def calcular_intervalo_confianza(distribucion: Dict[str, Any], nivel_confianza: float = 0.95) -> Tuple[float, float]:
    """
    Calcula el intervalo de confianza para la distribución
    """
    alpha = 1 - nivel_confianza
    limite_inferior = distribucion['ppf'](alpha/2)
    limite_superior = distribucion['ppf'](1 - alpha/2)
    return limite_inferior, limite_superior

