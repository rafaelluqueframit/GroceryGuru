class Producto:
    def __init__(self, precio, nombre, enlace, supermercado, logo, urlImagen):
        self.precio = precio
        self.nombre = nombre
        self.enlace = enlace
        self.supermercado = supermercado
        self.logo = logo
        self.urlImagen = urlImagen
        
    def getPrecio(self):
        return self.precio
    
    def setPrecio(self, precio):
        self.precio = precio
    
    def getNombre(self):
        return self.nombre
    
    def setNombre(self, nombre):
        self.nombre = nombre
    
    def getEnlace(self):
        return self.enlace
    
    def setEnlace(self, enlace):
        self.enlace = enlace

    def getSupermercado(self):
        return self.supermercado
    
    def setSupermercado(self, supermercado):
        self.supermercado = supermercado
    
    def getLogo(self):
        return self.logo
    
    def setLogo(self, logo):
        self.logo = logo

    def getUrlImagen(self):
        return self.urlImagen
    
    def setUrlImagen(self, urlImagen):
        self.urlImagen = urlImagen