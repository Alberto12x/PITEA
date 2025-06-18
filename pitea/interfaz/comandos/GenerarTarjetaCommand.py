from interfaz.comandos.command import Command
from constantes import constantes
from interfaz.utils import comprobar_opcion
from interfaz.MenuPrinter import MenuPrinter
from pathlib import Path
import builtins
import subprocess
import os

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
        qra = input("📡 Indicativo del destinatario (ej. EA2EEB): ").strip().upper()
        qth = input("🌍 QTH del destinatario: ").strip()
        fecha = input("📅 Fecha del contacto (YYYY-MM-DD): ").strip()
        hora = input("⏰ Hora del contacto (UTC): ").strip()
        freq = input("📶 Frecuencia (ej. 14.074MHz): ").strip()
        modo = input("🎙️ Modo (SSB, CW, FT8, etc.): ").strip()
        rst = input("📶 RST o SNR reportado (ej. 595): ").strip()

         # Ruta absoluta al script bash
        script_path = Path(__file__).parent / "qso_fill2.sh"

        if not script_path.exists():
            builtins.print(f"\033[1;31m❌ Error: El script no se encuentra en {script_path}\033[0m")
            return
        if not os.access(script_path, os.X_OK):
            builtins.print(f"\033[1;31m❌ El script no tiene permisos de ejecución. Use:\nchmod +x {script_path}\033[0m")
            return

        # Mostrar resumen
        builtins.print("\n📋 Datos a usar:")
        builtins.print(f"  QRA:   {qra}")
        builtins.print(f"  QTH:   {qth}")
        builtins.print(f"  Fecha: {fecha}")
        builtins.print(f"  Hora:  {hora} UTC")
        builtins.print(f"  Freq:  {freq}")
        builtins.print(f"  Modo:  {modo}")
        builtins.print(f"  RST:   {rst}")

        confirm = input("\n✅ ¿Confirmar y generar la tarjeta? (s/n): ").strip().lower()
        if confirm != "s":
            builtins.print("⛔ Cancelado por el usuario.")
            return

        # Ejecutar script
        comando = [
            "bash",
            str(script_path),
            qra,
            qth,
            fecha,
            hora,
            freq,
            modo,
            rst
        ]

        try:
            builtins.print("\n⏳ Generando tarjeta QSL...")
            subprocess.run(comando, check=True)
            builtins.print(f"\n✅ Tarjeta generada correctamente: {qra}.jpg y {qra}_2.jpg\n")
        except subprocess.CalledProcessError as e:
            builtins.print(f"\033[1;31m❌ Error al ejecutar el script: {e}\033[0m")


#main para pruebas

if __name__ == "__main__":
    command = GenerarTarjetaCommand()
    command.ejecutar()