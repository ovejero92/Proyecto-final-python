from utils.helpers import ( imprimir_titulo, imprimir_exito, imprimir_error,
    validar_input_string, validar_input_float, validar_input_int
)
from utils import db_manager
import sys

def mostrar_tabla(productos):
    if not productos:
        print("No se encontraron productos.")
        return

    print(f"{'ID':<5} {'NOMBRE':<20} {'CATEGORIA':<15} {'PRECIO':<10} {'CANTIDAD':<10}")
    print("-" * 65)
    for prod in productos:
        print(f"{prod[0]:<5} {prod[1][:18]:<20} {prod[5][:13]:<15} ${prod[4]:<9.2f} {prod[3]:<10}")
    print("-" * 65)

def menu_registrar():
    imprimir_titulo("Registrar Nuevo Producto")
    nombre = validar_input_string("Nombre")
    desc = input("Descripción (opcional): ").strip()
    categ = validar_input_string("Categoría")
    cantidad = validar_input_int("Cantidad inicial")
    precio = validar_input_float("Precio unitario")
    
    if db_manager.registrar_producto(nombre, desc, cantidad, precio, categ):
        imprimir_exito("Producto registrado correctamente.")

def menu_mostrar():
    imprimir_titulo("Listado de Productos")
    productos = db_manager.obtener_productos()
    mostrar_tabla(productos)

def menu_actualizar():
    imprimir_titulo("Actualizar Producto")
    menu_mostrar()
    id_prod = validar_input_int("Ingrese el ID del producto a modificar")
    
    producto_actual = db_manager.buscar_producto_id(id_prod)
    if not producto_actual:
        imprimir_error("Producto no encontrado.")
        return

    print(f"Editando: {producto_actual[1]}")
    print("Deje vacío si no desea modificar el campo.")
    
    nuevo_nombre = input(f"Nombre [{producto_actual[1]}]: ").strip() or producto_actual[1]
    nueva_desc = input(f"Descripción [{producto_actual[2]}]: ").strip() or producto_actual[2]
    nueva_cat = input(f"Categoría [{producto_actual[5]}]: ").strip() or producto_actual[5]
    
    cant_str = input(f"Cantidad [{producto_actual[3]}]: ").strip()
    nuevo_cant = int(cant_str) if cant_str.isdigit() else producto_actual[3]
    
    precio_str = input(f"Precio [{producto_actual[4]}]: ").strip()
    nuevo_precio = float(precio_str) if precio_str else producto_actual[4]

    if db_manager.actualizar_producto(id_prod, nuevo_nombre, nueva_desc, nuevo_cant, nuevo_precio, nueva_cat):
        imprimir_exito("Producto actualizado.")
    else:
        imprimir_error("No se pudo actualizar.")

def menu_eliminar():
    imprimir_titulo("Eliminar Producto")
    menu_mostrar()

    id_prod = validar_input_int("ID del producto a eliminar")
    
    confirm = input(f"¿Seguro que desea eliminar el ID {id_prod}? (s/n): ").lower()
    if confirm == 's':
        if db_manager.eliminar_producto(id_prod):
            imprimir_exito("Producto eliminado.")
        else:
            imprimir_error("No se encontró ese ID.")

def menu_buscar():
    imprimir_titulo("Búsqueda de Productos")
    print("1. Buscar por ID")
    print("2. Buscar por Nombre o Categoría")
    opcion = input("Opción: ")
    
    if opcion == "1":
        id_prod = validar_input_int("ID")
        res = db_manager.buscar_producto_id(id_prod)
        if res:
            mostrar_tabla([res])
        else:
            imprimir_error("No encontrado.")
    elif opcion == "2":
        termino = validar_input_string("Término de búsqueda")
        res = db_manager.buscar_producto_texto(termino)
        mostrar_tabla(res)
    else:
        imprimir_error("Opción inválida.")

def menu_reporte():
    imprimir_titulo("Reporte de Bajo Stock")
    limite = validar_input_int("Ingrese el límite de cantidad para el reporte")
    res = db_manager.reporte_bajo_stock(limite)
    if res:
        imprimir_exito(f"Se encontraron {len(res)} productos con stock <= {limite}")
        mostrar_tabla(res)
    else:
        imprimir_exito("Todos los productos superan ese límite de stock.")

def main():
    db_manager.inicializar_db()
    
    while True:
        print("\n" + "="*30)
        print("   GESTIÓN DE INVENTARIO")
        print("="*30)
        print("1. Registrar Producto")
        print("2. Mostrar Todos")
        print("3. Actualizar Producto")
        print("4. Eliminar Producto")
        print("5. Buscar Producto")
        print("6. Reporte Bajo Stock")
        print("7. Salir")
        
        opcion = input("\nSeleccione una opción: ")
        
        if opcion == '1':
            menu_registrar()
        elif opcion == '2':
            menu_mostrar()
        elif opcion == '3':
            menu_actualizar()
        elif opcion == '4':
            menu_eliminar()
        elif opcion == '5':
            menu_buscar()
        elif opcion == '6':
            menu_reporte()
        elif opcion == '7':
            print("Saliendo del sistema...")
            sys.exit()
        else:
            imprimir_error("Opción no válida, intente nuevamente.")

if __name__ == "__main__":
    main()
