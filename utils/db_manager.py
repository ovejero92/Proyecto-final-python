import sqlite3
from config import DB_NAME, TABLE_NAME
from utils.helpers import imprimir_error

def conectar_db():
    return sqlite3.connect(DB_NAME)

def inicializar_db():
    try:
        with conectar_db() as conn:
            cursor = conn.cursor()
            sql = f'''
            CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                descripcion TEXT,
                cantidad INTEGER NOT NULL,
                precio REAL NOT NULL,
                categoria TEXT
            )
            '''
            cursor.execute(sql)
            cursor.execute('''
                    CREATE TABLE IF NOT EXISTS ventas (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            id_producto INTEGER,
                            cantidad_vendida INTEGER,
                            total REAL,
                            fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                            FOREIGN KEY(id_producto) REFERENCES productos(id)
                        )
                    ''')
            conn.commit()
    except sqlite3.Error as e:
        imprimir_error(f"Error al inicializar la BD: {e}")

def registrar_producto(nombre, descripcion, cantidad, precio, categoria):
    try:
        with conectar_db() as conn:
            cursor = conn.cursor()
            cursor.execute(f"INSERT INTO {TABLE_NAME} (nombre, descripcion, cantidad, precio, categoria) VALUES (?, ?, ?, ?, ?)",
                           (nombre, descripcion, cantidad, precio, categoria))
            conn.commit()
            return True
    except sqlite3.Error as e:
        imprimir_error(f"Error al registrar: {e}")
        return False

def obtener_productos():
    try:
        with conectar_db() as conn:
            cursor = conn.cursor()
            cursor.execute(f"SELECT * FROM {TABLE_NAME}")
            return cursor.fetchall()
    except sqlite3.Error as e:
        imprimir_error(f"Error al leer datos: {e}")
        return []

def buscar_producto_id(id_prod):
    try:
        with conectar_db() as conn:
            cursor = conn.cursor()
            cursor.execute(f"SELECT * FROM {TABLE_NAME} WHERE id = ?", (id_prod,))
            return cursor.fetchone()
    except sqlite3.Error as e:
        imprimir_error(f"Error al buscar: {e}")
        return None

def buscar_producto_texto(termino):
    try:
        with conectar_db() as conn:
            cursor = conn.cursor()
            query = f"SELECT * FROM {TABLE_NAME} WHERE nombre LIKE ? OR categoria LIKE ?"
            cursor.execute(query, (f'%{termino}%', f'%{termino}%'))
            return cursor.fetchall()
    except sqlite3.Error as e:
        imprimir_error(f"Error al buscar: {e}")
        return []

def actualizar_producto(id_prod, nombre, descripcion, cantidad, precio, categoria):
    try:
        with conectar_db() as conn:
            cursor = conn.cursor()
            sql = f'''UPDATE {TABLE_NAME} SET 
                      nombre=?, descripcion=?, cantidad=?, precio=?, categoria=? 
                      WHERE id=?'''
            cursor.execute(sql, (nombre, descripcion, cantidad, precio, categoria, id_prod))
            if cursor.rowcount > 0:
                conn.commit()
                return True
            return False
    except sqlite3.Error as e:
        imprimir_error(f"Error al actualizar: {e}")
        return False

def eliminar_producto(id_prod):
    try:
        with conectar_db() as conn:
            cursor = conn.cursor()
            cursor.execute(f"DELETE FROM {TABLE_NAME} WHERE id = ?", (id_prod,))
            if cursor.rowcount > 0:
                conn.commit()
                return True
            return False
    except sqlite3.Error as e:
        imprimir_error(f"Error al eliminar: {e}")
        return False

def reporte_bajo_stock(limite):
    try:
        with conectar_db() as conn:
            cursor = conn.cursor()
            cursor.execute(f"SELECT * FROM {TABLE_NAME} WHERE cantidad <= ?", (limite,))
            return cursor.fetchall()
    except sqlite3.Error as e:
        imprimir_error(f"Error en reporte: {e}")
        return []

def realizar_venta_transaccional(id_prod, cantidad_vender):
    try:
        conn = conectar_db()
        cursor = conn.cursor()
        
        cursor.execute(f"SELECT precio, cantidad FROM {TABLE_NAME} WHERE id = ?", (id_prod,))
        producto = cursor.fetchone()
        
        if not producto:
            print("❌ Producto no existe.")
            return False
            
        precio, stock_actual = producto
        
        if stock_actual < cantidad_vender:
            print(f"❌ Stock insuficiente. Solo quedan {stock_actual}.")
            return False

        try:
            nuevo_stock = stock_actual - cantidad_vender
            cursor.execute(f"UPDATE {TABLE_NAME} SET cantidad = ? WHERE id = ?", (nuevo_stock, id_prod))
            
            total = precio * cantidad_vender
            cursor.execute("INSERT INTO ventas (id_producto, cantidad_vendida, total) VALUES (?, ?, ?)", 
                           (id_prod, cantidad_vender, total))
            conn.commit()
            return True
            
        except Exception as e:
            conn.rollback()
            imprimir_error(f"Transacción fallida. Se hizo ROLLBACK: {e}")
            return False
    finally:
        conn.close()
        

def obtener_historial_ventas():
    try:
        with conectar_db() as conn:
            cursor = conn.cursor()
            sql = '''
                SELECT v.id, p.nombre, v.cantidad_vendida, v.total, v.fecha 
                FROM ventas v
                JOIN productos p ON v.id_producto = p.id
                ORDER BY v.fecha DESC
            '''
            cursor.execute(sql)
            return cursor.fetchall()
    except sqlite3.Error as e:
        imprimir_error(f"Error al obtener ventas: {e}")
        return []