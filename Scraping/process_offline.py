import json
from db_handler import DBHandler
from config_products import PRODUCTOS_MONITOREO

def obtener_categoria_automatica(nombre_producto):
    """Busca el nombre del producto en las listas de config_products."""
    nombre_low = nombre_producto.lower()
    for categoria, subproductos in PRODUCTOS_MONITOREO.items():
        for sub in subproductos:
            if sub.lower() in nombre_low:
                return categoria
    return "Otros / Sin Clasificar"


def procesar_carga_inteligente(nombre_archivo):
    db = DBHandler()
    from main_scrap import producto_es_valido
    
    try:
        with open(nombre_archivo, 'r', encoding='utf-8') as f:
            productos = json.load(f)
        
        for p in productos:
            valido, motivo = producto_es_valido(p['nombre'])
            
            if valido:
                if p.get('categoria') in [None, "Despensa_Manual"]:
                    p['categoria'] = obtener_categoria_automatica(p['nombre'])
                db.guardar_producto(p)
            else:
                print(f"Saltando {p['nombre'][:20]} por: {motivo}")
                
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    procesar_carga_inteligente('datos.json')