
"""
Módulo utils: Funciones auxiliares para interacción con el usuario y ejecución de comandos.
Incluye validación de rutas, selección de opciones y ejecución de flujo mediante Click.
"""
import os
from constantes import constantes
from prompt_toolkit import prompt
from prompt_toolkit.completion import PathCompleter
import sys
sys.path.append("../../")  
from script_ejecucion import main
from click.testing import CliRunner




archivo_completer = PathCompleter(expanduser=True)

def comprobar_directorio(mensaje):
    """
    Solicita una ruta de directorio al usuario y verifica que exista.

    Esta función mantiene un ciclo de entrada hasta que el usuario ingrese una ruta válida de directorio
    que exista en el sistema.

    Args:
        mensaje (str): Mensaje que se muestra al usuario para pedir la ruta.

    Returns:
        str: La ruta del archivo ingresada por el usuario.

    Raises:
        ValueError: Si el directorio donde se guardara el archivo ha ingresar no existe.
    """
    while True:
        salida = prompt(mensaje, completer=archivo_completer).strip()
        salida = os.path.expanduser(salida)  # Expande '~' a '/home/usuario/'
        directorio = os.path.dirname(salida)  # Extraer solo el directorio de la ruta

        if directorio == "" or os.path.exists(directorio):  
            return salida
        print(constantes.ROJO + "❌ Error: La carpeta de salida no existe. Introduce una ruta válida." + constantes.RESET)


def comprobar_opcion(mensaje, opciones):
    """
    Solicita una opción al usuario y verifica que esté en las opciones válidas.

    Esta función mantiene un ciclo de entrada hasta que el usuario ingrese una opcion valida.

    Args:
        mensaje (str): Mensaje que se muestra al usuario para pedir la opción.
        opciones (list): Lista de opciones válidas.

    Returns:
        str: Opción seleccionada por el usuario.
    
    Raises:
        ValueError: Si la opción ingresada no es válida.
    """
    while True:
        opcion = input(constantes.YELLOW + mensaje + constantes.RESET).strip().lower()
        if opcion in opciones:
            return opcion
        print(constantes.ROJO + "❌ Error: Opción inválida." + constantes.RESET)


def comprobar_archivo(mensaje):
    """
    Solicita una ruta de archivo al usuario y verifica que exista.

    Esta función mantiene un ciclo de entrada hasta que el usuario ingrese una ruta válida de archivo
    que exista en el sistema.

    Args:
        mensaje (str): Mensaje que se muestra al usuario para pedir la ruta del archivo.

    Returns:
        str: La ruta del archivo ingresada por el usuario.

    Raises:
        ValueError: Si el archivo ingresado no existe.
    """
    while True:
        archivo = prompt( mensaje , completer=archivo_completer).strip()
        if os.path.exists(archivo):
            return archivo
        print(constantes.ROJO + "❌ Error: El archivo no existe. Introduce una ruta válida." + constantes.RESET)


def ejecutar_comando(comando):
    """
    Ejecuta un comando en el sistema y muestra el resultado.

    Esta función ejecuta el comando proporcionado, muestra un spinner mientras el comando se ejecuta y,
    al finalizar, imprime el resultado en la consola. Si ocurre un error, se maneja la excepción y
    se muestra el error al usuario.

    Args:
        comando (list): Lista que representa el comando a ejecutar.

    Returns:
        None

    Raises:
        subprocess.CalledProcessError: Si ocurre un error durante la ejecución del comando.
    """

    comando = comando[2:]

    try:
        runner = CliRunner()
        result = runner.invoke(main, comando)
        print(result.output)

        if result.exception:
            raise result.exception 

        print(constantes.VERDE + f"\r🟢 Proceso de {comando[0]} finalizado.\n" + constantes.RESET)
        print(constantes.MORADO + "Podrá encontrar el archivo en la ruta especificada.\n" + constantes.RESET)
        input(constantes.MORADO + "Presione enter para continuar..." + constantes.RESET)

    except Exception as error:
        print(constantes.ROJO + "\r❌ Error en la ejecución:\n" + constantes.RESET, error)
        input(constantes.MORADO + "Presione enter para continuar..." + constantes.RESET)
        raise error  
    

