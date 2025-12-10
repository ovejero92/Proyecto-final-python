import tkinter as tk
from tkinter import ttk
from controllers.gestor import InventarioController
from ui.tabs import TabInventario, TabVentas, TabHistorial

class MainApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Inventario (MVC)")
        self.root.geometry("900x600")
        
        self.controller = InventarioController()

        style = ttk.Style()
        style.theme_use('clam')

        notebook = ttk.Notebook(root)
        notebook.pack(fill='both', expand=True)

        self.tab1 = TabInventario(notebook, self.controller)
        self.tab2 = TabVentas(notebook, self.controller)
        self.tab3 = TabHistorial(notebook, self.controller)

        notebook.add(self.tab1, text="Inventario")
        notebook.add(self.tab2, text="Ventas")
        notebook.add(self.tab3, text="Historial")
        
        notebook.bind("<<NotebookTabChanged>>", self.refrescar_tabs)

    def refrescar_tabs(self, event):
        self.tab1.cargar_datos()
        self.tab3.cargar()