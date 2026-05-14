from pymongo import MongoClient

def limpiar_duplicados_geoprecio():
    client = MongoClient('mongodb://localhost:27017/')
    db = client['geoprecio_db']
    collection = db['productos']

    pipeline = [
        {
            "$group": {
                "_id": "$url", 
                "count": {"$sum": 1},
                "ids": {"$push": "$_id"}
            }
        },
        {
            "$match": {
                "count": {"$gt": 1}
            }
        }
    ]

    duplicados = list(collection.aggregate(pipeline))
    count_borrados = 0

    for doc in duplicados:
        ids_a_borrar = doc['ids'][1:] 
        collection.delete_many({"_id": {"$in": ids_a_borrar}})
        count_borrados += len(ids_a_borrar)

    print(f"=== Limpieza terminada: Se eliminaron {count_borrados} duplicados ===")

if __name__ == "__main__":
    limpiar_duplicados_geoprecio()