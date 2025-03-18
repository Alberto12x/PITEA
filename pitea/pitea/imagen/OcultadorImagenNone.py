import base64

from pitea.imagen.OcultadorImagen import OcultadorImagen

from constantes import constantes

class OcultadorImagenNone(OcultadorImagen):
    """
    Implementación de un ocultador de imagen que no realiza ninguna ocultación de datos en la imagen,
    sino que solo permite la desocultación de datos almacenados en un archivo de texto.

    Este ocultador se utiliza para la desocultación de datos que han sido previamente guardados en un
    archivo de texto (en formato base64 si está cifrado).

    Atributos:
        nombre (str): El nombre del tipo de ocultador, en este caso 'none'.
    
    Métodos:
        ocultar(self, datos, altura_imagen=None, anchura_imagen=None):
            Lanza una excepción indicando que el ocultador 'none' no puede realizar ocultación.
        
        desocultar(self):
            Extrae y descompone los datos del archivo de texto, devolviendo los datos desocultados.
        
        desocultar_guardar(self):
            Extrae los datos y los guarda en un archivo para su posterior uso.
    """
    nombre = "none"
    
    def ocultar(self, datos, altura_imagen=None, anchura_imagen=None):
        """
        Lanza una excepción indicando que el ocultador 'none' no puede realizar ocultación.

        Este método no es válido en el modo 'none', ya que no se realiza ninguna ocultación de datos.

        Args:
            datos (bytes): Los datos que se intentarían ocultar (no se usan en este método).
            altura_imagen (int, optional): Altura de la imagen (si se requiere). Por defecto es None.
            anchura_imagen (int, optional): Anchura de la imagen (si se requiere). Por defecto es None.

        Raises:
            Exception: Siempre lanza una excepción, indicando que el modo 'none' no es válido para ocultación.
        """
        raise Exception("El modo Ocultador de imagen None no es valido para ocultacion, solo para desocultacion")

    def desocultar(self):
        """
        Extrae y descompone los datos de un archivo de texto.

        Si los datos están cifrados (indicado por el atributo `cifrado`), los datos se decodifican de base64.
        Si no están cifrados, se devuelven tal como están.

        Returns:
            str or bytes: Los datos extraídos del archivo, ya sean decodificados o no.
        
        Raises:
            FileNotFoundError: Si el archivo de texto no se encuentra en la ruta indicada.
        """
        with open(self.ruta_txt, 'rb') as f:
            datos = f.read()
        
        if self.cifrado:
            return base64.b64decode(datos)
        else:
            return datos

    def desocultar_guardar(self):
        """
        Extrae los datos utilizando el método `desocultar()` y los guarda en un archivo.

        Los datos extraídos se escriben en un archivo para su posterior uso.

        Returns:
            None
        """
        datos_extraidos = self.desocultar()

        with open(constantes.RUTA_DATOS_CIFRADOS_DESOCULTACION, "wb") as f:
            f.write(datos_extraidos)

        print(f"Datos cifrados guardados en {constantes.RUTA_DATOS_CIFRADOS_DESOCULTACION}")
