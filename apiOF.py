import requests
from Producto import Producto

class apiOF:

    def __init__(self, producto):
        self.producto = producto
        self.listaProductos = []

    def search_OpenFood(self):
        url = f"https://world.openfoodfacts.org/cgi/search.pl?search_terms={self.producto}&search_simple=1&action=process&json=1"

        respuesta = requests.get(url)
        data = respuesta.json()

        if "products" in data:
            for producto in data["products"]:
                precio = "Precio no disponible"
                titulo = producto.get("product_name", "")
                link = producto.get("url", "")
                supermercado = producto.get("stores", "")
                urlImagen = producto.get("image_front_url", "")

                producto = Producto(precio, titulo, link, supermercado, "openfood", urlImagen)
                self.listaProductos.append(producto)

        return self.listaProductos
    
