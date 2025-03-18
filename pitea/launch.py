#!/usr/bin/env python3
from interfaz.Invoker import Invoker
from interfaz.comandos.OcultarArchivoCommand import OcultarArchivoCommand
from interfaz.comandos.DesocultarArchivoCommand import DesocultarArchivoCommand
from interfaz.MenuPrinter import MenuPrinter
from constantes import constantes


def menu():
    """
    Función principal que maneja la interacción con el usuario a través del menú.

    - Crea el objeto `MenuPrinter` para mostrar el menú y la interfaz.
    - Crea el objeto `Invoker` para gestionar los comandos.
    - Registra los comandos en el `Invoker`.
    - Muestra el menú y ejecuta los comandos seleccionados por el usuario.
    - Si el usuario selecciona una opción inválida o sale, el ciclo termina.
    """
    menu_printer = MenuPrinter() #Creamos el printer
    inv = Invoker()              #Creamos el invoker

    # Registro de comandos
    comandos = [OcultarArchivoCommand(), DesocultarArchivoCommand()]
    for idx, comando in enumerate(comandos, start=1):
        inv.registrar_comando(str(idx), comando)

  
    while True:
        menu_printer.mostrar_titulo()                            #mostramos el nombre de la aplicacion
        opcion = menu_printer.mostrar_menu(inv.obtener_comandos())   #mostramos el menu de opciones
        if opcion == str(idx+1) :                                    
            menu_printer.mostrar_salida()
            break
        elif opcion < str(idx+1) and opcion > "0":
            inv.ejecutar_comando(opcion)                              #ejecutamos el comando seleccionado
        else:
            print("Opción inválida.")     
        constantes.actualizar_cache()                   
        

if __name__ == "__main__":
    menu()
