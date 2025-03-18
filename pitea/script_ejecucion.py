#!/usr/bin/env python3
import click
from constantes import constantes
from pitea.main import flujo_de_trabajo_ocultar, flujo_de_trabajo_desocultar
from pitea.mensajes import SEPARADOR
from pitea.utils import comprobar_existencia_archivo


@click.group(context_settings=dict(help_option_names=["-h", "--help"]))
def main():
    """Herramienta para la ocultacion y desocultacion de datos en imagen y audio."""
    pass


@main.command()
@click.option(
    "--modo-cifrado",
    type=click.Choice(
        constantes.OPCIONES_CIFRADO
    ),  
    default="aes",
    help="Modo de cifrado a utilizar.",
)
@click.option(
    "--modo-cifrado-imagen",
    type=click.Choice(
        constantes.OPCIONES_OCULTACION_IMAGEN
    ), 
    default="lsb",
    help="Modo de ocultacion a usar en la imagen.",
)
@click.option(
    "--modo-cifrado-audio",
    type=click.Choice(
        constantes.OPCIONES_OCULTACION_AUDIO
    ),  
    default="lsb",
    help="Modo de ocultacion específico para audio.",
)
@click.option(
    "-v",
    "--verbose",
    is_flag=True,
    help="Modo verbose , muestra mensajes del flujo.",
)
@click.option(
    "-i",
    "--input",
    required=True,
    type=click.Path(exists=True),
    help="Archivo de datos a ocultar",
)
@click.option(
    "--input_imagen",
    type=click.Path(exists=True),
    help="Archivo de imagen requerido para ciertos modo de ocultacion de imagen.",
)
@click.option(
    "--input_audio",
    type=click.Path(exists=True),
    help="Archivo de audio requerido para ciertos modo de ocultacion de audio.",
)
@click.option(
    "-o",
    "--output",
    default="audio_salida",
    type=click.Path(),
    help="Nombre del archivo de salida.", 
)
@click.option(
    "--contraseña", 
    help="Contraseña para cifrado o descifrado."
)
def ocultar(
    modo_cifrado,
    modo_cifrado_imagen,
    modo_cifrado_audio,
    input,
    input_imagen,
    input_audio,
    output,
    contraseña,
    verbose,
):
    """
    Ejecuta la acción de ocultación.
    """

    # activo el modo verbose o no
    if verbose:
        constantes.VERBOSE = True

   
    comprobar_existencia_archivo(input)

    if input_imagen is None and modo_cifrado_imagen  in ["lsb"] :
        raise click.BadParameter(f"En el modo {modo_cifrado_imagen} es necesario añadir la opcion --input_imagen ARCHIVO ")
    elif input_imagen is not None:
        comprobar_existencia_archivo(input_imagen)

    if input_audio is None and modo_cifrado_audio  in ["lsb"]:
        raise click.BadParameter(f"En el modo {modo_cifrado_audio} es necesario añadir la opcion --input_audio ARCHIVO ")
    elif input_audio is not None :
        comprobar_existencia_archivo(input_audio)


    # Mostramos parámetros para depuración
    if constantes.VERBOSE:
        click.echo(f"Modo de cifrado: {modo_cifrado}")
        click.echo(f"Modo de cifrado de imagen: {modo_cifrado_imagen}")
        click.echo(f"Modo de cifrado de audio: {modo_cifrado_audio}")

        click.echo(f"Archivo de entrada de texto: {input}")
        if input_imagen:
            click.echo(f"Archivo de entrada de imagen: {input_imagen}")
        if input_audio:
            click.echo(f"Archivo de entrada de audio: {input_audio}")

        click.echo(f"Archivo de salida de audio: {output}")

        print(SEPARADOR)

    flujo_de_trabajo_ocultar(
        modo_cifrado,
        modo_cifrado_imagen,
        modo_cifrado_audio,
        input,
        input_imagen,
        input_audio,
        output,
        contraseña,
    )


@main.command()
@click.option(
    "--modo-cifrado",
    type=click.Choice(
        constantes.OPCIONES_CIFRADO
    ),  
    default="aes",
    help="Modo de cifrado a utilizar."
)
@click.option(
    "--modo-cifrado-imagen",
    type=click.Choice(
        constantes.OPCIONES_DESOCULTACION_IMAGEN
    ),  
    default="lsb",
    help="Modo de ocultacion usado en la imagen.",
)
@click.option(
    "--modo-cifrado-audio",
    type=click.Choice(
        constantes.OPCIONES_DESCOCULTACION_AUDIO
    ),  
    default="lsb",
    help="Modo de ocultacion usado en el audio.",
)
@click.option(
    "-v",
    "--verbose",
    is_flag=True,
    help="Modo verbose , muestra mensajes del flujo.",
)
@click.option(
    "-s",
    "--streaming",
    is_flag=True,
    help="Modo streaming, captura el audio sstv en streaming en vez de pasarle un audio.",
)
@click.option(
    "--input_audio",
    type=click.Path(exists=True),
    help="Archivo de audio de entrada.",
)
@click.option(
    "--input_imagen",
    type=click.Path(exists=True),
    help="Archivo de imagen de entrada.",
)
@click.option(
    "-i",
    "--input_text",
    type=click.Path(exists=True),
    help="Archivo de texto de entrada.",
)
@click.option(
    "-o",
    "--output",
    default="datos_desocultos.txt",
    type=click.Path(),
    help="Archivo de texto de salida.",
)
@click.option("--contraseña", help="Contraseña para descifrado.")
def desocultar(
    modo_cifrado,
    modo_cifrado_imagen,
    modo_cifrado_audio,
    input_audio,
    input_imagen,
    input_text,
    output,
    contraseña,
    verbose,
    streaming
):
    """
    Ejecuta la acción de desocultación.
    """

    # activo el modo verbose o no
    if verbose:
        constantes.VERBOSE = True
        # activo el modo streaming o no
    if streaming:
        constantes.STREAMING = True

    #Se puede pasar o el de audio o el de imagen, los dos no y uno obligatorio a no ser que estemos e streaming
    if not input_audio  and not input_imagen and not input_text and not constantes.STREAMING:
        click.BadOptionUsage("No se ha introducido nigún input")
    elif input_audio and input_imagen :
        click.BadOptionUsage("Solo se puede introducir input_imagen si no introduce input_audio")
    elif input_text and input_imagen :
        click.BadOptionUsage("Solo se puede introducir input_text si no introduce input_imagen")
    elif input_text and input_audio :
        click.BadOptionUsage("Solo se puede introducir input_text si no introduce input_audio")

    # Mostramos parámetros para depuración
    if constantes.VERBOSE:
        click.echo(f"Modo de cifrado: {modo_cifrado}")
        click.echo(f"Modo de cifrado de imagen: {modo_cifrado_imagen}")
        click.echo(f"Modo de cifrado de audio: {modo_cifrado_audio}")
        click.echo(f"Streaming: {'Si' if constantes.STREAMING else 'No'}")

        if input_audio :
            click.echo(f"Archivo de entrada de audio: {input_audio}")
        if input_imagen:
            click.echo(f"Archivo de entrada de imagen: {input_imagen}")

        click.echo(f"Archivo de salida: {output}")

        print(SEPARADOR)

    flujo_de_trabajo_desocultar(
            modo_cifrado,
            modo_cifrado_imagen,
            modo_cifrado_audio,
            input_audio,
            input_imagen,
            input_text,
            output,
            contraseña,
            streaming
        )


if __name__ == "__main__":
    main()
