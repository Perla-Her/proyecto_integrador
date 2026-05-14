import pandas as pd
import re



df = pd.read_csv('geoprecio_clean.csv')

#filtro aceite
def filtro_aceite(nombre):
    n = str(nombre).lower()
    if 'aceite' not in n: return False
    prohibidos = ['coco', 'cÃ¡rtamo','cartamo', 'virgen','aguacate', 'uva','aerosol', 'lata', 'carbonell',
                  'ecologico', 'suave', 'squeeze','ajonjoli']
    return not any(p in n for p in prohibidos)

# filtro para Pastas
def filtro_pastas(nombre):
    n = str(nombre).lower()
    if 'pasta' not in n and 'sopa' not in n and 'espagueti' not in n and 'codo' not in n: 
        return False
    prohibidos = ['salsa', 'lista', 'vaso', 'instantÃ¡nea', 'instantanea', 'fettuccine alfredo']
    return not any(p in n for p in prohibidos)

# Filtro para Frijoles
def filtro_frijoles(nombre):
    n = str(nombre).lower()
    if 'frijol' not in n: return False
    prohibidos = ['ensalada', 'mezcla', 'chipotle', 'elote','chorizo','puercos',
                  'claros','charros','adobo','congelado','organico','moro','horrneado',
                  'chilorio','queso','chipotle','ranch','soya','karne','jamapa','campo','salsa']
    return not any(p in n for p in prohibidos)

#filtro leche
def filtro_leche(nombre):
    n = str(nombre).lower()
    if 'leche' not in n: return False
    prohibidos = ['polvo', 'nido', 'nan', 'bebe', 'formula', 'condensada', 'evaporada', 'sabor', 'evaporada', 'chocolate',
                  'fresa', 'vainilla', 'almendra', 'soya', 'coco', 'avena']
    return not any(p in n for p in prohibidos)



# aceite
df_aceite = df[df['nombre'].apply(filtro_aceite)].copy()
df_aceite = df_aceite[(df_aceite['precio_unitario'] >= 15) & (df_aceite['precio_unitario'] <= 80)].copy()
df_aceite['categoria_ml'] = 'Aceite'

#leche
df_leche = df[df['nombre'].apply(filtro_leche)].copy()
df_leche = df_leche[(df_leche['precio_unitario'] >= 10) & (df_leche['precio_unitario'] <= 45)].copy()
df_leche['categoria_ml'] = 'Leche'

# frijoles
df_frijoles = df[df['nombre'].apply(filtro_frijoles)].copy()
df_frijoles = df_frijoles[(df_frijoles['precio_unitario'] >= 20) & (df_frijoles['precio_unitario'] <= 60)].copy()
df_frijoles['categoria_ml'] = 'Frijol'

#pastas
df_pastas = df[df['nombre'].apply(filtro_pastas)].copy()
df_pastas = df_pastas[(df_pastas['precio_unitario'] >= 5) & (df_pastas['precio_unitario'] <= 35)].copy()
df_pastas['categoria_ml'] = 'Pasta'

# concat
df_master_ml = pd.concat([df_aceite, df_leche, df_frijoles, df_pastas], ignore_index=True)

# to csv
df_master_ml.to_csv('geoprecio_ML.csv', index=False)

print(f"Dataset creado exitosamente con {len(df_master_ml)} registros.")
print(df_master_ml['categoria_ml'].value_counts())
