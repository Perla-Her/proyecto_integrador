# import requests
# from bs4 import BeautifulSoup
# import json
# import time
# import random
# import re
# from config import HEADERS, URLS_BASE

# session = requests.Session()

# def get_links_soriana(producto):
#     """Busca productos en Soriana y extrae links de productos (/p/)."""
#     url = f"{URLS_BASE['soriana']}{producto}"
    
#     try:
#         time.sleep(random.uniform(2, 5))
        
#         headers = HEADERS()
#         response = session.get(url, headers=headers, timeout=30)
        
#         if response.status_code == 200:
#             soup = BeautifulSoup(response.content, 'html.parser')
#             links = []
            
#             for a in soup.find_all('a', href=True):
#                 href = a['href']
#                 if '/p/' in href:
#                     if href.startswith('http'):
#                         full_url = href
#                     else:
#                         full_url = f"https://www.soriana.com{href}"
#                     links.append(full_url)
            
#             return list(set(links))
#         elif response.status_code == 403:
#             print("Soriana: Acceso denegado (403). La IP podría estar marcada temporalmente.")
#             return []
#         else:
#             print(f"Soriana respondió con status: {response.status_code}")
            
#     except Exception as e:
#         print(f"Error buscando en Soriana: {e}")
#     return []

# def extract_details_soriana(url):
#     """Extrae nombre y precio usando metadatos de SEO para mayor robustez."""
#     try:
#         time.sleep(random.uniform(1, 3))
#         headers = HEADERS()
#         response = session.get(url, headers=headers, timeout=25)
        
#         if response.status_code != 200:
#             return None

#         soup = BeautifulSoup(response.content, 'html.parser')

#         nombre_tag = (
#             soup.find('meta', property='og:title') or 
#             soup.find('h1')
#         )
        
#         if nombre_tag.name == 'meta':
#             nombre = nombre_tag.get('content', 'N/A')
#         else:
#             nombre = nombre_tag.get_text(strip=True) if nombre_tag else "N/A"

#         precio = "0.00"
        
#         meta_price = (
#             soup.find('meta', property='product:price:amount') or 
#             soup.find('meta', property='og:price:amount') or
#             soup.find('meta', itemprop='price')
#         )
        
#         if meta_price:
#             precio_raw = meta_price.get('content', '0.00')
#             precio = "".join(re.findall(r"[-+]?\d*\.\d+|\d+", precio_raw.replace(',', '')))
#         else:
#             precio_tag = soup.find('span', class_='pdp-price') or soup.find('span', class_='sales')
#             if precio_tag:
#                 raw_price = precio_tag.get_text(strip=True)
#                 precio = "".join(re.findall(r"[-+]?\d*\.\d+|\d+", raw_price.replace(',', '')))

#         return {
#             "nombre": nombre,
#             "precio": precio,
#             "tienda": "Soriana",
#             "url": url
#         }
#     except Exception as e:
#         print(f"Error en detalle Soriana para {url}: {e}")
#         return None