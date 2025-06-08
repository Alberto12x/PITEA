# Manual de uso

En este documento se explicará brevemente cómo usar las distintas
funcionalidades de la herramienta, aportando imágenes de la terminal o
de la herramienta para facilitar su entendimiento.

## Ejemplos de Ejecución

El archivo "script_ejecucion.py" y "launch.py" es ejecutable de la
manera estándar de Linux, $./archivo$ o con $python3$.\
El mensaje de ayuda generado por la herramienta al ejecutar
"script_ejecucion.py" con la opción -h o --help es:

``` bash
Usage: script_ejecucion.py [OPTIONS] COMMAND [ARGS]...

  Herramienta para la ocultacion y desocultacion de datos en imagen y
  audio.

Options:
  -h, --help  Show this message and exit.

Commands:
  desocultar  Ejecuta la acción de desocultación.
  ocultar     Ejecuta la acción de ocultación.
```

y ejecutando cada subcomando con la misma opción:

``` bash
> ./script_ejecucion.py ocultar -h
Usage: script_ejecucion.py ocultar [OPTIONS]

  Ejecuta la acción de ocultación.

Options:
  --modo-cifrado [aes|none]       Modo de cifrado a utilizar.
  --modo-cifrado-imagen [lsb|text]
                                  Modo de ocultacion a usar en la imagen.
  --modo-cifrado-audio [lsb|sstv]
                                  Modo de ocultacion específico para audio.
  -v, --verbose                   Modo verbose , muestra mensajes del
                                  flujo.
  -i, --input PATH                Archivo de datos a ocultar  [required]
  --input_imagen PATH             Archivo de imagen requerido para ciertos
                                  modo de ocultacion de imagen.
  --input_audio PATH              Archivo de audio requerido para ciertos
                                  modo de ocultacion de audio.
  -o, --output PATH               Nombre del archivo de salida.
  --contraseña TEXT               Contraseña para cifrado o descifrado.
  -h, --help                      Show this message and exit.
```

``` bash
> ./script_ejecucion.py desocultar -h
Usage: script_ejecucion.py desocultar [OPTIONS]

  Ejecuta la acción de desocultación.

Options:
  --modo-cifrado [aes|none]       Modo de cifrado a utilizar.
  --modo-cifrado-imagen [lsb|text|none]
                                  Modo de ocultacion usado en la imagen.
  --modo-cifrado-audio [lsb|sstv|none]
                                  Modo de ocultacion usado en el audio.
  -v, --verbose                   Modo verbose , muestra mensajes del
                                  flujo.
  -s, --streaming                 Modo streaming, captura el audio sstv en
                                  streaming en vez de pasarle un audio.
  --input_audio PATH              Archivo de audio de entrada.
  --input_imagen PATH             Archivo de imagen de entrada.
  -i, --input_text PATH           Archivo de texto de entrada.
  -o, --output PATH               Archivo de texto de salida.
  --contraseña TEXT               Contraseña para descifrado.
  -h, --help                      Show this message and exit.
```

Para ejecutar la CLI $python3\ launch.py$, este comando es lo que se
ejecuta tras haber ejecutado el "install.sh" y ejecutar $pitea$ como se
muestra en el documento [Guía de instalación](./docs/INSTALL.md).

### Uso de algoritmos de ocultación basados en LSB

#### Llamada por terminal

``` bash
python3 script_ejecucion.py ocultar \
  --modo-cifrado aes \
  --modo-cifrado-imagen lsb \
  --modo-cifrado-audio lsb \
  -i archivos_prueba/prueba.txt \
  --input_imagen archivos_prueba/imagen.png \
  --input_audio archivos_prueba/audio.wav \
  -o ./archivos_prueba/audio_salida.wav \
  --contraseña qwqwqw \
  -v
```

``` bash
python3 script_ejecucion.py desocultar \
  --modo-cifrado aes \
  --modo-cifrado-imagen lsb \
  --modo-cifrado-audio lsb \
  --input_audio ./archivos_prueba/audio_salida.wav \
  -o ./archivos_prueba/datos_desocultos.txt \
  --contraseña qwqwqw \
  -v
```

#### Llamada en la CLI

![Ejemplo de uso de la CLI para ocultación con LSB. Captura de pantalla
de la herramienta.](Imagenes/C/o_lsb.png){#fig:proceso2 width="60%"}

![Ejemplo de uso de la CLI para desocultación con LSB. Captura de
pantalla de la herramienta.](Imagenes/C/d_lsb.png){#fig:proceso2
width="60%"}

### SSTV

``` bash
python3 script_ejecucion.py ocultar \
  --modo-cifrado aes \
  --modo-cifrado-imagen text \
  --modo-cifrado-audio sstv \
  -i archivos_prueba/prueba.txt \
  -o ./archivos_prueba/sstv.wav \
  --contraseña qwqwqw \
  -v
```

![Ejemplo de uso de la CLI para ocultación con SSTV. Captura de pantalla
de la herramienta.](Imagenes/C/o_sstv.png){#fig:proceso2 width="50%"}

Para la desocultación de esta subsección es necesario configurar QSSTV.
Es marcar la casilla del *autoslant*.

![Marcar *autoslant*. Captura de pantalla de
QSSTV.](Imagenes/C/autoslant.png){#fig:proceso2 width="60%"}

#### Desocultación desde imagen

``` bash
python3 script_ejecucion.py desocultar \
  --modo-cifrado aes \
  --modo-cifrado-imagen text \
  --modo-cifrado-audio none \
  --input_imagen ./archivos_prueba/imagen_salida_sstv.png \
  -o ./archivos_prueba/datos_desocultos_text_sstv.txt \
  --contraseña qwqwqw \
  -v
```

![Ejemplo de uso de la CLI para desocultación con SSTV usando una imagen
ya decodificada de SSTV. Captura de pantalla de la
herramienta.](Imagenes/C/d_i_sstv.png){#fig:proceso2 width="50%"}

#### Desocultación desde audio

Es necesario configurar QSSTV para que reciba el audio desde un archivo.

![Configuración QSSTV para lectura desde archivos. Capturas de pantalla
de QSSTV.](Imagenes/C/conf_file.png){#fig:proceso2 width="100%"}

``` bash
python3 script_ejecucion.py desocultar \
  --modo-cifrado aes \
  --modo-cifrado-imagen text \
  --modo-cifrado-audio sstv \
  --input_audio ./archivos_prueba/sstv.wav \
  -o ./archivos_prueba/datos_desocultos_text_sstv.txt \
  --contraseña qwqwqw \
  -v
```

![Ejemplo de uso de la CLI para desocultación con SSTV. Captura de
pantalla de la herramienta.](Imagenes/C/d_sstv.png){#fig:proceso2
width="50%"}

#### Desocultación desde audio streaming

Es necesario configurar QSSTV para que reciba el audio desde la tarjeta
de sonido del dispositivo.

![Configuración QSSTV para lectura desde la tarjeta de sonido. Capturas
de pantalla de QSSTV.](Imagenes/C/conf_sound.png){#fig:proceso2
width="100%"}

``` bash
python3 script_ejecucion.py desocultar \
  --modo-cifrado aes \
  --modo-cifrado-imagen text \
  --modo-cifrado-audio sstv \
  -o ./archivos_prueba/datos_desocultos_text_sstv.txt \
  --contraseña qwqwqw \
  -v \
  -s
```

![Ejemplo de uso de la CLI para desocultación con SSTV en modo
*streaming*. Captura de pantalla de la
herramienta.](Imagenes/C/d_s_sstv.png){#fig:proceso2 width="50%"}

#### Desocultación desde Base64

``` bash
python3 script_ejecucion.py desocultar \
  --modo-cifrado aes \
  --modo-cifrado-imagen none \
  --modo-cifrado-audio none \
  --input_text ./archivos_prueba/base64.txt \
  -o ./archivos_prueba/datos_desocultos_text_sstv.txt \
  --contraseña qwqwqw \
  -v
```

![Ejemplo de uso de la CLI para desocultación con SSTV iniciando con un
archivo que contiene información en base64. Captura de pantalla de la
herramienta.](Imagenes/C/d_64_sstv.png){#fig:proceso2 width="50%"}

## Documentación del archivo de configuración, "configuracion.toml"

``` {.toml fontsize="\\small" frame="lines" breaklines=""}
[persistente]
# Contador utilizado para distinguir la caché entre varias ejecuciones en un mismo minuto
contador_cache = 0

# Fecha de la última ejecución, usada para saber si es necesario utilizar el contador de caché
ult_fecha = "20-02-2025_21:22"

[Ajustes_sstv]
# Modo de transmisión SSTV seleccionado, especifica el tipo de imagen que se usará
modo_sstv = "MartinM1"

# Muestras por segundo, define la calidad de la transmisión en términos de frecuencia
samples_per_sec = 48000

# Número de bits por muestra, determina la resolución de las muestras de audio
bits = 16

[Ajustes_ocultador_imagen_text]
# Tamaño de la fuente en píxeles, utilizado para ajustar el texto sobre las imágenes
tamanio_fuente = 10

# Ancho máximo de las imágenes, para asegurarse de que las imágenes no sean demasiado anchas
anchura_maxima = 800

# Ruta relativa a la fuente utilizada para el texto (debe estar en el directorio adecuado)
ruta_fuente = "../fuentes/ocraregular.ttf"

# Configuración para usar la GPU, puede ser un valor booleano (True o False)
gpu = "True"
```

### Descripción de las secciones {#descripción-de-las-secciones .unnumbered}

- `persistente`: Guarda parámetros que se mantienen entre ejecuciones,
    como la caché y la fecha de la última ejecución.

- `Ajustes_sstv`: Define la configuración de transmisión SSTV,
    incluyendo modo, muestras por segundo y resolución.

- `Ajustes_ocultador_imagen_text`: Contiene opciones para superponer
    texto en imágenes, como tamaño de fuente, ancho máximo, fuente y uso
    de GPU.
