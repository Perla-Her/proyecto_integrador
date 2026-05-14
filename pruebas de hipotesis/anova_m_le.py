import pandas as pd
import numpy as np
import re
from scipy.special import gamma
from scipy import integrate
from scipy.stats import studentized_range
import matplotlib.pyplot as plt
import seaborn as sns

#Carga y filtro
df = pd.read_csv('geoprecio_clean.csv')

def filtro_leche_avanzado(nombre):
    n = str(nombre).lower()
    if 'leche' not in n: return False
    prohibidos = ['polvo', 'nido', 'nan', 'bebe', 'formula', 'condensada', 'evaporada', 'sabor']
    return not any(p in n for p in prohibidos)

df_l = df[df['nombre'].apply(filtro_leche_avanzado)].copy()

def normalizar_a_litro(row):
    nombre = str(row['nombre']).lower()
    precio_total = row['precio_num']
    
    match_caja = re.search(r'(\d+)\s*(pzas|piezas|pack|caja con)', nombre)
    if match_caja:
        return precio_total / int(match_caja.group(1))
            
    # macheo para detectar volumen explicito
    match_vol = re.search(r'(\d+\.?\d*)\s*(l|litros?)\b', nombre)
    if match_vol:
        litros = float(match_vol.group(1))
        if litros > 0: return precio_total / litros
            
    return row['precio_unitario']

df_l['precio_litro_final'] = df_l.apply(normalizar_a_litro, axis=1)
df_l = df_l[(df_l['precio_litro_final'] >= 15) & (df_l['precio_litro_final'] <= 40)].copy()

def extraer_marca(nombre):
    for m in ['lala', 'alpura', 'santa clara', 'san marcos', 'great value']:
        if m in str(nombre).lower(): return m.title()
    return 'Otra'

df_l['marca'] = df_l['nombre'].apply(extraer_marca)
df_l = df_l[df_l['marca'] != 'Otra']

#calculo de metricas anova
def calculate_ssa(groups, global_mean):
    return sum(len(g) * (np.mean(g) - global_mean)**2 for g in groups)

def calculate_sse(groups):
    return sum(sum((yij - np.mean(g))**2 for yij in g) for g in groups)

def fdist(f, df1, df2):
    return (gamma((df1+df2)*0.5)*(df1/df2)**(df1*0.5)/(gamma(df1*0.5)*gamma(df2*0.5))) * f**(df1*0.5-1) / (1.0+df1*f/df2)**((df1+df2)*0.5)


#anova por marca
marcas_unicas = df_l['marca'].unique()

for marca in marcas_unicas:
    df_marca = df_l[df_l['marca'] == marca]
    
    # Agrupacion por tienda para la marca
    grupos_serie = df_marca.groupby('tienda')['precio_litro_final'].apply(list)
    
    # Filtro de tiendas con al menos dos precios
    grupos_validos = grupos_serie[grupos_serie.apply(len) > 1]
    data = grupos_validos.tolist()
    nombres_grupos = grupos_validos.index.tolist()
    
    k = len(data)
    all_values = [val for sublist in data for val in sublist]
    n_total = len(all_values)
    
    print(f"\n---> MARCA: {marca.upper()} <---")
    
    if k < 2 or n_total <= k:
        print("No hay datos suficientes para comparar tiendas en esta marca.")
        continue
        
    y_mean_total = np.mean(all_values)
    ssa = calculate_ssa(data, y_mean_total)
    sse = calculate_sse(data)
    
    # prevencion por si todos son iguales
    if sse == 0:
        print("Los precios son idénticos. F=0.")
        continue
        
    msa = ssa / (k - 1)
    mse = sse / (n_total - k)
    f_stat = msa / mse
    
    nu1 = k - 1
    nu2 = n_total - k
    
    # p-value
    p_valor = integrate.quad(fdist, f_stat, np.inf, args=(nu1, nu2))[0]
    
    print(f"Estadístico F: {f_stat:.4f} | Valor p: {p_valor:.4f}")
    

    print(f"--- Intervalos de Confianza (95%) para la Media ---")
    import scipy.stats as st

    for i in range(k):
        grupo = data[i]
        nombre_t = nombres_grupos[i]
        
        n = len(grupo)
        media = np.mean(grupo)
        # o la desviación estándar propia del grupo:
        std_err = st.sem(grupo) 
        
        # Intervalo de confianza usando distribución t
        intervalo = st.t.interval(0.95, n-1, loc=media, scale=std_err)
        
        print(f"Tienda: {nombre_t:20} | Media: ${media:.2f} | IC 95%: [${intervalo[0]:.2f} - ${intervalo[1]:.2f}]")
    print("-" * 50)

    x = np.linspace(0.0001, max(f_stat * 2, 10), 1000)
    y = [fdist(val, nu1, nu2) for val in x]

    plt.figure(figsize=(10,6))

    # curva F
    plt.plot(x, y, label='Distribución F')

    # área del p-value
    x_fill = np.linspace(f_stat, max(x), 500)
    y_fill = [fdist(val, nu1, nu2) for val in x_fill]

    plt.fill_between(x_fill, y_fill, alpha=0.4,
                    label=f'Área p-value = {p_valor:.4f}')

    # línea del estadístico F
    plt.axvline(f_stat, linestyle='--',
                label=f'F observado = {f_stat:.2f}')

    plt.title(f'Distribución F - Marca {marca}')
    plt.xlabel('Valor F')
    plt.ylabel('Densidad')

    plt.legend()
    plt.grid(True)

    plt.show()
    
    # PRUEBA TUKEY
    if p_valor < 0.05:
        q_critico = studentized_range.ppf(0.95, k, nu2)
        
        for i in range(k):
            for j in range(i + 1, k):
                g1, g2 = data[i], data[j]
                n1, n2 = nombres_grupos[i], nombres_grupos[j]
                
                diff = abs(np.mean(g1) - np.mean(g2))
                error_est = np.sqrt((mse / 2) * ((1 / len(g1)) + (1 / len(g2))))
                margen = q_critico * error_est
                
                if diff > margen:
                    if np.mean(g1) < np.mean(g2):
                        print(f"{n1} es significativamente MAS BARATO que {n2} por ${diff:.2f}")
                    else:
                        print(f"{n2} es significativamente MAS BARATO que {n1} por ${diff:.2f}")
            print()
    else:
        print("No hay diferencia estadística entre tiendas.")

        
        # ==============================
    # BOXPLOT PRECIOS POR TIENDA
    # ==============================

    plt.figure(figsize=(12,6))

    sns.boxplot(
        data=df_marca,
        x='tienda',
        y='precio_litro_final'
    )

    plt.title(f'Comparación de precios por tienda - {marca}')
    plt.xlabel('Tienda')
    plt.ylabel('Precio por litro')

    plt.xticks(rotation=45)

    plt.show()


plt.figure(figsize=(12,6))

sns.boxplot(
    data=df_marca,
    x='tienda',
    y='precio_litro_final'
)

sns.stripplot(
    data=df_marca,
    x='tienda',
    y='precio_litro_final',
    color='red',
    alpha=0.5
)

plt.title(f'Precios individuales por tienda - {marca}')
plt.xlabel('Tienda')
plt.ylabel('Precio por litro')

plt.xticks(rotation=45)

plt.show()

#df_l.to_csv('marca_leche.csv', index=False)
