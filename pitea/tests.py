#!/usr/bin/env python3
import subprocess 
import os
from PIL import Image
from pitea.imagen.OcultadorImagenLSB import OcultadorImagenLSB
import tempfile

# Ruta del script principal
SCRIPT_PATH = "script_ejecucion.py"
num_test = 1

def ejecutar_comando(command):
    """
    Ejecuta un comando en un subproceso, redirigiendo la salida estándar y de error a archivos temporales.

    El comando se ejecuta y, en caso de éxito, se guarda la salida estándar y de error en archivos temporales.
    Si el comando falla, se imprime un mensaje con los detalles del error y las rutas de los archivos de salida.

    Args:
        command (list): Comando a ejecutar, representado como una lista de strings.

    Returns:
        result (subprocess.CompletedProcess): El resultado de la ejecución del comando.

    Raises:
        subprocess.CalledProcessError: Si el comando ejecutado falla.
    """
    global num_test
    
    temp_dir = tempfile.gettempdir()
    
    numero = f"_{num_test}"

    # Crear las rutas específicas para los archivos temporales
    stdout_temp_path = os.path.join(temp_dir, f"SalidaPitea{numero}.log")
    stderr_temp_path = os.path.join(temp_dir, f"ErroresPitea{numero}.log")
    
    try:
        # Ejecutar el comando y redirigir stdout y stderr a los archivos temporales
        with open(stdout_temp_path, 'w') as stdout_temp, open(stderr_temp_path, 'w') as stderr_temp:
            result = subprocess.run(
                command,
                stdout=stdout_temp,
                stderr=stderr_temp,
                text=True,
                check=True
            )

        # Si el comando se ejecuta correctamente, imprimimos las ubicaciones de los archivos
        print(f"Se ha guardado stdout en: {stdout_temp_path}")
        print(f"Se ha guardado stderr en: {stderr_temp_path}")
    except subprocess.CalledProcessError as e:
        # Si el comando falla, mostramos un mensaje indicando el error
        print("❌ El comando falló. Los detalles del error están en:")
        print(f"   stdout guardado en: {stdout_temp_path}")
        print(f"   stderr guardado en: {stderr_temp_path}")
        print(f"   Error: {e.stderr}")
        raise  
    
    num_test += 1
    return result

def  test_transformada():
    """
    Realiza una prueba para verificar si las transformaciones de una imagen son reversibles.

    - Carga una imagen de prueba.
    - Utiliza un `OcultadorImagenLSB` para transformar la imagen.
    - Verifica que la imagen original y la imagen revertida sean iguales.
    
    Raises:
        AssertionError: Si la comparación entre la imagen original y la revertida no es exitosa.
    """
    ruta_imagen_prueba = "archivos_prueba/imagen_salida_sstv.png"
    imagen_original = Image.open(ruta_imagen_prueba)

    # Crear instancia de OcultadorImagen
    ocultador = OcultadorImagenLSB(ruta_imagen_prueba, modo_cifrador="none")

    # Transformar la imagen
    imagen_transformada = ocultador.transformar_imagen(imagen_original)

    # Invertir la transformación
    imagen_revertida = ocultador.transformar_imagen_inversa(imagen_transformada)

    # Comparar píxeles para verificar reversibilidad completa
    assert list(imagen_original.getdata()) == list(imagen_revertida.getdata()), " Las transformaciones no son reversibles."
    print("✅ Prueba de transformación completamente reversible, completada con éxito \n")

def test_ocultar_desocultar_aes_lsb_lsb():
    """
    Realiza una prueba de ocultar y desocultar datos, cifrados con AES  y usando LSB (Least Significant Bit) en imágenes y audio.

    - Ejecuta el comando para ocultar datos en la imagen y audio.
    - Ejecuta el comando para desocultar los datos.
    - Compara los archivos originales y los desocultos para verificar que son iguales.

    Raises:
        AssertionError: Si los archivos originales y desocultos no coinciden.
    """
    command = [
        "python3", SCRIPT_PATH, "ocultar",
        "--modo-cifrado", "aes",
        "--modo-cifrado-imagen", "lsb",
        "--modo-cifrado-audio", "lsb",
        "--contraseña", "prueba123",
        "-i", "archivos_prueba/prueba.txt",
        "--input_imagen", "archivos_prueba/imagen.png", 
        "--input_audio", "archivos_prueba/audio.wav",  
        "-o", "archivos_prueba/audio_salida.wav",
        "-v"
    ]
    ejecutar_comando(command)

    command = [
        "python3", SCRIPT_PATH, "desocultar",
        "--modo-cifrado", "aes",
        "--modo-cifrado-imagen", "lsb",
        "--modo-cifrado-audio", "lsb",
        "--input_audio", "archivos_prueba/audio_salida.wav",
        "-o", "archivos_prueba/datos_desocultos.txt",
        "--contraseña", "prueba123",
        "-v"
    ]
    ejecutar_comando(command)
    
    with open("archivos_prueba/prueba.txt", "rb") as file1, open("archivos_prueba/datos_desocultos.txt", "rb") as file2:
        assert file1.read() == file2.read(), "Los archivos no son iguales"
    
    print("✅ Prueba de ocultar y desocultar completada con éxito")
    os.remove("archivos_prueba/datos_desocultos.txt")
    os.remove("archivos_prueba/audio_salida.wav")


def test_ocultar_desocultar_none_lsb_lsb():
    """
    Realiza una prueba de ocultar y desocultar datos, cifrados con AES  y usando LSB (Least Significant Bit) en imágenes y audio.

    - Ejecuta el comando para ocultar datos en la imagen y audio.
    - Ejecuta el comando para desocultar los datos.
    - Compara los archivos originales y los desocultos para verificar que son iguales.

    Raises:
        AssertionError: Si los archivos originales y desocultos no coinciden.
    """
    command = [
        "python3", SCRIPT_PATH, "ocultar",
        "--modo-cifrado", "none",
        "--modo-cifrado-imagen", "lsb",
        "--modo-cifrado-audio", "lsb",
        "--contraseña", "prueba123",
        "-i", "archivos_prueba/prueba.txt",
        "--input_imagen", "archivos_prueba/imagen.png", 
        "--input_audio", "archivos_prueba/audio.wav",  
        "-o", "archivos_prueba/audio_salida.wav",
        "-v"
    ]
    ejecutar_comando(command)

    command = [
        "python3", SCRIPT_PATH, "desocultar",
        "--modo-cifrado", "none",
        "--modo-cifrado-imagen", "lsb",
        "--modo-cifrado-audio", "lsb",
        "--input_audio", "archivos_prueba/audio_salida.wav",
        "-o", "archivos_prueba/datos_desocultos.txt",
        "--contraseña", "prueba123",
        "-v"
    ]
    ejecutar_comando(command)
    
    with open("archivos_prueba/prueba.txt", "rb") as file1, open("archivos_prueba/datos_desocultos.txt", "rb") as file2:
        assert file1.read() == file2.read(), "Los archivos no son iguales"
    
    print("✅ Prueba de ocultar y desocultar completada con éxito")
    os.remove("archivos_prueba/datos_desocultos.txt")
    os.remove("archivos_prueba/audio_salida.wav")


#def test_ocultar_desocultar_sstv():
    
# Ejecutar los casos de prueba
def run_tests():
    """
    Ejecuta todos los casos de prueba definidos en el sistema.

    - Llama a las funciones de prueba para verificar que los procesos de ocultación/desocultación y transformación
      funcionen correctamente.
      
    Raises:
        AssertionError: Si alguna de las pruebas falla.
        subprocess.CalledProcessError: Si algún subproceso falla.
    """
    try:
            
        # Ejecutar las pruebas
        print("Ejecutando pruebas... \n")

        print("🧪 Prueba de ocultar y desocultar con cifrado AES y LSB")
        test_ocultar_desocultar_aes_lsb_lsb()
        print("🧪 Prueba de ocultar y desocultar con cifrado None y LSB")
        test_ocultar_desocultar_none_lsb_lsb()
        print("🧪 Prueba transformada de imagenes")
        test_transformada()
        

        print(" \n🎉 Todas las pruebas han pasado correctamente. \n")
    except AssertionError as error:
        print("❌ Error en la prueba:", error)
        exit(1)
    except subprocess.CalledProcessError as error:
        print("❌ Error en subproceso:", error)
        exit(1)

        

if __name__ == "__main__":
    run_tests()
