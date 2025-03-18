# TFG-PITEA

## Arbol de directorio provisional de pitea

```TFG-PITEA/
├── README.md
├── pitea/
│   ├── README.md
│   ├── pitea/
│   │   ├── audio/
│   │   │   ├── desocultador.py
│   │   │   ├── ocultador.py
│   │   │   └── procesamiento.py
│   │   ├── cache/
│   │   │   ├── audio/
│   │   │   │   ├── contenedroes/
│   │   │   │   └── limpio/
│   │   │   ├── imagenes/
│   │   │   │   ├── contenedores/
│   │   │   │   └── limpio/
│   │   ├── imagen/
│   │   │   ├── desocultador.py
│   │   │   ├── ocultador.py
│   │   │   └── procesamiento.py
│   │   ├── constantes.py
│   └── script_ejecucion.py
└── pyproject.toml
```

## Instalacion 


ES NECESARIO INSTALAR tessercar-ocr, qsstv y la fuente a utilizar.

En qsstv hay que ponerlo en modo "sound form file2 y activar el auto slant.



## Documentacion del .toml


``` python
# Archivo de configuracion utilizado para guardar ciertos valores entre ejecuciones del programa
# o parámetros de configuración más concretos que hemos decidido que no se pasen por parámetro
# debido a que no responden al fin de la herramienta, sino a parámetros específicos de esta.

[persistente]
# Contador utilizado para distinguir la cache entre varias ejecuciones en un mismo minuto
contador_cache = 0

# Fecha de la última ejecución, usada para saber si es necesario utilizar el contador de cache
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

## EJEMPLO DE LLAMADA

## LSB

```bash
python3 script_ejecucion.py ocultar \
  --modo-cifrado aes \
  --modo-cifrado-imagen lsb \
  --modo-cifrado-audio lsb \
  -i archivos_prueba/prueba.txt \
  --input_imagen archivos_prueba/imagen.png \
  --input_audio  archivos_prueba/audio.wav \
  -o ./archivos_prueba/audio_salida.wav \
  --contraseña qwqwqw \
  -v
```

```bash
  python3 script_ejecucion.py desocultar \
  --modo-cifrado aes \
  --modo-cifrado-imagen lsb \
  --modo-cifrado-audio lsb \
  --input_audio ./archivos_prueba/audio_salida.wav \
  -o ./archivos_prueba/datos_desocultos.txt \
  --contraseña qwqwqw \
  -v
```

## SSTV

```bash
python3 script_ejecucion.py ocultar \
  --modo-cifrado aes \
  --modo-cifrado-imagen text \
  --modo-cifrado-audio sstv \
  -i archivos_prueba/prueba.txt \
  -o ./archivos_prueba/sstv.wav \
  --contraseña qwqwqw \
  -v
```

### Desocultacion desde imagen

```bash
  python3 script_ejecucion.py desocultar \
  --modo-cifrado aes \
  --modo-cifrado-imagen text \
  --modo-cifrado-audio sstv \
  --input_imagen ./archivos_prueba/imagen_salida_sstv.png\
  -o ./archivos_prueba/datos_desocultos_text_sstv.txt \
  --contraseña qwqwqw \
  -v
```

### Desocultacion desde audio

```bash
  python3 script_ejecucion.py desocultar \
  --modo-cifrado aes \
  --modo-cifrado-imagen text \
  --modo-cifrado-audio sstv \
  --input_audio ./archivos_prueba/sstv.wav\
  -o ./archivos_prueba/datos_desocultos_text_sstv.txt \
  --contraseña qwqwqw \
  -v
```

### Desocultacion desde audio streaming

```bash
  python3 script_ejecucion.py desocultar \
  --modo-cifrado aes \
  --modo-cifrado-imagen text \
  --modo-cifrado-audio sstv \
  -o ./archivos_prueba/datos_desocultos_text_sstv.txt \
  --contraseña qwqwqw \
  -v \
  -s
```

### Desocultacion desde base64

```bash
  python3 script_ejecucion.py desocultar \
  --modo-cifrado aes \
  --modo-cifrado-imagen none \
  --modo-cifrado-audio none \
  --input_text ./archivos_prueba/base64.txt\
  -o ./archivos_prueba/datos_desocultos_text_sstv.txt \
  --contraseña qwqwqw \
  -v
```

