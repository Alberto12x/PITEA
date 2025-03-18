from abc import ABC, abstractmethod
import wave
from constantes import constantes
from pitea.mensajes import print


class OcultadorAudio(ABC):
    """
    Clase base abstracta para ocultación de datos en archivos de audio.

    Métodos abstractos:
        ocultar(self, datos): Implementación específica para ocultar datos en audio.
        desocultar(self): Implementación específica para extraer datos ocultos de audio.

    Métodos auxiliares:
        guardar(self, ruta, frames): Guarda un archivo de audio con los frames modificados.
        ocultar_guardar(self, formato_imagen, ruta_salida): Oculta datos y los guarda en un archivo de audio.
        desocultar_guardar(self): Extrae datos ocultos y los guarda como imagen.
    """

    nombre = ""

    def __init__(self, ruta_audio):
        """
        Inicializa el objeto con un archivo de audio.

        Args:
            ruta_audio (str): Ruta del archivo de audio en el que se ocultarán/extrarán datos.
        """
        self.audio = None
        self.formato = None
        self.ruta_audio = ruta_audio

        if ruta_audio:
            try:
                self.audio = wave.open(ruta_audio, mode="rb")
                self.formato = ruta_audio.split(".")[-1]
            except wave.Error as e:
                raise ValueError(f"Error al abrir el archivo de audio: {e}")

    def guardar(self, ruta, frames):
        """
        Guarda los frames modificados en un archivo de audio.

        Args:
            ruta (str): Ruta donde se guardará el archivo de audio.
            frames (bytes): Datos de audio modificados.

        Raises:
            ValueError: Si el archivo de audio original no se ha cargado correctamente.
        """
        if not self.audio:
            raise ValueError("El archivo de audio original no está cargado.")

        with wave.open(ruta, "wb") as audio_modificado:
            audio_modificado.setparams(self.audio.getparams())  # Copiar los parámetros del original
            audio_modificado.writeframes(frames)  # Escribir los frames modificados

        print(f"Archivo de audio guardado en: {ruta}")

    @abstractmethod
    def ocultar(self, datos):
        """Oculta datos en el audio y devuelve los frames modificados."""
        pass

    @abstractmethod
    def desocultar(self):
        """Extrae datos ocultos del audio y los devuelve como bytes."""
        pass

    def ocultar_guardar(self, formato_imagen, ruta_salida=None):
        """
        Oculta una imagen en el archivo de audio y guarda el resultado.

        Args:
            formato_imagen (str): Formato de la imagen a ocultar.
            ruta_salida (str, optional): Ruta personalizada para guardar el audio modificado.
        """
        with open(str(constantes.RUTA_IMAGEN_CONTENEDORA) % formato_imagen, "rb") as img_file:
            datos_imagen = img_file.read()

        frames = self.ocultar(datos_imagen)

        # Guardar en la ruta por defecto
        self.guardar(str(constantes.RUTA_AUDIO_CONTENEDOR) % constantes.FORMATO_AUDIO_OCULTACION, frames)

        # Guardar en la ruta personalizada si se especifica
        if ruta_salida:
            self.guardar(ruta_salida, frames)

    def desocultar_guardar(self):
        """
        Extrae la imagen oculta del archivo de audio y la guarda en un archivo.
        """
        datos_extraidos = self.desocultar()

        ruta_salida = str(constantes.RUTA_IMAGEN_DESOCULTACION) % constantes.FORMATO_IMAGEN_DESOCULTACION
        with open(ruta_salida, "wb") as archivo_img:
            archivo_img.write(datos_extraidos)

        print(f"Imagen extraída y guardada en: {ruta_salida}")
