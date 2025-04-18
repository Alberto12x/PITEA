from pitea.cifradores.Cifrador import Cifrador


class CifradorNone(Cifrador):
    """
    Clase que implementa un cifrador sin cifrado real.

    Esta clase es útil para cuando no se desea realizar ningún tipo de cifrado o descifrado,
    pero se mantiene la interfaz para que el proceso sea compatible con otros sistemas que esperan
    un cifrador.

    Atributos:
        nombre (str): El nombre del cifrador, en este caso "none".
    """

    nombre = "none"

    def __init__(self, contraseña, ruta=None):
        """
        Inicializa el cifrador con la contraseña y una ruta opcional.

        Args:
            contraseña (str): Contraseña del cifrado.
            ruta (str, opcional): Ruta del archivo donde se guardan los datos. (default es None)
        """
        super().__init__(contraseña,ruta)

    def _cifrar(self, datos):
        """
        Método que "cifra" los datos, pero no realiza ninguna operación de cifrado real.

        En lugar de cifrar los datos, simplemente devuelve los datos sin cambios.

        Args:
            datos (bytes): Los datos a cifrar.

        Returns:
            tuple: Un tuple vacío seguido de los datos sin cambios.
        """
        return b"", datos

    def _descifrar(self, datos):
        """
        Método que "descifra" los datos, pero no realiza ninguna operación de descifrado real.

        En lugar de descifrar los datos, simplemente devuelve los datos sin cambios.

        Args:
            datos (bytes): Los datos a descifrar.

        Returns:
            bytes: Los datos sin cambios.
        """
        return datos
