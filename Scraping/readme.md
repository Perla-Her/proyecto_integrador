Esta carpeta contiene los archivos de codigo con elque se realizo el scraping.

* config_products.py contiene un diccinario con la lista de las categorias y productos elegidos dentreo de ella. Para fines del proyecto no se utilizaron todas.
* config.py contiene los user agents para simular las sesiones desde distintos navegadors, asi como las urls de las tiendas scrapeadas.
* db_handler contiene una clase desde la cual se crean los documentos json para almacenar en MONGO DB Compass los datos html obtenidos de ona forma mas ordenada y limpia
* scrap_wa, scrap_ba, scrap_fgdl, scrap_sor, scrap_lacoer, son los codigos scraping, no todos funcionaron y se opto por solo utilizar los que daban resultados, se usaron librerias como rquest, bs4(beautifoulsoup),time, re, ullib3 y json
* main_scrap.py ejecuta los cosdigos scrap, db_handler y config_products para su almacenamiento
* limpieza_scrap.py se ejecuto para eliminar duplicados
* process_offline.py guarda documentos json en Mongo DB que se hayan obtenido de manera manual
