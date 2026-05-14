import requests
from bs4 import BeautifulSoup
import json
import time
import random
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from config import get_headers, URLS_BASE

def get_session():
    session = requests.Session()
    try:
        main_url = "https://www.bodegaaurrera.com.mx/"
        session.get(main_url, headers=get_headers(), timeout=10)
    except:
        pass
    
    retry = Retry(total=3, backoff_factor=2, status_forcelist=[403, 429, 500, 502, 503, 504])
    session.mount("https://", HTTPAdapter(max_retries=retry))
    return session

def get_links_bodega(producto):
    session = get_session()
    url = f"{URLS_BASE['bodega_aurrera']}{producto}"
    try:
        time.sleep(random.uniform(5, 10))
        response = session.get(url, headers=get_headers(), timeout=15)
        
        if "px-captcha" in response.text or response.status_code == 403:
            return ["BLOQUEO_BOT"]

        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            links = set()
            for a in soup.find_all('a', href=True):
                if '/ip/' in a['href'] and 'bodegaaurrera' in a['href']:
                    links.add(a['href'].split('?')[0])
            return list(links)
    except Exception as e:
        print(f"Error BA Links: {e}")
    return []

def extract_details_bodega(url):
    if url == "BLOQUEO_BOT": return {"nombre": "BLOQUEO_BOT", "url": "N/A"}
    
    session = get_session()
    try:
        time.sleep(random.uniform(5, 12))
        response = session.get(url, headers=get_headers(referer=URLS_BASE['bodega_aurrera']), timeout=15)
        
        if "px-captcha" in response.text or response.status_code == 403:
            return {"nombre": "BLOQUEO_BOT", "precio": "0.00", "url": url}

        soup = BeautifulSoup(response.content, 'html.parser')
        script_data = soup.find('script', id='__NEXT_DATA__')
        
        if script_data:
            data = json.loads(script_data.string)
            p = data.get('props', {}).get('pageProps', {}).get('initialData', {}).get('data', {}).get('product', {})
            if p:
                return {
                    "nombre": p.get('name', 'N/A'),
                    "precio": f"{p.get('priceInfo', {}).get('currentPrice', {}).get('price', 0):.2f}",
                    "tienda": "Bodega Aurrera",
                    "url": url
                }
    except:
        pass
    return None