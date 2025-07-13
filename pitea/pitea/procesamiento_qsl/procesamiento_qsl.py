import json
from constantes import constantes
import re
class Procesamiento_datos_qsl:
    
    def procesamiento_datos_qsl(self, datos_decodificados):
        self.__dic_campos = {}
        self.__procesamiento_estructura(datos_decodificados)

        
    
    def __procesamiento_estructura(self,datos_decodificados):

        FORMAS_PITEA = ["PITEA", "P1TEA", "P1T3A", "P1T3A", "P1T3E", "P1T3EA", "P1T3E1", "P1T3E2", "P1T3E3",]
        
        if any(palabra in datos_decodificados.decode() for palabra in FORMAS_PITEA):
            campos_separados= datos_decodificados.decode().split(" ")
            self.__estructura_pitea(campos_separados) 
        else:
            self.__estructura_cualquiera(datos_decodificados.decode())
            
        json_string = json.dumps(self.__dic_campos, indent=4, ensure_ascii=False)
        bytes_json = json_string.encode('utf-8')

        with open(constantes._RUTA_QSL_DATOS_ESTRUCTURADOS, "wb") as f:
            f.write(bytes_json)


    def __estructura_pitea(self,campos_separados) :
        self.__dic_campos["QRA_RECEPTOR"] = campos_separados[0].split(":")[1].strip()
        self.__dic_campos["DATE"] = campos_separados[1].split(":")[1].strip()
        self.__dic_campos["FREQ"] = campos_separados[3].split(":")[1].strip()
        self.__dic_campos["MODE"] = campos_separados[4].split(":")[1].strip()
        self.__dic_campos["RST"] = campos_separados[5].split(":")[1].strip()
        self.__dic_campos["QRA_EMISOR"] = campos_separados[6].split(":")[1].strip()
        self.__dic_campos["QTH"] = campos_separados[7].split(":")[1].strip()

        hora_cruda = campos_separados[2]  # "Time:17:43UTC"

        # Extraer las partes numéricas
        partes_hora = hora_cruda.split(":")[1:]  # ['17', '43UTC']

        # Limpiar la segunda parte, quedándonos solo con dígitos
        minutos = re.findall(r'\d+', partes_hora[1])[0]  # '43'

        # Formar el resultado
        hora_formateada = f"{partes_hora[0]}:{minutos}"

        self.__dic_campos["TIME"] = hora_formateada

        
    def __estructura_cualquiera(self, input_text):
        """
        Procesa los datos sacados de tarjetas QSL con una estructura cualquiera,
        para cumplir con cualquier formato y error de OCR, asumimos
        que los datos no están separados por espacios ni nada, entendiendo todo como un único string.
        Además tenemos en cuenta los fallos típicos de OCR, como el cambio de 0 por O, o 1 por I, etc.
        """

        # Modos SSTV, por ejemplo
        patron_modo = r"(" + "|".join(constantes.MODOS_VALIDOS_SSTV) + r")"

        patron_qra = r"([A-R]{2}\d{2}(?:[a-x]{2})?|[A-Z]{1,2}\d{1}[A-Z]{1,3})"

        patrones_date = [
            r"((?:0?[1-9]|[12][0-9]|3[01])[-\/\.](?:0?[1-9]|1[012])[-\/\.](?:\d{2}|\d{4}))",  # DD/MM/YYYY o D/M/YY
            r"(\d{4}[-\/\.](?:0?[1-9]|1[012])[-\/\.](?:0?[1-9]|[12][0-9]|3[01]))",  # YYYY-MM-DD (ISO)
            r"((?:January|February|March|April|May|June|July|August|September|October|November|December)\s?(?:0?[1-9]|[12][0-9]|3[01]),?\s?\d{4})",  # Mes Nombre DD, YYYY
            r"((?:0?[1-9]|[12][0-9]|3[01])\s?(?:January|February|March|April|May|June|July|August|September|October|November|December)\s??\d{4})",  # DD Mes Nombre YYYY
        ]

        patrones_hora = [
            r"((?:[01]?\d|2[0-3])[:\.][0-5]\d(?:[:\.][0-5]\d)?)",  # 24h con minutos y opcional segundos
            r"((?:0?[1-9]|1[0-2])[:\.][0-5]\d\s?(?:AM|PM|am|pm))",  # 12h con minutos + AM/PM
            r"((?:[01]\d|2[0-3])[0-5]\d)",  # 24h sin separador, HHMM
            r"((?:0?[1-9]|1[0-2])\s??(?:AM|PM|am|pm))",  # 12h sin minutos, solo HH AM/PM
            r"((?:[01]?\d|2[0-3])[:\.][0-5]\d(?:[:\.][0-5]\d)?\s?(?:UTC|GMT|Z|z)(?:[+\-]\d{2}(?::?\d{2})?)?)",  # 24h con zona horaria
            r"((?:0?[1-9]|1[0-2])[:\.][0-5]\d\s?(?:AM|PM|am|pm)\s?(?:UTC|GMT|Z|z)(?:[+\-]\d{2}(?::?\d{2})?)?)",  # 12h con AM/PM y zona horaria
        ]

        patron_freq = r"(\d{1,3}(?:\.\d{1,3})?\s?(?:kHz|KHz|KHZ|MHz|MHZ|hz|Hz)?)"

        patron_qth = r"[A-R]{2}[0-9]{2}(?:[A-X]{2})?"  # QTH sin ^ y $

        patron_rst = r"((?:RST|RS)?[ :\-]?\s?[1-5][1-9]{1,2})"

        self.__dic_campos = {}

        # Busca modo
        self.__dic_campos['MODE'] = re.findall(patron_modo, input_text, re.IGNORECASE)

        # Busca qra
        self.__dic_campos['QRA_RECEPTOR'] = re.findall(patron_qra, input_text, re.IGNORECASE)
        self.__dic_campos['QRA_EMISOR'] = self.__dic_campos['QRA_RECEPTOR']

        # Busca fechas: cada patrón individual, concatenando self.__dic_campos
        fechas = []
        for p in patrones_date:
            fechas.extend(re.findall(p, input_text, re.IGNORECASE))
        self.__dic_campos['DATE'] = fechas

        # Busca horas: igual que fechas
        horas = []
        for p in patrones_hora:
            horas.extend(re.findall(p, input_text, re.IGNORECASE))
        self.__dic_campos['TIME'] = horas

        # Busca frecuencia
        self.__dic_campos['FREQ'] = re.findall(patron_freq, input_text, re.IGNORECASE)

        # Busca qth
        self.__dic_campos['QTH'] = re.findall(patron_qth, input_text, re.IGNORECASE)

        # Busca rst
        self.__dic_campos['RST'] = re.findall(patron_rst, input_text, re.IGNORECASE)

         









