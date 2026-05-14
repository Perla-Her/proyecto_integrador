import threading
import time
import random
from db_handler import DBHandler
from config_products import PRODUCTOS_MONITOREO

from scrap_wal import get_product_links, extract_product_details
from scrap_ba import get_links_bodega, extract_details_bodega
#from scrap_lacomer import get_links_lacomer, extract_details_lacomer


MAX_CARACTERES = 200
PALABRAS_NEGATIVAS = [
    'prensa', 'maquina', 'tortilladora', 'comal', 'electrodomestico', 
    'set', 'kit', 'juego de', 'organizador', 'molino', 'vaporera',
    'olla', 'sarten', 'estuche', 'dispensador', 'soporte', 'funda',
    'base para', 'repuesto', 'tapa', 'shampoo', 'crema de ducha', 'sombra',
    'perfume', 'colonia', 'desodorante', 'maquillaje', 'brocha de', 'esmalte',
    'accesorio', 'herramienta', 'utensilio', 'cuchillo', 'tabla de cortar',
    'licuadora', 'batidora', 'procesador de alimentos', 'cafetera',
    'hot cakes', 'wafflera', 'freidora', 'parrilla', 'plancha', 'horno',
    'microondas', 'refrigerador', 'congelador', 'lavadora',
    'pastel'

]

def producto_es_valido(nombre):
    """Valida que el producto sea un alimento/insumo y no un accesorio o cosmético."""
    nombre_low = nombre.lower()
    if len(nombre) > MAX_CARACTERES:
        return False, "Longitud"
    if any(neg in nombre_low for neg in PALABRAS_NEGATIVAS):
        return False, "Categoría/Accesorio"
    return True, "OK"

def procesar_tienda(tienda, producto, categoria, db):
    """Ejecuta el scraping para una tienda específica con manejo de bloqueos."""
    try:
        time.sleep(random.uniform(2, 6))
        
        links = tienda['l_func'](producto)
        
        if not links or "BLOQUEO_BOT" in links:
            if links and "BLOQUEO_BOT" in links:
                print(f"!!! {tienda['nombre']} detectó actividad (CAPTCHA). Saltando ronda... !!!")
            return

        links_limpios = [l for l in links if not any(n in l.lower() for n in PALABRAS_NEGATIVAS)]
        
        if not links_limpios:
            return

        link = random.choice(links_limpios)
        datos = tienda['d_func'](link)
        
        if not datos:
            return
            
        if datos.get('nombre') == "BLOQUEO_BOT":
            print(f"!!! Bloqueo detectado en detalle de {tienda['nombre']} !!!")
            return

        precio_val = datos.get('precio')
        if precio_val and precio_val not in ["0.00", "0", 0, None, "No encontrado"]:
            valido, motivo = producto_es_valido(datos['nombre'])
            
            if valido:
                datos['categoria'] = categoria
                db.guardar_producto(datos)
            else:
                print(f"{tienda['nombre']} descartó ({motivo}): {datos['nombre'][:25]}...")
        
        time.sleep(random.uniform(5, 10))
            
    except Exception as e:
        print(f"Error crítico en hilo {tienda['nombre']}: {e}")

def ejecutar_ciclo_simultaneo():
    """Coordina la búsqueda aleatoria de productos en todas las tiendas configuradas."""
    db = DBHandler()
    tiendas = [
        #{"nombre": "Walmart", "l_func": get_product_links, "d_func": extract_product_details},
        #{"nombre": "Bodega Aurrera", "l_func": get_links_bodega, "d_func": extract_details_bodega},
        #{"nombre": "La Comer", "l_func": get_links_lacomer, "d_func": extract_details_lacomer}
    ]

    for i in range(5): 
        cat = random.choice(list(PRODUCTOS_MONITOREO.keys()))
        prod = random.choice(PRODUCTOS_MONITOREO[cat])
        
        print(f"\n--- Ronda {i+1}/5 | Buscando: {prod.upper()} ---")
        
        hilos = []
        for t in tiendas:
            h = threading.Thread(target=procesar_tienda, args=(t, prod, cat, db))
            hilos.append(h)
            h.start()
        
        for h in hilos: 
            h.join()
        
        time.sleep(random.uniform(15, 25))

if __name__ == "__main__":
    print("=== GeoPrecio: Sistema de Monitoreo Iniciado ===")
    while True:
        try:
            ejecutar_ciclo_simultaneo()
            
            espera = random.randint(1800, 3600) 
            print(f"\nCiclo finalizado. Esperando {espera // 60} minutos para el siguiente...")
            time.sleep(espera)
            
        except KeyboardInterrupt:
            print("\nDeteniendo sistema GeoPrecio...")
            break