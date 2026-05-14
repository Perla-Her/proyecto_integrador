import requests
from bs4 import BeautifulSoup
import time
import random
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from config import get_headers, URLS_BASE

def get_session():
    session = requests.Session()
    retry = Retry(total=3, backoff_factor=1, status_forcelist=[429, 500, 502, 503, 504])
    adapter = HTTPAdapter(max_retries=retry)
    session.mount("https://", adapter)
    return session

def get_product_links(search_query):
    session = get_session()
    url = f"{URLS_BASE['walmart']}{search_query}"
    try:
        time.sleep(random.uniform(2, 5))
        response = session.get(url, headers=get_headers(), timeout=15)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            links = set()
            for a in soup.find_all('a', href=True):
                if '/ip/' in a['href']:
                    href = a['href']
                    full_url = href if href.startswith('http') else f"https://www.walmart.com.mx{href}"
                    links.add(full_url.split('?')[0])
            return list(links)
    except Exception as e:
        print(f"Error en Walmart (links): {e}")
    return []

def extract_product_details(url):
    session = get_session()
    try:
        time.sleep(random.uniform(3, 6))
        headers = get_headers(referer=URLS_BASE['walmart'])
        response = session.get(url, headers=headers, timeout=15)
        
        if "Verifica tu identidad" in response.text or response.status_code == 403:
            return {"nombre": "BLOQUEO_BOT", "precio": "0.00", "url": url}

        soup = BeautifulSoup(response.content, 'html.parser')
        title_tag = soup.find('h1', {'itemprop': 'name'}) or soup.find('h1')
        price_tag = soup.find('span', {'itemprop': 'price'}) or soup.find('span', {'item-id': 'price'})
        
        if title_tag and price_tag:
            return {
                "nombre": title_tag.get_text(strip=True),
                "precio": price_tag.get_text(strip=True),
                "tienda": "Walmart",
                "url": url
            }
    except Exception as e:
        print(f"Error en Walmart (detalles): {e}")
    return None