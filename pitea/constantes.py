from pathlib import Path
from pitea.utils import cargar_configuracion
from datetime import datetime
from pitea.utils import actualizar_conf
from pysstv.color import MartinM1, Robot36, ScottieS1


class Constantes:
    def __init__(self):
        self._RUTA_PROGRAMA = Path("pitea")
        self._ARCHIVO_CONFIG = self._RUTA_PROGRAMA / "configuracion.toml"
        self._RUTA_CACHE_GENERAL = self._RUTA_PROGRAMA.parent / "cache"
        self._RUTA_CACHE_GENERAL = self._RUTA_CACHE_GENERAL.resolve()

        self.actualizar_cache()

        self._VERBOSE = False
        self._STREAMING = False

        self._FORMATO_IMAGEN_DESOCULTACION = "png"
        self._FORMATO_IMAGEN_OCULTACION = "png"
        self._FORMATO_AUDIO_OCULTACION = "wav"
        
        self._MODES_SSTV = {
            "MartinM1": (MartinM1, (320, 256)),
            "Robot36": (Robot36, (320, 240)),
            "ScottieS1": (ScottieS1, (320, 256)),
        }
        
        self._SCRIPT_PATH = "script_ejecucion.py"
        self._RESET = "\033[0m"
        self._CYAN = "\033[1;36m"
        self._YELLOW = "\033[1;33m"
        self._ROJO = "\033[1;31m"
        self._VERDE = "\033[1;32m"
        self._MORADO = "\033[1;35m"
        
        self._TITULO = """
░▒▓███████▓▒░  ░▒▓█▓▒░ ░▒▓████████▓▒░ ░▒▓████████▓▒░  ░▒▓██████▓▒░  
░▒▓█▓▒░░▒▓█▓▒░ ░▒▓█▓▒░    ░▒▓█▓▒░     ░▒▓█▓▒░        ░▒▓█▓▒░░▒▓█▓▒░ 
░▒▓█▓▒░░▒▓█▓▒░ ░▒▓█▓▒░    ░▒▓█▓▒░     ░▒▓█▓▒░        ░▒▓█▓▒░░▒▓█▓▒░ 
░▒▓███████▓▒░  ░▒▓█▓▒░    ░▒▓█▓▒░     ░▒▓██████▓▒░   ░▒▓████████▓▒░ 
░▒▓█▓▒░        ░▒▓█▓▒░    ░▒▓█▓▒░     ░▒▓█▓▒░        ░▒▓█▓▒░░▒▓█▓▒░ 
░▒▓█▓▒░        ░▒▓█▓▒░    ░▒▓█▓▒░     ░▒▓█▓▒░        ░▒▓█▓▒░░▒▓█▓▒░ 
░▒▓█▓▒░        ░▒▓█▓▒░    ░▒▓█▓▒░     ░▒▓████████▓▒░ ░▒▓█▓▒░░▒▓█▓▒░ 
        """
        
        self._OPCIONES_CIFRADO=["aes", "none"]
        self._OPCIONES_OCULTACION_IMAGEN=["lsb", "text"]
        self._OPCIONES_DESOCULTACION_IMAGEN= self._OPCIONES_OCULTACION_IMAGEN + ["none"]
        self._OPCIONES_OCULTACION_AUDIO=["lsb", "sstv"]
        self._OPCIONES_DESCOCULTACION_AUDIO= self._OPCIONES_OCULTACION_AUDIO + ["none"]
        self._OPCIONES_VERBOSE = ["s", "n"]

    def __getattr__(self, name):
        # Check if the attribute exists
        if f"_{name}" in self.__dict__:
            return self.__dict__[f"_{name}"]
        else:
            raise AttributeError(f"{name} no encontrado")


    def actualizar_cache(self):
        conf = cargar_configuracion(self._ARCHIVO_CONFIG)
        fecha_hora_actual = datetime.now()
        formato = fecha_hora_actual.strftime("%d-%m-%Y_%H:%M")
        
        if formato != conf['persistente']["ult_fecha"]:
            self._RUTA_CACHE_ESPECIFICA = self._RUTA_CACHE_GENERAL / f"cache_{formato}"
            conf['persistente']["ult_fecha"] = formato
            conf['persistente']["contador_cache"] = 0
        else:
            self._RUTA_CACHE_ESPECIFICA = (
                self._RUTA_CACHE_GENERAL / f"cache_{formato}_{conf['persistente']['contador_cache']}"
            )
            conf['persistente']["contador_cache"] += 1
        
        actualizar_conf(conf, self._ARCHIVO_CONFIG)
        
        self._RUTA_OCULTACION = self._RUTA_CACHE_ESPECIFICA / "ocultacion"
        self._RUTA_OCULTACION_DATOS = self._RUTA_OCULTACION / "datos"
        self._RUTA_OCULTACION_IMAGEN = self._RUTA_OCULTACION / "imagen"
        self._RUTA_OCULTACION_AUDIO = self._RUTA_OCULTACION / "audio"

        self._RUTA_DATOS_CIFRADO = self._RUTA_OCULTACION_DATOS / "datos_originales_cifrados.txt"
        self._RUTA_DATOS_OCULTADOR_IMAGEN_TEXT = self._RUTA_OCULTACION_DATOS / "datos_ocultador_imagen_text.txt"
        self._RUTA_IMAGEN_CONTENEDORA = self._RUTA_OCULTACION_IMAGEN / "imagen_contenedora.%s"
        self._RUTA_IMAGEN_CONTENEDORA_SIN_TRANSFORMAR= self._RUTA_OCULTACION_IMAGEN / "imagen_contenedora_sin_transformar.%s"

        self._RUTA_IMAGEN_CONTENEDORA_REDIMENSIONADA = self._RUTA_OCULTACION_IMAGEN / "imagen_contenedora_redimensionada.%s"
        self._RUTA_AUDIO_CONTENEDOR = self._RUTA_OCULTACION_AUDIO / "audio_contenedor.%s"
        
        self._RUTA_DESOCULTACION = self._RUTA_CACHE_ESPECIFICA / "desocultacion"
        self._RUTA_DESOCULTACION_DATOS = self._RUTA_DESOCULTACION / "datos"
        self._RUTA_DESOCULTACION_IMAGEN = self._RUTA_DESOCULTACION / "imagen"
        

        self._RUTA_DATOS_CIFRADOS_DESOCULTACION = (
            self._RUTA_DESOCULTACION_DATOS / "datos_desocultos_originales_cifrados.txt"
        )
        self._RUTA_DATOS_LIMPIOS_DESOCULTACION = (
            self._RUTA_DESOCULTACION_DATOS / "datos_desocultos_originales_limpios.txt"
        )
        self._RUTA_IMAGEN_DESOCULTACION = (
            self._RUTA_DESOCULTACION_IMAGEN / "imagen_contenedora_desocultacion.%s"
        )
        self._RUTA_IMAGEN_CONTENEDORA_DESOCULTACION_DESTRANSFORMADA = (
            self._RUTA_DESOCULTACION_IMAGEN / "imagen_contenedora_desocultacion_destransformada.%s"
        )


        self._LISTA_DIR_CACHE_OCULTACION = [
            self._RUTA_OCULTACION_DATOS,
            self._RUTA_OCULTACION_IMAGEN,
            self._RUTA_OCULTACION_AUDIO,
        ]

        self._LISTA_DIR_CACHE_DESOCULTACION = [self._RUTA_DESOCULTACION_DATOS, self._RUTA_DESOCULTACION_IMAGEN]

constantes = Constantes()
