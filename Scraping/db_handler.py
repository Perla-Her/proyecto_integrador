# from pymongo import MongoClient
# from datetime import datetime

# class DBHandler:
#     def __init__(self):
#         self.client = MongoClient('mongodb://localhost:27017/')
#         self.db = self.client['geoprecio_db']
#         self.collection = self.db['productos']

#     def guardar_producto(self, datos):
#         datos['fecha_actualizacion'] = datetime.now()
        
#         if isinstance(datos['precio'], str):
#             try:
#                 precio_limpio = datos['precio'].replace('$', '').replace(',', '').strip()
#                 precio_limpio = precio_limpio.split(' ')[0] 
#                 datos['precio_num'] = float(precio_limpio)
#             except:
#                 datos['precio_num'] = 0.0 
                
#         self.collection.update_one(
#             {'url': datos['url']},
#             {'$set': datos},
#             upsert=True
#         )
#         print(f"Base de Datos: Guardado/Actualizado {datos['nombre']}")

#     def obtener_todos(self):
#         return list(self.collection.find())





from pymongo import MongoClient, ASCENDING
from datetime import datetime
import re

class DBHandler:
    def __init__(self):
        self.client = MongoClient('mongodb://localhost:27017/')
        self.db = self.client['geoprecio_db']
        self.collection = self.db['productos']
        self.collection.create_index([("url", ASCENDING)], unique=True)

    def guardar_producto(self, datos):
        datos['fecha_actualizacion'] = datetime.now()
        
        if isinstance(datos.get('precio'), str):
            try:
                precio_limpio = re.sub(r'[^\d.]', '', datos['precio'])
                datos['precio_num'] = float(precio_limpio)
            except (ValueError, TypeError):
                datos['precio_num'] = 0.0
        elif isinstance(datos.get('precio'), (int, float)):
            datos['precio_num'] = float(datos['precio'])
        else:
            datos['precio_num'] = 0.0
                
        if datos.get('nombre') == "BLOQUEO_BOT":
            print(f"Alerta: Bloqueo detectado en {datos.get('tienda')}. No se guarda.")
            return

        self.collection.update_one(
            {'url': datos['url']},
            {'$set': datos},
            upsert=True
        )
        print(f"DB: {'Actualizado' if 'nombre' in datos else 'Guardado'} -> {datos.get('nombre', 'N/A')[:25]}")

        self.collection.update_one(
            {'url': datos['url']},
            {'$set': datos},
            upsert=True
        )

    def obtener_todos(self):
        return list(self.collection.find())