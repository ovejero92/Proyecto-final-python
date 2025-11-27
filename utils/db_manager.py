import sqlite3
from utils.helpers import imprimir_error
from config import BD_NAME, TABLE_NAME

def conectar_db():
    return sqlite3.connect(BD_NAME)

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
                categoria TEXT )
           '''
           cursor.execute(sql)
           conn.commit()
    except sqlite3.Error as e:
        imprimir_error(f"Error al iniciar la base de datos. {e}")
        
def registrar_producto(nombre,descripcion,cantidad,precio,categoria):
    try:
        with conectar_db() as conn:
            cursor = conn.cursor()
            cursor.execute(f"INSERT INTO {TABLE_NAME} (nombre,descripcion,cantidad,precio,categoria) VALUES (?,?,?,?,?)",(nombre,descripcion,cantidad,precio,categoria))
            conn.commit()
            return True
    except sqlite3.Error as e:
        imprimir_error(f"Error al registrar el producto. {e}")
        return False    

def obtener_productos():
    try:
        with conectar_db() as conn:
            cursor = conn.cursor()
            cursor.execute(f"SELECT * FROM {TABLE_NAME}")
            return cursor.fetchall()
    except sqlite3.Error as e:
        imprimir_error(f"Error al leer los datos. {e}")
        return []

def buscar_producto_id(id_prod):
    try:
        with conectar_db() as conn:
            cursor = conn.cursor()
            cursor.execute(f"SELECT * FROM {TABLE_NAME} WHERE id = ?",(id_prod) )
            return cursor.fetchone()
    except sqlite3.Error as e:
        imprimir_error(f"Error al buscar. {e}")
        return None
    
def buscar_producto_texto(termino):
    try:
        with conectar_db() as conn:
            cursor = conn.cursor()
            query = f"SELECT * FROM {TABLE_NAME} WHERE nombre LIKE ? OR categoria LIKE ?"
            cursor.execute(query,(f'%{termino}%',f'%{termino}%') )
            return cursor.fetchall()
    except sqlite3.Error as e:
        imprimir_error(f"Error al buscar. {e}")
        return []
    
def actualizar_producto(id_prod,nombre,decripcion,cantidad,precio,categoria):
    try:
        with conectar_db() as conn:
            cursor = conn.cursor()
            sql = f"UPDATE {TABLE_NAME} SET nombre=?, decripcion=?, cantidad=?, precio=?, categoria=? WHERE id =?"
            cursor.execute(sql,(nombre,decripcion,cantidad,precio,categoria,id_prod) )
            if cursor.rowcount > 0:
                conn.commit()
                return True
            return False
    except sqlite3.Error as e:
        imprimir_error(f"Error al actualizar. {e}")
        return False

def eliminar_producto(id_prod):
    try:
        with conectar_db() as conn:
            cursor = conn.cursor()
            cursor.execute(f"DELETE FROM {TABLE_NAME} WHERE id = ?", (id_prod))
            if cursor.rowcount > 0:
                conn.commit()
                return True
            return False
    except sqlite3.Error as e:
        imprimir_error(f"Error al eliminar. {e}")
        return False

def reporte_bajo_stock(limite):
    try:
        with conectar_db() as conn:
            cursor = conn.cursor()
            cursor.execute(f"SELECT * FROM {TABLE_NAME} WHERE cantidad <= ?", (limite))
            return cursor.fetchall()
    except sqlite3.Error as e:
        imprimir_error(f"Error en el reporte. {e}")
        return []