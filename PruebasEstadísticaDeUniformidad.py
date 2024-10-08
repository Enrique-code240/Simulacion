import random
import scipy.stats as stats
import matplotlib.pyplot as plt
import math

# Generar 100 números aleatorios
n = 100
numeros_aleatorios = [random.random() for _ in range(n)]

# Prueba de Uniformidad: Chi-cuadrado
def prueba_uniformidad(numeros):
    # Frecuencias observadas
    intervalos = [0] * 10
    for numero in numeros:
        index = min(int(numero * 10), 9)  # Asegura que 1.0 caiga en el último intervalo
        intervalos[index] += 1
    
    # Frecuencias esperadas en una distribución uniforme
    frec_esp = [len(numeros) / 10] * 10
    # Prueba Chi-cuadrado
    chi2, p_valor = stats.chisquare(intervalos, frec_esp)
    return chi2, p_valor

# Prueba de Aleatoriedad: Prueba de corridas (runs test)
def prueba_aleatoriedad(numeros):
    # Calcular la mediana manualmente
    numeros_ordenados = sorted(numeros)
    mid = len(numeros) // 2
    if len(numeros) % 2 == 0:
        mediana = (numeros_ordenados[mid - 1] + numeros_ordenados[mid]) / 2
    else:
        mediana = numeros_ordenados[mid]
    
    # Construir secuencia de corridas
    corridas = ''.join(['1' if x >= mediana else '0' for x in numeros])
    cambios = sum(1 for i in range(1, len(corridas)) if corridas[i] != corridas[i - 1])
    n1 = corridas.count('1')
    n2 = corridas.count('0')
    
    # Estadístico de prueba
    media_corridas = ((2 * n1 * n2) / (n1 + n2)) + 1
    var_corridas = (2 * n1 * n2 * (2 * n1 * n2 - n1 - n2)) / (((n1 + n2) ** 2) * (n1 + n2 - 1))
    z = (cambios - media_corridas) / math.sqrt(var_corridas)
    p_valor = 2 * (1 - stats.norm.cdf(abs(z)))  # valor p
    return z, p_valor

# Prueba de Independencia: Autocorrelación
def prueba_independencia(numeros, k=1):
    media = sum(numeros) / len(numeros)
    suma_num = sum((numeros[i] - media) * (numeros[i + k] - media) for i in range(len(numeros) - k))
    suma_den = sum((x - media) ** 2 for x in numeros)
    autocorr = suma_num / suma_den if suma_den != 0 else 0
    return autocorr

# Resultados
chi2, p_uniformidad = prueba_uniformidad(numeros_aleatorios)
z_aleatoriedad, p_aleatoriedad = prueba_aleatoriedad(numeros_aleatorios)
autocorrelacion = prueba_independencia(numeros_aleatorios)

# Mostrar resultados
print(f"Prueba de Uniformidad (Chi-cuadrado): Chi2 = {chi2:.4f}, p-valor = {p_uniformidad:.4f}")
print(f"Prueba de Aleatoriedad (Corridas): Z = {z_aleatoriedad:.4f}, p-valor = {p_aleatoriedad:.4f}")
print(f"Prueba de Independencia (Autocorrelación): Autocorrelación = {autocorrelacion:.4f}")

# Histograma para visualizar uniformidad
plt.hist(numeros_aleatorios, bins=10, range=(0, 1), edgecolor='black')
plt.title('Histograma de los números generados')
plt.show()

