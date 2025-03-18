from constantes import constantes

#clase para invocar comandos
class Invoker:
    """
    Clase encargada de gestionar y ejecutar los comandos registrados.

    Esta clase actúa como un invocador de comandos, permitiendo registrar comandos
    por nombre, obtener una lista de los comandos registrados y ejecutar un comando
    específico mediante su nombre.

    Métodos:
        obtener_comandos():
            Devuelve el diccionario de comandos registrados.

        registrar_comando(nombre, comando):
            Registra un comando bajo un nombre específico.

        ejecutar_comando(nombre):
            Ejecuta el comando asociado al nombre proporcionado.
    """
    def __init__(self):
        """
        Inicializa el invocador, creando un diccionario vacío para almacenar los comandos.

        Atributos:
            comandos (dict): Diccionario que almacena los comandos registrados, con el nombre como clave.
        """
        self.comandos = {}

    def obtener_comandos(self):
        """
        Devuelve el diccionario de comandos registrados.

        Returns:
            dict: Diccionario con los comandos registrados, donde las claves son los nombres de los comandos.
        """
        return self.comandos
    
    def registrar_comando(self, nombre, comando):
        """
        Registra un comando bajo un nombre específico.

        Args:
            nombre (str): Nombre del comando.
            comando (obj): Objeto del comando que implementa el método `ejecutar`.
        """
        self.comandos[nombre] = comando
    
    def ejecutar_comando(self, nombre):
        """
        Ejecuta el comando asociado al nombre proporcionado.

        Args:
            nombre (str): Nombre del comando a ejecutar.

        Si el nombre del comando no está registrado, se imprime un mensaje de error.
        """
        if nombre in self.comandos:
            self.comandos[nombre].ejecutar()
        else:
            print(constantes.ROJO + "Comando no reconocido." + constantes.RESET)