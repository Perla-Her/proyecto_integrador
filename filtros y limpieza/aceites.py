import pandas as pd
import numpy as np
import re
from scipy.special import gamma
from scipy import integrate
from scipy.stats import studentized_range
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv('geoprecio_clean.csv')

def filtro_aceite(nombre):
    n = str(nombre).lower()
    if 'aceite' not in n: return False
    prohibidos = ['coco', 'cÃ¡rtamo','cartamo', 'virgen','aguacate', 'uva','aerosol', 'lata', 'carbonell',
                  'ecologico', 'suave', 'squeeze','ajonjoli']
    return not any(p in n for p in prohibidos)



df_l = df[df['nombre'].apply(filtro_aceite)].copy()

df_l = df_l[(df_l['precio_unitario'] >= 15) & (df_l['precio_unitario'] <= 80)].copy()


df_l.to_csv('aceite_limpio.csv', index=False)