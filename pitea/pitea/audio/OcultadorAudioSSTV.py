from constantes import constantes
import subprocess
from pitea.audio.OcultadorAudio import OcultadorAudio
from PIL import Image
from pathlib import Path
from pitea.mensajes import print
import builtins
import os
from pitea.utils import launch_qsstv


class OcultadorAudioSSTV(OcultadorAudio):
    """
    Ocultador de audio usando SSTV (Slow Scan Television).

    Codifica una imagen en un archivo de audio WAV usando un modo SSTV específico,
    y permite la desocultación mediante QSSTV en un entorno limpio.

    Atributos:
        nombre (str): Identificador del modo, "sstv".
    """

    nombre= "sstv"

    def __init__(self, ruta_audio):
        """
        Inicializa el ocultador SSTV con el archivo de audio contenedor.

        Args:
            ruta_audio (str): Ruta al archivo WAV que servirá de contenedor SSTV.

        Raises:
            ValueError: Si no se puede abrir el archivo de audio.
        """
        super().__init__(ruta_audio)
        
       

    def __guardar(self, ruta, sstv):
        """
        Escribe el buffer SSTV en un archivo WAV.

        Args:
            ruta (str): Archivo de salida para audio SSTV.
            sstv (PySSTV): Instancia de codificador SSTV con método write_wav().
        """
        sstv.write_wav(ruta)  # Usar el método directo de PySSTV
        print(f"La imagen ha sido ocultada en el archivo de audio: {ruta}")

    def __guardar_imagen_redimensionada(self, imagen, ruta,modo):
        """
        Redimensiona y guarda la imagen de entrada según las dimensiones requeridas por el modo SSTV.

        Args:
            imagen (PIL.Image.Image): Imagen original a ocultar.
            ruta (str): Ruta donde se guardará la imagen redimensionada.
            modo (str): Identificador del modo SSTV (p.ej. 'MartinM1').
        """

        imagen.resize(constantes.MODES_SSTV[modo][1], Image.Resampling.LANCZOS).save(ruta)
        print(f"Imagen contenedora redimensionada guardada en {ruta}")

    def _ocultar(self, modo="MartinM1", image=None, samples_per_sec=None, bits=None):
        """
        Configura y devuelve el codificador SSTV para generar audio.

        Args:
            modo (str): Modo de codificación SSTV definido en la configuración.
            image (PIL.Image.Image): Imagen a codificar.
            samples_per_sec (int): Frecuencia de muestreo para WAV.
            bits (int): Profundidad de bits del audio.

        Returns:
            PySSTV: Instancia preparada para escribir audio SSTV.
        """
        sstv = constantes.MODES_SSTV[modo][0](image, samples_per_sec, bits)
        return sstv

    def _desocultar(self):
        """
        Instruye al usuario para usar QSSTV y espera hasta que la imagen SSTV sea exportada.

        Genera indicaciones con rutas absolutas y verifica la presencia de al menos
        un archivo PNG en la carpeta de desocultación.

        Raises:
            Exception: Si no se genera ninguna imagen tras varias ejecuciones.
        """

        RUTA_AUDIO = Path(f"{self._ruta_audio}").resolve()
        RUTA_IMAGEN_DESOCULTACION_absoluta = (Path.cwd() / Path(constantes.RUTA_IMAGEN_DESOCULTACION)).resolve()

        while True:
            if not constantes.STREAMING:
                builtins.print(f"Una vez abierto QSSTV, elija el audio con ruta \033[1;33m{RUTA_AUDIO}\033[0m")
            builtins.print(f"Asegúrese de guardar la imagen como \033[1;33m{str(RUTA_IMAGEN_DESOCULTACION_absoluta) % constantes.FORMATO_IMAGEN_DESOCULTACION}\033[0m")
            launch_qsstv()

            # Verificar si hay al menos un archivo PNG en la ruta
            ruta_padre = Path(constantes.RUTA_IMAGEN_DESOCULTACION).parent
            archivos_png = list(ruta_padre.glob("*.png"))

            if len(archivos_png) >= 1:
                break
            else:
                print(f"\033[91mNo hay ningún archivo 'png' en el directorio especificado: {ruta_padre} \033[0m")

    def ocultar_guardar(self, formato_imagen, ruta_salida):
        """
        Realiza el flujo completo de ocultación SSTV:
        1. Redimensiona la imagen.
        2. Genera audio SSTV.
        3. Guarda en rutas por defecto y personalizada.

        Args:
            formato_imagen (str): Extensión de la imagen a ocultar.
            ruta_salida (str): Ruta para el archivo de audio generado.
        """
        # Cargar configuración de SSTV desde archivo
        modo = constantes.conf['Ajustes_sstv']["modo_sstv"]
        samples_per_sec = constantes.conf['Ajustes_sstv']["samples_per_sec"]
        bits = constantes.conf['Ajustes_sstv']["bits"]

        # Leer y redimensionar la imagen con Pillow
        image = Image.open(str(constantes.RUTA_IMAGEN_CONTENEDORA) % formato_imagen)
        self.__guardar_imagen_redimensionada(image, str(constantes.RUTA_IMAGEN_CONTENEDORA_REDIMENSIONADA) % formato_imagen, modo)

        # Codificar imagen en audio SSTV
        sstv = self._ocultar(modo, image, samples_per_sec, bits)

        # Guardar el archivo de audio
        self.__guardar(str(constantes.RUTA_AUDIO_CONTENEDOR) % constantes.FORMATO_AUDIO_OCULTACION, sstv)
        self.__guardar(ruta_salida, sstv)

    def desocultar_guardar(self):
        """
        Ejecuta el proceso de desocultación SSTV usando QSSTV y bloquea hasta obtener la imagen.
        """
        self._desocultar()
