# import requests
# from bs4 import BeautifulSoup
# import time
# import random
# import re
# from config import HEADERS, URLS_BASE

# def get_links_gdl(producto):
#     """Busca productos en Farmacias Guadalajara."""
#     # La URL de búsqueda suele requerir parámetros adicionales para ser efectiva
#     url = f"{URLS_BASE['farmacias_gdl']}{producto}"
    
#     try:
#         time.sleep(random.uniform(2, 4))
#         # En Farmacias GDL a veces ayuda no enviar tantos headers de 'Accept' si fallan
#         response = requests.get(url, headers=HEADERS, timeout=30)
        
#         if response.status_code == 200:
#             soup = BeautifulSoup(response.content, 'html.parser')
#             links = []
            
#             # Los links de productos en GDL suelen estar en contenedores con clase 'product_name'
#             # o directamente en etiquetas 'a' que contienen el slug del producto
#             for a in soup.find_all('a', href=True):
#                 href = a['href']
#                 # Filtro específico para el patrón de URL de productos de GDL
#                 if '/es/guadalajara/' in href and '.html' in href:
#                     full_url = href if href.startswith('http') else f"https://www.farmaciasguadalajara.com{href}"
#                     links.append(full_url)
            
#             return list(set(links))
#         else:
#             print(f"Farmacias GDL respondió con status: {response.status_code}")
            
#     except Exception as e:
#         print(f"Error al buscar en Farmacias Gdl: {e}")
#     return []

# def extract_details_gdl(url):
#     """Extrae nombre y precio de la página de producto."""
#     try:
#         time.sleep(random.uniform(1, 3))
#         response = requests.get(url, headers=HEADERS, timeout=25)
        
#         if response.status_code != 200:
#             return None

#         soup = BeautifulSoup(response.content, 'html.parser')
        
#         # --- EXTRACCIÓN DE NOMBRE ---
#         # GDL usa mucho la clase 'product-name' o etiquetas h1 simples
#         nombre_tag = soup.find('h1') or soup.find('span', class_='product--name')
#         nombre = nombre_tag.get_text(strip=True) if nombre_tag else "N/A"
        
#         # --- EXTRACCIÓN DE PRECIO ---
#         # El precio en GDL suele estar en un span con clase 'price' o dentro de un div con 'product-price'
#         precio_tag = (
#             soup.find('span', class_='price') or 
#             soup.find('div', class_='product--price') or
#             soup.find('span', {'itemprop': 'price'})
#         )
        
#         if precio_tag:
#             # Limpiamos el texto ($120.00 -> 120.00)
#             raw_price = precio_tag.get_text(strip=True)
#             # Expresión regular para capturar solo el número decimal
#             match = re.search(r"(\d+\.\d+)", raw_price.replace(',', ''))
#             precio = match.group(1) if match else "0.00"
#         else:
#             precio = "0.00"

#         return {
#             "nombre": nombre,
#             "precio": precio,
#             "tienda": "Farmacias Guadalajara",
#             "url": url
#         }
#     except Exception as e:
#         print(f"Error en detalle GDL para {url}: {e}")
#         return None

# if __name__ == "__main__":
#     print("Probando Farmacias Guadalajara...")
#     links = get_links_gdl("panales")
#     if links:
#         print(f"Se encontraron {len(links)} links.")
#         print(extract_details_gdl(links[0]))