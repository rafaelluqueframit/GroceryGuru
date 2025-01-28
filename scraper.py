import requests
from bs4 import BeautifulSoup
import time
from playwright.sync_api import sync_playwright
from Producto import Producto
import subprocess


def textoNoDelimitador(texto, dInicial, dFinal):
    indice_ini = texto.find(dInicial)
    if indice_ini == -1:
        return None
    indice_ini += len(dInicial)
    
    indice_fin = texto.find(dFinal, indice_ini)
    if indice_fin == -1:
        return None
    
    return texto[indice_ini:indice_fin].strip()


class Scraper:
    def __init__(self, producto):
        self.producto = producto
        self.listaProductos = []
        #subprocess.run(["playwright", "install", "chromium"])


    ########################### SCRAPER HIPERCOR #########################################

    # def scrape_hipercor(self):
    #     #print("entro en scrap de hipercor")

    #     with sync_playwright() as p:
    #         browser = p.chromium.launch(headless=False, args=['--disable-http2'])
            
    #         context = browser.new_context()
    #         page = context.new_page()
    #         url_base = "https://www.hipercor.es"
    #         url_baseFoto = "https:"
    #         url = f"https://www.hipercor.es/supermercado/buscar/?term={self.producto}"
    #         page.goto(url, timeout=60000)  # Incrementar el timeout a 60 segundos
    #         #page.goto(url, wait_until='networkidle')
    #         page.wait_for_timeout(5000)  # Esperar 5 segundos adicionales
    #         time.sleep(5)  # Espera 5 segundos para que la página se cargue completamente
    #         #print("entro en scrap de hipercor4")

    #         try:
    #             # Usa el locator para seleccionar los productos
    #             resultados = page.locator('div.js-product').all()
    #             #print(f"Número de resultados encontrados: {len(resultados)}")
    #             for resultado in resultados:
    #                 try:
    #                     nombre = resultado.locator('h3.product_tile-description').inner_text(timeout=5000).strip()
                        
    #                     # Verificar si existe el precio en oferta
    #                     if resultado.locator('div.prices-price._offer').count() > 0:
    #                         precio = resultado.locator('div.prices-price._offer').inner_text(timeout=5000).strip()
    #                     else:
    #                         precio = resultado.locator('div.prices-price._current').inner_text(timeout=5000).strip()
                        
    #                     enlace_relativo = resultado.locator('a.link.event.js-product-link').get_attribute('href')
    #                     enlace = f"{url_base}{enlace_relativo}"

    #                     urlImagen_relativo = resultado.locator('img').get_attribute('src')
    #                     urlImagen = f"{url_baseFoto}{urlImagen_relativo}"

    #                     producto = Producto(precio, nombre, enlace, "Hipercor", "Hipercor", urlImagen)
    #                     self.listaProductos.append(producto)
    #                 except Exception as e:
    #                     print(f"Error al procesar un producto: {e}")
    #                     continue
    #         except Exception as e:
    #             print(f"Error al encontrar resultados: {e}")

    #         browser.close()

    #     return self.listaProductos


    ########################### SCRAPER DIA #########################################

    def scraper_dia(self):

        url1 = "https://www.dia.es/search?q="
        url = url1 + self.producto

        headers = {
		    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
		    'Accept-Language': 'en-US,en;q=0.8',
		    'Referer': 'https://www.google.com/',
		    'Accept-Encoding': 'gzip, deflate, br',
		    'Connection': 'keep-alive',
		}

        respuesta = requests.get(url, headers=headers)
        #print("Hago busqueda de Dia")
        if respuesta.status_code == 200 or respuesta.status_code == 403:
            document = BeautifulSoup(respuesta.content, "html.parser")       
            
            productos = document.select("li.search-product-card-list__item-container")
            #print("He entrado en Dia")
            for p in productos:
                titulo = ""
                precio = ""
                link = ""
                urlImagen = ""

                titulo = textoNoDelimitador(str(p.select('p.search-product-card__product-name')), ">", "<")

                precio = textoNoDelimitador(str(p.select('p.search-product-card__active-price')), ">", "<")

                url2 = "https://www.dia.es"
                link = url2 + p.select("a.search-product-card__product-image-link")[0]["href"]
                
                if len(p.select("img.search-product-card__product-image")) > 0:
                    urlImagen = url2 + p.select("img.search-product-card__product-image")[0]["src"]
                
                product = Producto(precio, titulo, link, "Dia", "dia", urlImagen)
                self.listaProductos.append(product)

        else:
            print("El Status Code no es OK es: " + str(respuesta.status_code))
    

#################################### SCRAPER AMAZON ######################################################################

    def scraper_amazon(self):

        url1 = "https://www.amazon.es/s?k="
        url = url1 + self.producto

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
            'Accept-Language': 'en-US,en;q=0.8',
            'Referer': 'https://www.google.com/',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
        }

        respuesta = requests.get(url, headers=headers)
        
        if respuesta.status_code == 200 or respuesta.status_code == 403:
            document = BeautifulSoup(respuesta.content, "html.parser") 

            productos = document.find_all("div", class_="sg-col-4-of-24 sg-col-4-of-12 s-result-item s-asin sg-col-4-of-16 sg-col s-widget-spacing-small sg-col-4-of-20")
            for p in productos:
                titulo = ""
                precio = ""
                link = ""
                urlImagen = ""

                titulo = textoNoDelimitador(str(p.select('span.a-size-base-plus.a-color-base.a-text-normal')), ">", "<")

                precio = textoNoDelimitador(str(p.select('span.a-offscreen')), ">", "<")

                url2 = "https://www.amazon.es/"
                link = url2 + p.select("a.a-link-normal.s-no-outline")[0]["href"]
                
                if len(p.select("img.s-image")) > 0:
                    urlImagen = p.select("img.s-image")[0]["src"]

                product = Producto(precio, titulo, link, "Amazon", "amazon", urlImagen)

                self.listaProductos.append(product)
        else:
            print("El Status Code no es OK es: " + str(respuesta.status_code))

    ###############################################################################

    def getListaProductos(self):
        return self.listaProductos

    def buscar(self):
        #self.scrape_hipercor()
        self.scraper_dia()
        self.scraper_amazon()        

        return self.listaProductos
    
    
