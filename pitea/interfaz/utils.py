
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
import re
from datetime import datetime


archivo_completer = PathCompleter(expanduser=True)

def pedir_qra(mensaje="📡 Indicativo de TU estación (ej. EA2ABC): "):
    """
    Solicita y valida el indicativo de llamada propio.
    """
    regex_indicativo = r"^[A-Z]{1,2}[0-9]{1}[A-Z]{1,4}$"
    while True:
        qra = input(mensaje).strip().upper()
        if re.fullmatch(regex_indicativo, qra):
            return qra
        print(constantes.ROJO + "❌ Indicativo inválido. Debe tener 1-2 letras (prefijo), 1 número y 1-4 letras (sufijo). Ej: EA2ABC" + constantes.RESET)


def pedir_qth(mensaje="🌍 QTH del destinatario: "):
    while True:
        qth = input(mensaje).strip()
        if qth:
            return qth
        print(constantes.ROJO + "❌ QTH no puede estar vacío." + constantes.RESET)

def pedir_fecha(mensaje="📅 Fecha del contacto (YYYY-MM-DD): "):
    while True:
        fecha = input(mensaje).strip()
        try:
            datetime.strptime(fecha, "%Y-%m-%d")
            return fecha
        except ValueError:
            print(constantes.ROJO + "❌ Fecha inválida. Usa el formato YYYY-MM-DD." + constantes.RESET)

def pedir_hora(mensaje="⏰ Hora del contacto (UTC): "):
    while True:
        hora = input(mensaje).strip()
        if re.fullmatch(r"\d{2}:\d{2}", hora):
            h, m = map(int, hora.split(":"))
            if 0 <= h < 24 and 0 <= m < 60:
                return hora
        print(constantes.ROJO + "❌ Hora inválida. Usa el formato HH:MM en 24h." + constantes.RESET)

def pedir_freq(mensaje="📶 Frecuencia (ej. 14.074MHz): "):
    while True:
        freq = input(mensaje).strip()
        if re.fullmatch(r"\d+(\.\d+)?\s*MHz", freq, re.IGNORECASE):
            return freq.upper()
        print(constantes.ROJO + "❌ Frecuencia inválida. Usa el formato '14.074MHz'." + constantes.RESET)

def pedir_modo(mensaje="🎙️ Modo (SSB, CW, FT8, etc.): "):
    while True:
        modo = input(mensaje).strip().upper()
        if modo:
            return modo
        print(constantes.ROJO + "❌ Modo no puede estar vacío." + constantes.RESET)

def pedir_rst(mensaje="📶 RST o SNR reportado (ej. 595): "):
    while True:
        rst = input(mensaje).strip()
        if re.fullmatch(r"\d{2,3}|-\d{1,2}", rst):
            return rst
        print(constantes.ROJO + "❌ RST inválido. Usa 2-3 dígitos o valores negativos como -10." + constantes.RESET)

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
    

