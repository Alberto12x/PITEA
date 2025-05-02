"""
Módulo principal de flujos de trabajo de Pitea.
Define las funciones `flujo_de_trabajo_ocultar` y `flujo_de_trabajo_desocultar`
que orquestan los procesos de cifrado/desifrado y ocultación/desocultación
utilizando fábricas de cifradores, imagen y audio.
"""
from pitea.mensajes import MENSAJE_INICIO_FLUJO, print
from pitea.cifradores.cifradorfactory import CifradorFactory
from pitea.imagen.imagenfactory import OcultadorImagenFactory
from pitea.audio.audiofactory import OcultadorAudioFactory
from constantes import constantes
from pitea.utils import crear_cache
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
    Ejecuta el flujo de cifrado y ocultación de datos en imagen y audio.

    Args:
        modo_cifrado (str): Método de cifrado para datos ('aes' o 'none').
        modo_cifrado_imagen (str): Modo de ocultación en imagen ('lsb' o 'text').
        modo_cifrado_audio (str): Modo de ocultación en audio ('lsb' o 'sstv').
        input (str): Ruta al archivo de datos a ocultar.
        input_imagen (str): Ruta a la imagen contenedora.
        input_audio (str): Ruta al audio contenedor.
        output (str): Nombre o ruta base del archivo de salida de audio.
        contraseña (str): Contraseña para cifrado (si aplica).

    Notes:
        - Construye carpetas de caché antes de iniciar.
        - Utiliza fábricas (`CifradorFactory`, `OcultadorImagenFactory`,
          `OcultadorAudioFactory`) para instanciar componentes.
        - Muestra mensajes condicionados al modo verbose.
    """

    try :
        print("Creando estructura de la cache")
        crear_cache(constantes.LISTA_DIR_CACHE_OCULTACION)


        print(MENSAJE_INICIO_FLUJO % "ocultación")

        print("Creando cifrador...")
        cifrador = CifradorFactory.creacion(modo_cifrado, contraseña, None)

        print("Cifrador creado , cifrando datos ...")
        cifrador.cifrar_guardar(input)

        print("Creando ocultador en imagenes ...")
        ocultador_imagen = OcultadorImagenFactory.creacion(
            modo_cifrado_imagen, input_imagen, modo_cifrado
        )

        print("Ocultador en imagenes  creado, ocultando datos en imagen ...")
        if modo_cifrado_audio not in ["sstv"] :
            imagen_contenedora, formato = ocultador_imagen.ocultar_guardar()
        else :
            
            modo_sstv = constantes.conf['Ajustes_sstv']["modo_sstv"]
            anchura = constantes.MODES_SSTV[modo_sstv][1][0]
            altura = constantes.MODES_SSTV[modo_sstv][1][1]
            imagen_contenedora, formato = ocultador_imagen.ocultar_guardar(altura,anchura)

        print("Creando ocultador en audio ...")
        ocultador_audio = OcultadorAudioFactory.creacion(
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
    Ejecuta el flujo de desocultación y descifrado de datos desde imagen o audio.

    Args:
        modo_cifrado (str): Método de cifrado usado ('aes' o 'none').
        modo_cifrado_imagen (str): Modo de desocultación en imagen.
        modo_cifrado_audio (str): Modo de desocultación en audio.
        input_audio (str): Ruta al archivo de audio contenedor.
        input_imagen (str): Ruta al archivo de imagen contenedora.
        input_text (str): Ruta al archivo de texto contenedor.
        output (str): Ruta del archivo de salida para datos desocultados.
        contraseña (str): Contraseña para descifrado (si aplica).
        streaming (bool): Si el audio SSTV se captura en streaming.

    Notes:
        - Crea estructura de cache para desocultación.
        - Dependiendo de inputs, elige decodificar audio o usar imagen/texto.
    """

    try :
        print("Creando estructura de la cache")
        crear_cache(constantes.LISTA_DIR_CACHE_DESOCULTACION)

        print(MENSAJE_INICIO_FLUJO % "desocultación")

        #Opcion de pasar el audio sstv o en streaming
        if input_audio or streaming :
            print("Creando ocultador en audio ...")
            ocultador_audio = OcultadorAudioFactory.creacion(modo_cifrado_audio, input_audio)

            print("Ocultador en audio  creado, desocultando imagen en audio ...")
            ocultador_audio.desocultar_guardar()

        
        #Opcion de pasar el sstv ya decodificado como imagen
        print("Creando ocultador en imagenes ...")
        if  input_audio or streaming: 
            ocultador_imagen = OcultadorImagenFactory.creacion(
                modo_cifrado_imagen, str(constantes.RUTA_IMAGEN_DESOCULTACION) % "png",modo_cifrado
            )
        elif input_imagen : #opcion de pasar la imagen decodificada
            ocultador_imagen = OcultadorImagenFactory.creacion(
                modo_cifrado_imagen, input_imagen,modo_cifrado
            )
        elif input_text :
            ocultador_imagen = OcultadorImagenFactory.creacion(
                modo_cifrado_imagen, input_imagen,modo_cifrado,input_text
            )
            
        print("Ocultador en imagenes  creado, desocultando datos en imagen ...")
        ocultador_imagen.desocultar_guardar()


        print("Creando cifrador...")
        cifrador = CifradorFactory.creacion(modo_cifrado, contraseña, output)

        print("Cifrador creado, descifrando datos ...")
        cifrador.descifrar_guardar()

        print("Proceso realizado")
    except Exception as e:  # Captura cualquier tipo de excepción
        print(f"{Fore.RED}Se ha producido una excepción: {str(e)}")
        print(f"{Fore.RED}Pila de llamadas:")
        traceback.print_exc()
        print(f"{Fore.RED}Programa acabado de manera abrupta{Fore.RESET}")
