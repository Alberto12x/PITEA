from interfaz.comandos.command import Command
from constantes import constantes
from interfaz.MenuPrinter import MenuPrinter
import builtins
import subprocess
from utils import (
    pedir_qra, pedir_qth, pedir_fecha, pedir_hora,
    pedir_freq, pedir_modo, pedir_rst_snr
)

class GenerarTarjetaCommand(Command):
    """
    Comando para generar una tarjeta QSL gráfica utilizando un script externo en Bash.

    Recoge los datos necesarios por consola e invoca el script con los argumentos apropiados.
    """

    descripcion = "Generar tarjeta QSL"

    def ejecutar(self):
        menu = MenuPrinter()
        menu.mostrar_opcion(self.descripcion)

        # Recoger datos
        self.qra = pedir_qra()
        self.qth = pedir_qth()
        self.fecha = pedir_fecha()
        self.hora = pedir_hora()
        self.freq = pedir_freq()
        self.modo = pedir_modo()
        self.rst = pedir_rst_snr()

        # Mostrar resumen
        builtins.print("\n📋 Datos a usar:")
        builtins.print(f"  QRA:   {self.qra}")
        builtins.print(f"  QTH:   {self.qth}")
        builtins.print(f"  Fecha: {self.fecha}")
        builtins.print(f"  Hora:  {self.hora} UTC")
        builtins.print(f"  Freq:  {self.freq}")
        builtins.print(f"  Modo:  {self.modo}")
        builtins.print(f"  RST:   {self.rst}")

        confirm = input("\n✅ ¿Confirmar y generar la tarjeta? (s/n): ").strip().lower()
        if confirm != "s":
            builtins.print("⛔ Cancelado por el usuario.")
            input("Presiona Enter para continuar...")
            return
        
        verb = False
        m_verbose = input("🔍 ¿Activar modo verbose? (s/n): ").strip().lower()
        if m_verbose == "s":
            verb = True
            builtins.print("🔍 Modo verbose activado.")

         # Construir el comando
        comando = [
            "python3", constantes.SCRIPT_PATH, "generar-tarjeta",
            "--qra", self.qra,
            "--qth", self.qth,
            "--fecha", self.fecha,
            "--hora", self.hora,
            "--freq", self.freq,
            "--modo", self.modo,
            "--rst", self.rst,
        ]

        if verb:
            comando.extend(["-v"])

        try:
            builtins.print("⏳ Generando tarjeta QSL...")
            subprocess.run(comando, check=True)
            builtins.print("✅ Tarjeta generada correctamente: (FALTA INSERTAR LA RUTA)")
            input("Presiona Enter para continuar...")
        except subprocess.CalledProcessError as e:
            builtins.print(f"\033[1;31m❌ Error al ejecutar el script: {e}\033[0m")
            input("Presiona Enter para continuar...")


#main para pruebas

# if __name__ == "__main__":
#     command = GenerarTarjetaCommand()
#     command.ejecutar()