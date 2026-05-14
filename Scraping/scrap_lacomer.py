# import requests
# import time
# import random
# import re
# from config import HEADERS, URLS_BASE
# from bs4 import BeautifulSoup

# def get_links_lacomer(producto):
#     """
#     
#     url = f"https://www.lacomer.com.mx/lacomer/goBusqueda.action?term={producto}"
    
#     try:
#         time.sleep(random.uniform(2, 4))
#         response = requests.get(url, headers=HEADERS, timeout=20)
        
#         if response.status_code == 200:
#             links = []
#             soup = BeautifulSoup(response.content, 'html.parser')
            
#             for a in soup.find_all('a', href=True):
#                 href = a['href']
#                 if 'articulo' in href.lower() or '/p/' in href:
#                     full_url = href if href.startswith('http') else f"https://www.lacomer.com.mx{href}"
#                     links.append(full_url)
            
#             return list(set(links))
#     except Exception as e:
#         print(f"Error en links La Comer: {e}")
#     return []

# def extract_details_lacomer(url):
#     """Extrae detalles usando selectores actualizados y limpieza de datos."""
#     try:
#         time.sleep(random.uniform(1, 3))
#         response = requests.get(url, headers=HEADERS, timeout=20)
        
#         if response.status_code != 200:
#             return None

#         soup = BeautifulSoup(response.content, 'html.parser')
        
#         nombre_tag = (
#             soup.find('h1') or 
#             soup.find('div', class_='nombre-producto') or
#             soup.find('strong', class_='text-prod-detail')
#         )
#         nombre = nombre_tag.get_text(strip=True) if nombre_tag else "N/A"
        
#         precio_tag = (
#             soup.find('span', class_='precio_normal') or 
#             soup.find('div', class_='precio_art') or
#             soup.find('span', class_='com_pri') or
#             soup.find('meta', property='product:price:amount') # Metadatos
#         )
        
#         if precio_tag:
#             if precio_tag.name == 'meta':
#                 precio = precio_tag.get('content', '0.00')
#             else:
#                 raw_price = precio_tag.get_text(strip=True)
#                 match = re.search(r"(\d+\.\d+)", raw_price.replace(',', ''))
#                 precio = match.group(1) if match else "0.00"
#         else:
#             precio = "0.00"

#         return {
#             "nombre": nombre,
#             "precio": precio,
#             "tienda": "La Comer",
#             "url": url
#         }
#     except Exception as e:
#         print(f"Error en detalle La Comer: {e}")
#         return None