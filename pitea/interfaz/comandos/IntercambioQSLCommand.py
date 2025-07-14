from interfaz.comandos.command import Command
from constantes import constantes
from interfaz.utils import comprobar_opcion, comprobar_archivo, ejecutar_comando
from interfaz.MenuPrinter import MenuPrinter
from interfaz.comandos.GenerarTarjetaCommand import GenerarTarjetaCommand
from PIL import Image


class IntercambioQSLCommand(Command):
    """
    Comando para iniciar un intercambio QSL desde una imagen ya decodificada
    o mediante Qsstv (modo transmisión).
    """

    descripcion = "Intercambio QSL"

    def ejecutar(self):
        menu = MenuPrinter()
        menu.mostrar_opcion(self.descripcion)

        # Elegir modo
        modo = comprobar_opcion(
            "📡 ¿Cómo quieres hacer el intercambio? (imagen/transmision): ",
            ["imagen", "transmision"]
        )

        # ¿Verbose?
        verbose = comprobar_opcion(
            f"📢 ¿Activar modo verbose? ({'/'.join(constantes.OPCIONES_VERBOSE)}): ",
            constantes.OPCIONES_VERBOSE
        ) == "s"

        # Construir comando base
        comando = ["python3", constantes.SCRIPT_PATH, "intercambio-qsl"]

        if modo == "transmision":
            comando.append("--transmision")
        else:
            ruta_imagen = comprobar_archivo("🖼️ Ruta de la imagen decodificada: ")
            comando.extend(["--input", ruta_imagen])

        if verbose:
            comando.append("--verbose")

        # Ejecutar comando
        ejecutar_comando(comando)

        generar_tarjeta = comprobar_opcion( 
            "🖨️ ¿Generar tarjeta QSL? (s/n): ",
            ["s", "n"]
        ) == "s"
        if generar_tarjeta:
            # Mostramos la tarjeta recibida por pantalla
            if modo == "transmision":
                ruta_tarjeta = constantes._RUTA_QSL_RECIBIDA
            else:
                ruta_tarjeta = constantes._RUTA_QSL_RECIBIDA
            # Abrir y mostrar la imagen
            imagen = Image.open(ruta_tarjeta)
            imagen.show(title="Tarjeta recibida")
            # mostramos los datos extraidos
            ruta_datos = constantes._RUTA_QSL_DATOS_ESTRUCTURADOS
            with open(ruta_datos, "r") as f:
                print(f.read())
            # llamamos al comando de generar tarjeta para que se ejecute
            GenerarTarjetaCommand().ejecutar()
