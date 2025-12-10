import tkinter as tk
from tkinter import ttk, messagebox

class TabInventario(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.setup_ui()
    
    def setup_ui(self):
        panel = ttk.Frame(self)
        panel.pack(fill='x', padx=10, pady=10)
        
        ttk.Button(panel, text="Refrescar", command=self.cargar_datos).pack(side='left', padx=5)
        ttk.Button(panel, text="Nuevo", command=self.modal_producto).pack(side='left', padx=5)
        ttk.Button(panel, text="Editar", command=self.editar_seleccionado).pack(side='left', padx=5)
        ttk.Button(panel, text="Eliminar", command=self.eliminar_seleccionado).pack(side='left', padx=5)

        cols = ("id", "nombre", "categoria", "precio", "cantidad")
        self.tree = ttk.Treeview(self, columns=cols, show='headings')
        for col in cols:
            self.tree.heading(col, text=col.capitalize())
            self.tree.column(col, width=100)
            
        self.tree.pack(fill='both', expand=True, padx=10, pady=10)
        self.cargar_datos()

    def cargar_datos(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        productos = self.controller.obtener_todos()
        for p in productos:
            # p = (id, nombre, desc, cant, precio, cat)
            self.tree.insert("", "end", values=(p[0], p[1], p[5], f"${p[4]}", p[3]))

    def eliminar_seleccionado(self):
        sel = self.tree.selection()
        if not sel: return
        id_prod = self.tree.item(sel[0])['values'][0]
        if messagebox.askyesno("Confirmar", "¿Borrar producto?"):
            self.controller.eliminar(id_prod)
            self.cargar_datos()

    def modal_producto(self, datos=None):
        top = tk.Toplevel(self)
        top.title("Producto")
        
        entries = {}
        labels = ["Nombre", "Descripción", "Cantidad", "Precio", "Categoría"]
        keys = ["nombre", "desc", "cant", "precio", "cat"]
        defaults = [datos[1], datos[2], datos[3], datos[4], datos[5]] if datos else ["","","",0,0,""]

        for i, lbl in enumerate(labels):
            tk.Label(top, text=lbl).grid(row=i, column=0, padx=5, pady=5)
            entry = tk.Entry(top)
            entry.insert(0, str(defaults[i]))
            entry.grid(row=i, column=1, padx=5, pady=5)
            entries[keys[i]] = entry

        def guardar():
            try:
                id_p = datos[0] if datos else None
                self.controller.guardar_producto(
                    entries['nombre'].get(), entries['desc'].get(),
                    entries['cant'].get(), entries['precio'].get(),
                    entries['cat'].get(), id_p
                )
                top.destroy()
                self.cargar_datos()
                messagebox.showinfo("Éxito", "Guardado correctamente")
            except ValueError as e:
                messagebox.showerror("Error", str(e))

        tk.Button(top, text="Guardar", command=guardar).grid(row=5, columnspan=2, pady=10)

    def editar_seleccionado(self):
        sel = self.tree.selection()
        if not sel: return
        id_prod = self.tree.item(sel[0])['values'][0]
        prod_completo = self.controller.db.buscar_producto_por_id(id_prod)
        self.modal_producto(prod_completo)

class TabVentas(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        
        frame = ttk.Frame(self)
        frame.place(relx=0.5, rely=0.3, anchor='center')
        
        ttk.Label(frame, text="ID Producto:").pack()
        self.ent_id = ttk.Entry(frame)
        self.ent_id.pack(pady=5)
        
        ttk.Label(frame, text="Cantidad:").pack()
        self.ent_cant = ttk.Entry(frame)
        self.ent_cant.pack(pady=5)
        
        ttk.Button(frame, text="VENDER", command=self.vender).pack(pady=20)

    def vender(self):
        try:
            self.controller.realizar_venta(self.ent_id.get(), self.ent_cant.get())
            messagebox.showinfo("Venta", "Venta realizada con éxito")
            self.ent_id.delete(0, 'end')
            self.ent_cant.delete(0, 'end')
        except ValueError as e:
            # AQUÍ ES DONDE SE SOLUCIONA TU PROBLEMA VISUAL
            messagebox.showerror("Error de Venta", str(e))
        except Exception as e:
            messagebox.showerror("Error Crítico", str(e))

class TabHistorial(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        
        ttk.Button(self, text="Actualizar", command=self.cargar).pack()
        
        self.tree = ttk.Treeview(self, columns=("id","prod","cant","total","fecha"), show='headings')
        for c in ["id","prod","cant","total","fecha"]:
            self.tree.heading(c, text=c)
        self.tree.pack(fill='both', expand=True)
        self.cargar()

    def cargar(self):
        for r in self.tree.get_children(): self.tree.delete(r)
        for v in self.controller.ver_historial():
            self.tree.insert("", "end", values=v)