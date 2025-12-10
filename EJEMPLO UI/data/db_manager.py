import sqlite3
from config import DB_NAME, TABLE_NAME

class DBManager:
    def __init__(self):
        self.db_name = DB_NAME

    def conectar(self):
        return sqlite3.connect(self.db_name)

    def inicializar_db(self):
        try:
            with self.conectar() as conn:
                cursor = conn.cursor()
                cursor.execute(f'''
                    CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        nombre TEXT NOT NULL,
                        descripcion TEXT,
                        cantidad INTEGER NOT NULL,
                        precio REAL NOT NULL,
                        categoria TEXT
                    )
                ''')
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
            raise Exception(f"Error BD: {e}")

    def obtener_productos(self):
        with self.conectar() as conn:
            cursor = conn.cursor()
            cursor.execute(f"SELECT * FROM {TABLE_NAME}")
            return cursor.fetchall()

    def buscar_producto_por_id(self, id_prod):
        with self.conectar() as conn:
            cursor = conn.cursor()
            cursor.execute(f"SELECT * FROM {TABLE_NAME} WHERE id = ?", (id_prod,))
            return cursor.fetchone()

    def registrar_producto(self, datos):
        try:
            with self.conectar() as conn:
                cursor = conn.cursor()
                cursor.execute(f"INSERT INTO {TABLE_NAME} (nombre, descripcion, cantidad, precio, categoria) VALUES (?, ?, ?, ?, ?)",
                               (datos['nombre'], datos['desc'], datos['cant'], datos['precio'], datos['cat']))
                conn.commit()
        except sqlite3.Error as e:
            raise Exception(f"Error al registrar: {e}")

    def actualizar_producto(self, id_prod, datos):
        try:
            with self.conectar() as conn:
                cursor = conn.cursor()
                sql = f'''UPDATE {TABLE_NAME} SET 
                          nombre=?, descripcion=?, cantidad=?, precio=?, categoria=? 
                          WHERE id=?'''
                cursor.execute(sql, (datos['nombre'], datos['desc'], datos['cant'], datos['precio'], datos['cat'], id_prod))
                conn.commit()
        except sqlite3.Error as e:
            raise Exception(f"Error al actualizar: {e}")

    def eliminar_producto(self, id_prod):
        try:
            with self.conectar() as conn:
                cursor = conn.cursor()
                cursor.execute(f"DELETE FROM {TABLE_NAME} WHERE id = ?", (id_prod,))
                conn.commit()
        except sqlite3.Error as e:
            raise Exception(f"Error al eliminar: {e}")

    def procesar_venta(self, id_prod, cantidad_vender):
        conn = self.conectar()
        try:
            cursor = conn.cursor()
            
            cursor.execute(f"SELECT precio, cantidad, nombre FROM {TABLE_NAME} WHERE id = ?", (id_prod,))
            producto = cursor.fetchone()
            
            if not producto:
                raise ValueError(f"El producto con ID {id_prod} no existe.")
                
            precio, stock_actual, nombre = producto
            
            if stock_actual < cantidad_vender:
                raise ValueError(f"Stock insuficiente de '{nombre}'. Disponible: {stock_actual}")

            nuevo_stock = stock_actual - cantidad_vender
            cursor.execute(f"UPDATE {TABLE_NAME} SET cantidad = ? WHERE id = ?", (nuevo_stock, id_prod))
            
            total = precio * cantidad_vender
            cursor.execute("INSERT INTO ventas (id_producto, cantidad_vendida, total) VALUES (?, ?, ?)", 
                           (id_prod, cantidad_vender, total))
            
            conn.commit()
            return True
            
        except sqlite3.Error as e:
            conn.rollback()
            raise Exception(f"Error de base de datos: {e}")
        finally:
            conn.close()

    def obtener_historial(self):
        with self.conectar() as conn:
            cursor = conn.cursor()
            sql = '''
                SELECT v.id, p.nombre, v.cantidad_vendida, v.total, v.fecha 
                FROM ventas v
                JOIN productos p ON v.id_producto = p.id
                ORDER BY v.fecha DESC
            '''
            cursor.execute(sql)
            return cursor.fetchall()