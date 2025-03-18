from constantes import constantes
import builtins


MENSAJE_INICIO_FLUJO = "Iniciando flujo de %s ..."
SEPARADOR = "---------------------------------------------------------------------" # Utilizado para separar los mensajes del parseo de arugmentos con los de la aplicacion en la terminal


def print(str):
    """
    Imprime un mensaje en la salida estándar si el modo verbose está activado.

    Args:
        str (str): Mensaje a imprimir.

    Notes:
        - Utiliza la función `print` de `builtins` para evitar conflictos con redefiniciones.
        - Utilizado para implementar el modo verbose y poder escribir mensajes dependiendo de una constante

    """
    
    if constantes.VERBOSE:
        builtins.print(str)
