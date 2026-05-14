import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

df = pd.read_csv('geoprecio_clean.csv')
df['nombre_norm'] = df['nombre'].str.lower().str.strip()

# Agrupaiento por nombre y por cantidad estandarizada para asegurar que comparamos el mismo tamaño
walmart = df[df['tienda'] == 'Walmart'].groupby(['nombre_norm', 'cant_std'])['precio_num'].mean().reset_index()
bodega = df[df['tienda'] == 'Bodega Aurrera'].groupby(['nombre_norm', 'cant_std'])['precio_num'].mean().reset_index()

# Cruzamos por Nombre + Cantidad (Validación Doble)
comparativa_estricta = pd.merge(walmart, bodega, on=['nombre_norm', 'cant_std'], suffixes=('_w', '_ba'))
diferencias = (comparativa_estricta['precio_num_w'] - comparativa_estricta['precio_num_ba']).values

# estadisticos
n = len(diferencias)
nu = n - 1
media_d = np.mean(diferencias)
std_d = np.std(diferencias, ddof=1)
error_estandar = std_d / np.sqrt(n)

t_stat, p_valor = stats.ttest_rel(comparativa_estricta['precio_num_w'], comparativa_estricta['precio_num_ba'])
t_critico = stats.t.ppf(0.975, df=nu)
lim_inf = media_d - (t_critico * error_estandar)
lim_sup = media_d + (t_critico * error_estandar)

# visualizaciones
#distribucion t
plt.figure(figsize=(10, 5))
x = np.linspace(-12, 12, 1000)
y = stats.t.pdf(x, nu)
plt.plot(x, y, label='Distribución t de Student', color='#2E86C1', lw=2)
plt.fill_between(x, 0, y, where=(x > t_critico) | (x < -t_critico), color='#E74C3C', alpha=0.4, label='Zona de Rechazo')
plt.axvline(t_stat, color='#1D8348', linestyle='--', lw=2, label=f'T-observado: {t_stat:.2f}')
plt.title('Rigurosidad Estadística: Prueba de Hipótesis Pareada', fontsize=14)
plt.xlabel('Desviaciones (Valor t)', fontsize=12)
plt.legend()
plt.grid(alpha=0.2)
plt.savefig('distribucion_t_validada.png')

# histograma de diferencias
plt.figure(figsize=(10, 5))
plt.hist(diferencias, bins=25, color='#F4D03F', edgecolor='black', alpha=0.6)
plt.axvline(0, color='red', linewidth=2, label='H0: Sin Diferencia')
plt.axvline(media_d, color='black', linestyle='--', linewidth=2, label=f'Media: ${media_d:.2f}')
plt.title('Distribución de Diferencias (Validación: Nombre + Tamaño)', fontsize=14)
plt.xlabel('Diferencia Walmart - Bodega ($)', fontsize=12)
plt.legend()
plt.savefig('histograma_validado.png')

#barras comparativas
plt.figure(figsize=(7, 6))
tiendas = ['Bodega Aurrera', 'Walmart']
promedios = [comparativa_estricta['precio_num_ba'].mean(), comparativa_estricta['precio_num_w'].mean()]
plt.bar(tiendas, promedios, color=['#76D7C4', '#F7DC6F'], edgecolor='gray')
plt.title('Comparativa Final de Precios Promedio', fontsize=14)
for i, v in enumerate(promedios):
    plt.text(i, v + 0.5, f'${v:.2f}', ha='center', fontweight='bold')
plt.savefig('barras_validadas.png')

# # Exportar una muestra de los productos comparados para que el usuario los vea
# muestra_productos = comparativa_estricta.head(10)[['nombre_norm', 'cant_std', 'precio_num_w', 'precio_num_ba']]
# muestra_productos.to_csv('muestra_productos_validados.csv', index=False)

print(f"Número de pares tras validación: {n}")
print(f"T-stat: {t_stat:.4f}")
print(f"P-valor: {p_valor:.4f}")
print(f"IC: ({lim_inf:.4f}, {lim_sup:.4f})")