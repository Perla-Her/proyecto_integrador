
import pandas as pd
import json
import re
import numpy as np
import unicodedata

def limpieza(archivo_json, archivo_salida_csv):
    #
    with open(archivo_json, 'r', encoding='utf-8') as f:
        data = json.load(f)
    df = pd.DataFrame(data)
    print(f"Iniciando proceso con {len(df)} registros.")

    #normalizacion texto
    def normalizar_texto(texto):
        """Elimina acentos y estandariza a minúsculas."""
        if not isinstance(texto, str): return ""
        return "".join(c for c in unicodedata.normalize('NFD', texto)
                       if unicodedata.category(c) != 'Mn').lower()

    # limpieza precio
    def limpiar_precio(row):
        texto_precio = str(row['precio'])
        match = re.search(r'(\d+\.\d+)', texto_precio)
        if match:
            return float(match.group(1))
        solo_numeros = re.sub(r'[^\d]', '', texto_precio)
        try:
            return float(solo_numeros)
        except:
            return 0.0

    df['precio_num'] = df.apply(limpiar_precio, axis=1)
    df = df[df['precio_num'] > 0].copy() # Eliminar registros sin precio

    #
    # Lista de palabras que delatan productos que no son comida
    palabras_prohibidas = [
       'cepillo', 'jabon de manos', 'gel antibacterial',
        'corporal', 'crema para pies', 'urea', 'shampoo', 'acondicionador', 'jabón de manos',
        'prensa', 'maquina', 'tortilladora', 'utensilio', 'estanteria', 'lavadora',
        'juguete', 'lego', 'figura', 'muñeca', 'juego de mesa', 'hot wheels',
        'limpiador', 'detergente', 'suavizante', 'cloro', 'lavatrastes',
        'canva', 'cuadro', 'decoracion', 'arrocera', 'sarten', 'bateria de cocina',
        'vaso', 'taza', 'termo', 'almohada', 'sabana', 'colchon', 'accesorios',
        'ablandador','martillo','recargas','decorativa','decorativo','modelo',
        'desodorante','desodorizado','ampolla','lorann', 'esencia', 'esencias', 'perfume',
        'colonia', 'maquillaje', 'brocha de','aroma','protein','pulverizadora','pastel',
        'caja transparente','plano','plegado','cuero','manos','cuaderno','descorazonador',
        'kuchen','bolsillo','engranajes','espuma','extractor','estabilizadora','estabilizador',
        'juego','junta','muebles','pasta dental','plato','cortador','regla','separador',
        'perros','perro','gatos','gato','suplemento','vantal','vendaje','vino', 'quinoa',
        'monedero', 'abril', 'precio', 'compra','llevate',
    ]

    def es_comestible(nombre):
        if "Verifica tu identidad" in nombre: return False
        n = normalizar_texto(nombre)
        for p in palabras_prohibidas:
            if p in n: return False
        return True

    df = df[df['nombre'].apply(es_comestible)].copy()

    # EXTRACCIÓN DE UNIDADES Y PRECIO UNITARIO
    def extraer_unidades(nombre):
        n = normalizar_texto(nombre)
        # Busca: número + espacio opcional + unidad
        patron = r'(\d+\.?\d*)\s*(l|ml|g|kg|pzas|pzs|grs|piezas)'
        match = re.search(patron, n)
        if match:
            cantidad = float(match.group(1))
            unidad = match.group(2)
            # Estandarizacion
            if 'ml' in unidad: cantidad /= 1000; unidad = 'L'
            elif unidad == 'l': unidad = 'L'
            elif unidad in ['g', 'grs']: cantidad /= 1000; unidad = 'kg'
            elif 'pza' in unidad or 'pzs' in unidad: unidad = 'pzas'
            return cantidad, unidad
        return 1.0, 'unidad'

    df[['cant_std', 'unit_std']] = df['nombre'].apply(lambda x: pd.Series(extraer_unidades(x)))
    df['precio_unitario'] = df['precio_num'] / df['cant_std']

    # re categorizar
    # Mapa para mover productos de "Otros" a categorías reales
    mapa_categorias = {
        'leche': 'Lacteos', 'queso': 'Lacteos', 'yoghurt': 'Lacteos',
        'frijol': 'Legumbres', 'arroz': 'Granos', 'aceite': 'Aceites',
        'huevo': 'Huevo', 'pollo': 'Carnes', 'res': 'Carnes', 'cerdo': 'Carnes',
        'pasta': 'Pastas', 'pan': 'Panadería', 'manzana': 'Frutas', 'platano': 'Frutas',
        'cebolla': 'Verduras', 'jitomate': 'Verduras', 'harina': 'Abarrotes',
        'sopa':'Pastas','tortilla': 'Tortilla','tortillas de harina': 'Tortillas de harina',

    }

    def asignar_categoria(row):
        nombre = normalizar_texto(row['nombre'])
        cat_orig = str(row.get('categoria', 'Otros')).lower()
        if 'otros' in cat_orig or cat_orig == 'nan' or cat_orig == '':
            for clave, valor in mapa_categorias.items():
                if clave in nombre: return valor
            return "Otros / Sin Clasificar"
        return cat_orig.capitalize()

    df['categoria_limpia'] = df.apply(asignar_categoria, axis=1)

    # 6. DETECCIÓN DE OUTLIERS (OPCIONAL)
    def marcar_outliers(group):
        if len(group) < 3: return [False] * len(group)
        z_scores = (group - group.mean()) / (group.std() + 1e-6)
        return np.abs(z_scores) > 3

    df['posible_error_precio'] = df.groupby('categoria_limpia')['precio_num'].transform(marcar_outliers)

    # 7. GUARDADO FINAL
    df.to_csv(archivo_salida_csv, index=False)
    print(f"Proceso terminado. Archivo '{archivo_salida_csv}' generado con éxito.")
    print(f"Productos finales: {len(df)}")

# EJECUCIÓN
limpieza('datos.json', 'geoprecio_clean.csv')


df= pd.read_csv('geoprecio_clean.csv')
print(df.head())