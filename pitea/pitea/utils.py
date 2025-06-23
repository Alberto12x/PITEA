"""
Módulo de configuración y utilidades de caché de Pitea.
Proporciona funciones para crear directorios de caché, cargar y actualizar
configuración en formato TOML, y validar la existencia de archivos.
"""
import tomllib
import click
import tomli_w
from pathlib import Path
import os
import subprocess


def crear_cache(lista):
    """
    Crea los directorios de caché especificados en la lista.

    Args:
        lista (list of pathlib.Path): Lista de objetos Path que representan
        directorios que deben existir.

    Notes:
        - Si un directorio ya existe, no se genera error.
        - Se crean todos los directorios padres si no existen.
    """

    for dir in lista:
        dir.mkdir(exist_ok=True, parents=True)


def cargar_configuracion(archivo_conf):
    """
    Carga la configuración desde un archivo TOML.

    Args:
        archivo_conf (str or Path): Ruta al archivo TOML de configuración.

    Returns:
        dict: Contenido del archivo TOML como diccionario.
        None: Si ocurre un error en la lectura.

    """

    try:
        with open(archivo_conf, "rb") as f:
            conf = tomllib.load(f)
    except FileNotFoundError:
        print("El archivo no fue encontrado.")
        return None
    except PermissionError:
        print("No tienes permisos para acceder a este archivo.")
        return None
    except Exception as e:
        print(f"Ocurrió un error inesperado: {e}")
        return None

    return conf


def actualizar_conf(conf, archivo_conf):
    """
    Actualiza el archivo de configuración con los valores de 'conf'.

    Args:
        conf (dict): Diccionario que contiene la configuración en formato TOML.
        archivo_conf (str): Ruta del archivo de configuración a actualizar.

    Returns:
        None

    """

    with open(archivo_conf, "wb") as f:
        tomli_w.dump(conf, f)


def comprobar_existencia_archivo(nombre):
    """
    Verifica la existencia y validez de un archivo.

    Args:
        nombre (str): Ruta del archivo a comprobar.

    Raises:
        click.UsageError: Si el archivo no existe o no es un archivo válido.
    """
    ruta = Path(nombre)
    if not ruta.exists():
        raise click.UsageError(f"El archivo '{nombre}' no existe.")
    if not ruta.is_file():
        raise click.UsageError(f"'{nombre}' no es un archivo válido.")


def launch_qsstv(self):
        """
        Lanza QSSTV en un entorno con variables de entorno limpias para evitar errores de Qt.

        Elimina temporalmente variables como `QT_QPA_PLATFORM_PLUGIN_PATH` y similares,
        cambia al directorio home, invoca `qsstv`, y restaura el cwd.
        """

        # Crear entorno limpio
        env_clean = os.environ.copy()
        for var in ["QT_QPA_PLATFORM_PLUGIN_PATH", "QT_QPA_PLATFORM", "LD_LIBRARY_PATH", "OPENCV_UI_BACKEND"]:
            env_clean.pop(var, None)

        # Guardar el cwd actual
        original_cwd = os.getcwd()
        try:
            # Cambiar a un directorio seguro
            os.chdir(os.path.expanduser("~"))
            subprocess.run(["qsstv"], env=env_clean)
        finally:
            # Restaurar el cwd original (opcional pero recomendable)
            os.chdir(original_cwd)