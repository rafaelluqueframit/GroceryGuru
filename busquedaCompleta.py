from scraper import Scraper
from apiOF import apiOF

class busquedaCompleta:
    def __init__(self, producto):
        self.producto = producto
        self.listaProductos = []
        
    def busquedaScraping(self):
        listaDesordenada = []
        listaDesordenada = Scraper(self.producto)
        
        self.listaProductos.extend(listaDesordenada.buscar())
    
    def busquedaOpenFood(self):
        listaDesordenada1 = []
        listaDesordenada1 = apiOF(self.producto)
        
        self.listaProductos.extend(listaDesordenada1.search_OpenFood())
    
    def busqueda(self):
    
        self.busquedaScraping()
        self.busquedaOpenFood()
        
        return self.listaProductos