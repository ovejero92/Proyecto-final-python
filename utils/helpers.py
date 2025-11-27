import os
from colorama import init, Fore, Style

# iniciamos colorama 
init(autoreset=True)

def limpiar_pantalla():
    os.system('cls' if os.name == 'nt' else 'clear')

def imprimir_titulo(texto):
    print(f"\n{Fore.CYAN}{Style.BRIGHT}=== {texto.upper()} === {Style.RESET_ALL}")
    
def imprimir_error(texto):
    print(f"{Fore.RED}❌ Error: {texto}{Style.RESET_ALL}")
    
def imprimir_exito(texto):
    print(f"{Fore.GREEN}✅ {texto}{Style.RESET_ALL}")

def validar_input_string(prompt):
    while True:
        dato = input(f"{Fore.YELLOW}{prompt}: {Style.RESET_ALL}").strip() # ingresa el nombre del producto
        if dato:
            return dato
        imprimir_error("El campo no puede estar vacio")

def validar_input_float(prompt):
    while True:
        try:
           dato = float(input(f"{Fore.YELLOW}{prompt}: {Style.RESET_ALL}"))
           if dato >= 0:
               return dato
           imprimir_error("El numero debe ser positivo")
        except ValueError:
            imprimir_error("el campo no tiene que ser un numero valido.")

def validar_input_int(prompt):
    while True:
        try:
           dato = int(input(f"{Fore.YELLOW}{prompt}: {Style.RESET_ALL}"))
           if dato >= 0:
               return dato
           imprimir_error("El numero debe ser positivo")
        except ValueError:
            imprimir_error("el campo no tiene que ser un numero valido.")
        

