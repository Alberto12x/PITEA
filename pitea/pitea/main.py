from pitea.mensajes import MENSAJE_INICIO_FLUJO, print
from pitea.cifradores.cifradorfactory import CifradorFactory
from pitea.imagen.imagenfactory import OcultadorImagenFactory
from pitea.audio.audiofactory import OcultadorAudioFactory
from constantes import constantes
from pitea.utils import cargar_configuracion, crear_cache
from colorama import init, Fore
import traceback

# Inicializar colorama (para compatibilidad con Windows)
init()

def flujo_de_trabajo_ocultar(
    modo_cifrado,
    modo_cifrado_imagen,
    modo_cifrado_audio,
    input,
    input_imagen,
    input_audio,
    output,
    contraseña,
):

    """
    Ejecuta el flujo de trabajo para cifrar y/o posteriormente ocultar datos en imágenes y audio.

    Args:
        modo_cifrado (str): Método de cifrado utilizado para los datos.
        modo_cifrado_imagen (str): Método de ocultación utilizado para imágenes.
        modo_cifrado_audio (str): Método de ocultación utilizado para audio.
        input (str): Ruta del archivo de datos a ocultar.
        input_imagen (str): Ruta del archivo de imagen contenedora.
        input_audio (str): Ruta del archivo de audio contenedor.
        output (str): Nombre del archivo de salida.
        contraseña (str): Contraseña utilizada para el cifrado.

    Notes:
        - Crea la estructura de caché necesaria antes de iniciar el proceso.
    """

    try :
        print("Creando estructura de la cache")
        crear_cache(constantes.LISTA_DIR_CACHE_OCULTACION)


        print(MENSAJE_INICIO_FLUJO % "ocultación")

        print("Creando cifrador...")
        cifrador = CifradorFactory.get_builder(modo_cifrado, contraseña, None)

        print("Cifrador creado , cifrando datos ...")
        cifrador.cifrar_guardar(input)

        print("Creando ocultador en imagenes ...")
        ocultador_imagen = OcultadorImagenFactory.get_builder(
            modo_cifrado_imagen, input_imagen, modo_cifrado
        )

        print("Ocultador en imagenes  creado, ocultando datos en imagen ...")
        if modo_cifrado_audio not in ["sstv"] :
            imagen_contenedora, formato = ocultador_imagen.ocultar_guardar()
        else :
            conf = cargar_configuracion(constantes.ARCHIVO_CONFIG)
            modo_sstv = conf['Ajustes_sstv']["modo_sstv"]
            anchura = constantes.MODES_SSTV[modo_sstv][1][0]
            altura = constantes.MODES_SSTV[modo_sstv][1][1]
            imagen_contenedora, formato = ocultador_imagen.ocultar_guardar(altura,anchura)

        print("Creando ocultador en audio ...")
        ocultador_audio = OcultadorAudioFactory.get_builder(
            modo_cifrado_audio, input_audio
        )

        print("Ocultador en audio  creado, ocultando imagen en audio ...")
        ocultador_audio.ocultar_guardar(formato, output)

        print("Proceso realizado")
    except Exception as e:  # Captura cualquier tipo de excepción
        print(f"{Fore.RED}Se ha producido una excepción: {str(e)}")
        print(f"{Fore.RED}Pila de llamadas:")
        traceback.print_exc()
        print(f"{Fore.RED}Programa acabado de manera abrupta{Fore.RESET}")



def flujo_de_trabajo_desocultar(
    modo_cifrado, modo_cifrado_imagen, modo_cifrado_audio, input_audio,input_imagen,input_text, output, contraseña,streaming
):
    """
    Ejecuta el flujo de trabajo para desocultar y descifrar datos desde imágenes y/o audio.

    Args:
        modo_cifrado (str): Método de cifrado utilizado para los datos ocultos.
        modo_cifrado_imagen (str): Método de desocultación utilizado para imágenes.
        modo_cifrado_audio (str): Método de desocultación utilizado para audio.
        input_audio (str or None): Ruta del archivo de audio contenedor (opcional).
        input_imagen (str or None): Ruta del archivo de imagen contenedora (opcional).
        input_text (str or None): Ruta del archivo de texto contenedor (opcional).
        output (str): Nombre del archivo de salida.
        contraseña (str): Contraseña utilizada para el descifrado
        streaming (bool): Flag que dice si se ha activado el modo stremaing en sstv

    Notes:
        - Crea la estructura de caché necesaria antes de iniciar el proceso.
    """

    try :
        print("Creando estructura de la cache")
        crear_cache(constantes.LISTA_DIR_CACHE_DESOCULTACION)

        print(MENSAJE_INICIO_FLUJO % "desocultación")

        #Opcion de pasar el audio sstv o en streaming
        if input_audio or streaming :
            print("Creando ocultador en audio ...")
            ocultador_audio = OcultadorAudioFactory.get_builder(modo_cifrado_audio, input_audio)

            print("Ocultador en audio  creado, desocultando imagen en audio ...")
            ocultador_audio.desocultar_guardar()

        
        #Opcion de pasar el sstv ya decodificado como imagen
        print("Creando ocultador en imagenes ...")
        if  input_audio : 
            ocultador_imagen = OcultadorImagenFactory.get_builder(
                modo_cifrado_imagen, str(constantes.RUTA_IMAGEN_DESOCULTACION) % "png",modo_cifrado
            )
        elif input_imagen : #opcion de pasar la imagen decodificada
            ocultador_imagen = OcultadorImagenFactory.get_builder(
                modo_cifrado_imagen, input_imagen,modo_cifrado
            )
        elif input_text :
            ocultador_imagen = OcultadorImagenFactory.get_builder(
                modo_cifrado_imagen, input_imagen,modo_cifrado,input_text
            )
            
        print("Ocultador en imagenes  creado, desocultando datos en imagen ...")
        ocultador_imagen.desocultar_guardar()


        print("Creando cifrador...")
        cifrador = CifradorFactory.get_builder(modo_cifrado, contraseña, output)

        print("Cifrador creado, descifrando datos ...")
        cifrador.descifrar_guardar()

        print("Proceso realizado")
    except Exception as e:  # Captura cualquier tipo de excepción
        print(f"{Fore.RED}Se ha producido una excepción: {str(e)}")
        print(f"{Fore.RED}Pila de llamadas:")
        traceback.print_exc()
        print(f"{Fore.RED}Programa acabado de manera abrupta{Fore.RESET}")
