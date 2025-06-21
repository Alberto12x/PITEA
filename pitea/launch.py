#!/usr/bin/env python3
from interfaz.Invoker import Invoker
from interfaz.comandos.OcultarArchivoCommand import OcultarArchivoCommand
from interfaz.comandos.DesocultarArchivoCommand import DesocultarArchivoCommand
from interfaz.MenuPrinter import MenuPrinter
from constantes import constantes
from interfaz.comandos.GenerarTarjetaCommand import GenerarTarjetaCommand

class Launch :
    """
    Punto de entrada de la interfaz de línea de comandos de Pitea.

    Métodos:
        menu():
            Muestra el menú principal, registra comandos y ejecuta la selección del usuario.
    """
    def menu():
        """
        Gestiona el flujo de interacción con el usuario:

        1. Instancia `MenuPrinter` para mostrar el menú.
        2. Instancia `Invoker` para registrar y ejecutar comandos.
        3. Registra `OcultarArchivoCommand` y `DesocultarArchivoCommand`.
        4. Entra en un bucle mostrando el menú:
           - Opción de ocultar o desocultar: ejecuta el comando.
           - Opción de salir: muestra mensaje y termina.
           - Opción inválida: imprime error.
        5. Tras cada ejecución, actualiza el cache de constantes.
        """
        menu_printer = MenuPrinter() #Creamos el printer
        inv = Invoker()              #Creamos el invoker

        # Registro de comandos
        comandos = [OcultarArchivoCommand(), DesocultarArchivoCommand(), GenerarTarjetaCommand()]
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
    Launch.menu()
