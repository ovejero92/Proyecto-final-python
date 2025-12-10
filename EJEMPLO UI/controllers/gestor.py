from data.db_manager import DBManager

class InventarioController:
    def __init__(self):
        self.db = DBManager()
        self.db.inicializar_db()

    def obtener_todos(self):
        return self.db.obtener_productos()

    def guardar_producto(self, nombre, desc, cant, precio, cat, id_prod=None):
        if not nombre:
            raise ValueError("El nombre es obligatorio.")
        
        try:
            cantidad = int(cant)
            precio_val = float(precio)
            if cantidad < 0 or precio_val < 0:
                raise ValueError("Cantidad y precio deben ser positivos.")
        except ValueError:
            raise ValueError("Cantidad y Precio deben ser números válidos.")

        datos = {
            'nombre': nombre, 'desc': desc, 
            'cant': cantidad, 'precio': precio_val, 'cat': cat
        }

        if id_prod:
            self.db.actualizar_producto(id_prod, datos)
        else:
            self.db.registrar_producto(datos)

    def eliminar(self, id_prod):
        self.db.eliminar_producto(id_prod)

    def realizar_venta(self, id_prod_str, cant_str):
        if not id_prod_str or not cant_str:
            raise ValueError("Complete todos los campos de venta.")
        
        try:
            id_prod = int(id_prod_str)
            cant = int(cant_str)
            if cant <= 0:
                raise ValueError("La cantidad a vender debe ser mayor a 0.")
        except ValueError:
            raise ValueError("ID y Cantidad deben ser números enteros.")

        return self.db.procesar_venta(id_prod, cant)

    def ver_historial(self):
        return self.db.obtener_historial()