import base64
import numpy as np
from pitea.imagen.OcultadorImagen import OcultadorImagen
from PIL import Image, ImageDraw, ImageFont
from constantes import constantes
from pitea.utils import cargar_configuracion
import easyocr
import pytesseract
from pitea.mensajes import print


class OcultadorImagenText(OcultadorImagen):
    """
    Clase que implementa la ocultación y desocultación de datos en una imagen utilizando texto.
    
    Esta clase se utiliza para ocultar datos en una imagen como texto visible y luego recuperar los datos
    mediante el uso de OCR (Reconocimiento Óptico de Caracteres).

    Atributos:
        nombre (str): El nombre del tipo de ocultador, en este caso 'text'.

    Métodos:
        ocultar(self, datos, altura_imagen=None, anchura_imagen=None):
            Oculta los datos en una imagen como texto.

        desocultar(self):
            Recupera los datos de una imagen utilizando OCR.
    """
    nombre = "text"
    
    def ocultar(self, datos, altura_imagen=None, anchura_imagen=None):
        """
        Oculta los datos en una imagen en formato de texto.

        Si los datos están cifrados, se codifican en base64 antes de ser escritos. Si no están cifrados,
        se escriben tal cual. El texto se ajusta al tamaño de la imagen, dividiendo las líneas si es necesario.

        Args:
            datos (bytes): Los datos a ocultar en la imagen.
            altura_imagen (int, optional): La altura de la imagen en píxeles. Si es None, se calcula automáticamente.
            anchura_imagen (int, optional): La anchura de la imagen en píxeles. Si es None, se usa un valor por defecto.

        Returns:
            imagen (PIL.Image): La imagen con los datos ocultos como texto.
            str: El formato de la imagen.

        Raises:
            Exception: Si no es posible ajustar los datos en la imagen debido a la falta de espacio.
        """
        # Codificamos los datos en base64 si están cifrados
        if self.cifrado:
            datos = base64.b64encode(datos).decode('utf-8')
        else:
            datos = datos.decode('utf-8')

        # Guardamos los datos en un archivo de texto
        with open(constantes.RUTA_DATOS_OCULTADOR_IMAGEN_TEXT, 'w') as f:
            f.write(datos)

        print(f"Datos escritos en {constantes.RUTA_DATOS_OCULTADOR_IMAGEN_TEXT}")
        
        # Cargamos la configuración
        conf = cargar_configuracion(constantes.ARCHIVO_CONFIG)
        tamaño_fuente = conf['Ajustes_ocultador_imagen_text']["tamanio_fuente"]
        anchura_maxima = conf['Ajustes_ocultador_imagen_text']["anchura_maxima"]
        ruta_fuente = conf['Ajustes_ocultador_imagen_text']["ruta_fuente"]
        fuente = ImageFont.truetype(ruta_fuente, tamaño_fuente)
        
        # Definir la anchura máxima de las líneas
        if anchura_imagen is None:
            anchura_imagen = anchura_maxima
        else:
            anchura_maxima = anchura_imagen

        ancho_maximo_linea = anchura_imagen - 20  # Margen lateral de 10 píxeles a cada lado

        # Lista que contendrá las líneas de texto
        lineas_ajustadas = []

        if datos:
            # Comprobar si la palabra es demasiado larga para caber en una línea
            ancho_datos = fuente.getlength(datos)
            if ancho_datos > ancho_maximo_linea:
                # Dividir los datos en fragmentos que quepan en una línea
                fragmento = ""
                for caracter in datos:
                    fragmento_prueba = fragmento + caracter
                    ancho_fragmento = fuente.getlength(fragmento_prueba)
                    if ancho_fragmento > ancho_maximo_linea:
                        lineas_ajustadas.append(fragmento)
                        fragmento = caracter
                    else:
                        fragmento = fragmento_prueba
                if fragmento:
                    lineas_ajustadas.append(fragmento)
            else:
                lineas_ajustadas.append(datos)

        # Calcular la altura necesaria si no se ha proporcionado
        altura_linea = tamaño_fuente + 5  # Altura de línea con margen
        altura_necesaria = (altura_linea * len(lineas_ajustadas)) + 20  # Espacio adicional para márgenes

        if altura_imagen is None:
            altura_imagen = altura_necesaria

        # Crear la imagen con las dimensiones calculadas
        imagen = Image.new('RGB', (anchura_imagen, altura_imagen), color='white')
        dibujo = ImageDraw.Draw(imagen)

        # Dibujar el texto en la imagen
        posicion_y = 10  # Margen superior
        for linea in lineas_ajustadas:
            if posicion_y + altura_linea > altura_imagen - 10:  # Detener si excede la altura de la imagen
                raise Exception("No es posible añadir tantos datos a la imagen")
            dibujo.text((10, posicion_y), linea, font=fuente, fill='black')
            posicion_y += altura_linea

        return imagen, constantes.FORMATO_IMAGEN_OCULTACION

    def desocultar(self):
        """
        Extrae los datos ocultos de la imagen utilizando OCR (Reconocimiento Óptico de Caracteres).

        Si los datos están cifrados, los extrae y decodifica de base64. Si no están cifrados, los devuelve tal cual.

        Returns:
            bytes: Los datos extraídos de la imagen.

        Raises:
            ValueError: Si el texto extraído no es una cadena válida de base64.
        """
        # Configurar si se usará la GPU
        gpu = True if cargar_configuracion(constantes.ARCHIVO_CONFIG)['Ajustes_ocultador_imagen_text']["gpu"] == "True" else False

        if self.cifrado:
            # Convertir la imagen a un array de NumPy
            imagen_array = np.array(self.imagen)
    
            # Crear el lector OCR
            reader = easyocr.Reader(['en'], gpu=gpu)  

            # Extraer texto de la imagen
            resultado = reader.readtext(imagen_array, detail=0, allowlist='ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=') 
            texto_extraido = ''.join(resultado)  # Obtener solo el texto
        else:
            texto_extraido = pytesseract.image_to_string(self.imagen, config='--psm 6 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=')

        # Filtrar caracteres válidos en base64
        texto_base64 = ''.join(filter(lambda c: c.isalnum() or c in '+/=', texto_extraido))

        # Decodificar el texto base64 a bytes
        try:
            if self.cifrado:
                datos_decodificados = base64.b64decode(texto_base64)
            else:
                datos_decodificados = texto_base64.encode()
            print("Datos decodificados exitosamente")
            return datos_decodificados
        except base64.binascii.Error:
            raise ValueError("El texto extraído no es una cadena válida de base64")
