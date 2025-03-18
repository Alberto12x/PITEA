from abc import ABC, abstractmethod
from constantes import constantes
from pitea.mensajes import print


class Cifrador(ABC):
    """
    Clase base para los cifradores, que define la interfaz común para cifrar y descifrar datos.

    Esta clase es abstracta y debe ser extendida por otras clases que implementen los métodos específicos
    de cifrado y descifrado utilizando diferentes algoritmos.

    Atributos:
        nombre (str): El nombre del tipo de cifrador.
        contraseña (str): Contraseña  para el cifrado.
        ruta (str): Ruta del archivo donde se guardan los datos cifrados o descifrados.
    """

    nombre = ""

    def __init__(self, contraseña, ruta=None):
        """
        Inicializa el cifrador con la contraseña y una ruta opcional.

        Args:
            contraseña (str): Contraseña del cifrado.
            ruta (str, opcional): Ruta del archivo donde se guardan los datos. (default es None)
        """
        self.contraseña = contraseña
        self.df = None
        self.ruta = ruta

    @abstractmethod
    def cifrar(self, secreto, datos):
        """
        Método abstracto para cifrar los datos.

        Este método debe ser implementado por las subclases para cifrar los datos de acuerdo
        con el algoritmo de cifrado que se use.

        Args:
            secreto (str): Contraseña para el cifrado.
            datos (bytes): Datos a cifrar.

        Returns:
            tuple: Un tuple con el IV y los datos cifrados.
        """
        pass

    @abstractmethod
    def descifrar(self, datos):
        """
        Método abstracto para descifrar los datos.

        Este método debe ser implementado por las subclases para descifrar los datos de acuerdo
        con el algoritmo de descifrado que se use.

        Args:
            datos (bytes): Datos cifrados a descifrar.

        Returns:
            bytes: Los datos descifrados.
        """
        pass

    def cifrar_guardar(self, secreto):
        """
        Cifra los datos leídos desde un archivo y guarda el archivo cifrado.

        Este método lee los datos desde el archivo proporcionado, los cifra y guarda el IV y los datos
        cifrados en un archivo específico.

        Args:
            secreto (str): Ruta del archivo que contiene los datos a cifrar.
        """
        with open(secreto, "rb") as f:
            datos = f.read()

        iv, datos_cifrados = self.cifrar(datos)

        with open(constantes.RUTA_DATOS_CIFRADO, "wb") as f:
            f.write(iv + datos_cifrados)  # Escribir el IV al inicio del archivo

        print(f"Archivo cifrado guardado en {constantes.RUTA_DATOS_CIFRADO}")

    def descifrar_guardar(self):
        """
        Descifra los datos desde un archivo y guarda el archivo descifrado.

        Este método lee los datos cifrados desde un archivo, los descifra y guarda los datos
        descifrados tanto en el archivo de salida predeterminado como en la ruta proporcionada en el
        constructor.

        Raises:
            ValueError: Si los datos no se pueden descifrar correctamente.
        """
        with open(constantes.RUTA_DATOS_CIFRADOS_DESOCULTACION, "rb") as f:
            datos = f.read()

        datos_descifrados = self.descifrar(datos)

        # Guardar los datos descifrados en el archivo de salida
        with open(constantes.RUTA_DATOS_LIMPIOS_DESOCULTACION, "wb") as f:
            f.write(datos_descifrados)

        print(f"Archivo descifrado guardado en {constantes.RUTA_DATOS_LIMPIOS_DESOCULTACION}")

        # Guardar los datos descifrados en el archivo de salida
        with open(self.ruta, "wb") as f:
            f.write(datos_descifrados)

        print(f"Archivo descifrado guardado en {self.ruta}")
