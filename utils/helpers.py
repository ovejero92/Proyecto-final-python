import os
from colorama import init, Fore, Style

init(autoreset=True)

def limpiar_pantalla():
    os.system('cls' if os.name == 'nt' else 'clear')

def imprimir_titulo(texto):
    print(f"\n{Fore.CYAN}{Style.BRIGHT}=== {texto.upper()} ==={Style.RESET_ALL}")

def imprimir_error(texto):
    print(f"{Fore.RED}❌ Error: {texto}{Style.RESET_ALL}")

def imprimir_exito(texto):
    print(f"{Fore.GREEN}✅ {texto}{Style.RESET_ALL}")

def validar_input_string(prompt):
    while True:
        dato = input(f"{Fore.YELLOW}{prompt}: {Style.RESET_ALL}").strip()
        if dato:
            return dato
        imprimir_error("El campo no puede estar vacío.")

def validar_input_float(prompt):
    while True:
        try:
            dato = float(input(f"{Fore.YELLOW}{prompt}: {Style.RESET_ALL}"))
            if dato >= 0:
                return dato
            imprimir_error("El número debe ser positivo.")
        except ValueError:
            imprimir_error("Debe ingresar un número válido (ej: 10.50).")

def validar_input_int(prompt):
    while True:
        try:
            dato = int(input(f"{Fore.YELLOW}{prompt}: {Style.RESET_ALL}"))
            if dato >= 0:
                return dato
            imprimir_error("El número debe ser positivo.")
        except ValueError:
            imprimir_error("Debe ingresar un número entero.")