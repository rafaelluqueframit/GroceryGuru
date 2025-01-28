# Guillermo López Jiménez y Rafael Luque Framit

from flask import Flask, render_template, request
from busquedaCompleta import busquedaCompleta

app = Flask(__name__)

listaProductos = []

def imprimirResultados(productos):
    for producto in productos:
        print("Nombre: " + producto.nombre)
        print("Precio: " + str(producto.precio))
        print("urlProducto: " + producto.enlace)
        print("Supermercado: " + producto.supermercado)
        print("Logo: " + producto.logo)
        print("urlImagen: " + producto.urlImagen)
        print("-------------------------------")

@app.route("/")
def index():
    global listaProductos
    listaProductos = []
    return render_template("index.html", lista=listaProductos)

@app.route("/procesar", methods=['GET'])
def procesar():
    global listaProductos
    
    producto_introducido = request.args.get("producto")
    criterio_orden = request.args.get("orden")
    
    if producto_introducido:
        cb = busquedaCompleta(producto_introducido)
        listaProductos = cb.busqueda()

        def obtener_precio_numerico(producto):
            precio = producto.getPrecio()
            if precio is None or precio == "Precio no disponible" or precio == "":
                return float('inf')
            try:
                precio_str = precio.replace("€", "").replace(",", ".").strip()
                return float(precio_str)
            except (ValueError, TypeError, AttributeError):
                return float('inf')

        if criterio_orden == "asc":
            listaProductos.sort(key=obtener_precio_numerico)
        elif criterio_orden == "desc":
            listaProductos.sort(key=obtener_precio_numerico, reverse=True)

        # # Imprimir depuración de precios
        # for producto in listaProductos:
        #     print(f"Producto: {producto.getNombre()}, Precio: {producto.getPrecio()}")

    return render_template("index.html", lista=listaProductos)

if __name__ == '__main__':
    app.run()
