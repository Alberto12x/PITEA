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
        equivalencias = {
            '0': '[0o]',
            '1': '[1il]',
            '2': '[2s]',
            '5': '[5z]',
            '8': '[8b]',
            'a': '[a]',
            'b': '[b8]',
            'c': '[c]',
            'd': '[d]',
            'e': '[e3]',
            'g': '[g9]',
            'i': '[i1l]',
            'l': '[l1i]',
            'o': '[o0]',
            'q': '[q]',
            's': '[s2]',
            't': '[t7]',
            'z': '[z5]',
        }

        def modo_a_regex(modo: str) -> str:
            resultado = ''
            for c in modo:
                key = c.lower()
                if key in equivalencias:
                    resultado += equivalencias[key]
                else:
                    resultado += f"[{c.lower()}]"
            return resultado
        
        def grupo_modos_a_regex(grupo: str) -> str:
            modos = grupo.split('|')
            return '|'.join(modo_a_regex(modo) for modo in modos)

        grupo = "January|February|March|April|May|June|July|August|September|October|November|December"
        meses_tolerante = grupo_modos_a_regex(grupo)

        # Modos SSTV, por ejemplo
        patron_modo = r"(" + "|".join(modo_a_regex(modo) for modo in constantes.MODOS_VALIDOS_SSTV) + r")"


        patron_qra = r"([A-R125890]{2}[0-9ISZO]{2}(?:[a-x1250]{2})?|[A-Z125890]{1,2}[0-9ISZO][A-Z125890]{1,3})"

        patrones_date = [
            r"((?:[0O]?[1-9ISZ]|[12ISZ][0-9ISZO]|3[01OI])[-\/\.](?:[O0]?[1-9ISZ]|1[012ISZ])[-\/\.](?:[0-9ISZO]{2}|[0-9ISZO]{4}))",  # DD/MM/YYYY o D/M/YY
            r"([0-9ISZO]{4}[-\/\.](?:[O0]?[1-9ISZ]|1[012OISZ])[-\/\.](?:[O0]?[1-9ISZ]|[12ISZ][0-9ISZO]|3[01OI]))",  # YYYY-MM-DD (ISO)
            rf"((?:{meses_tolerante})\s?(?:[O0]?[1-9ISZ]|[12ISZ][0-9ISZO]|3[01OI])[,/]?\s?[0-9ISZO]{{4}})",  # Mes Nombre DD, YYYY
            rf"((?:[O0]?[1-9ISZ]|[12ISZ][1-9ISZO]|3[01OI])\s?(?:{meses_tolerante}\s??[0-9ISZO]{4}))",  # DD Mes Nombre YYYY
        ]

        patrones_hora = [
            r"((?:[01IO]?[0-9ISZO]|2[0-3])[:\.][0-5][0-9ISZO](?:[:\.][0-5][0-9ISZO])?)",  # 24h con minutos y opcional segundos
            r"((?:[O0]?[1-9ISZ]|1[0-2])[:\.][0-5][0-9ISZO]\s?(?:AM|PM))",  # 12h con minutos + AM/PM
            r"((?:[01IO][0-9ISZO]|2[0-3])[0-5][0-9ISZO])",  # 24h sin separador, HHMM
            r"((?:[O0]?[1-9ISZ]|1[0-2])\s??(?:AM|PM))",  # 12h sin minutos, solo HH AM/PM
            r"((?:[01IO]?[0-9ISZO]|2[0-3])[:\.][0-5][0-9ISZO](?:[:\.][0-5][0-9ISZO])?\s?(?:UTC|GMT|Z|z)(?:[+\-][0-9ISZO]{2}(?::?[0-9ISZO]{2})?)?)",  # 24h con zona horaria
            r"((?:[O0]?[1-9ISZ]|1[0-2])[:\.][0-5][0-9ISZO]\s?(?:AM|PM)\s?(?:UTC|GMT|Z|z)(?:[+\-][0-9ISZO]{2}(?::?[0-9ISZO]{2})?)?)",  # 12h con AM/PM y zona horaria
        ]

        patron_freq = r"([0-9ISZO]{1,3}(?:\.[0-9ISZO]{1,3})?\s?(?:kH[Z2]|KH[Z2]|KH[Z2]|MH[Z2]|MH[Z2]|h[Z2]|H[Z2])?)"

        patron_qth = r"[A-R125890]{2}[1-9ISZO]{2}(?:[A-X125890]{2})?"  

        todas_posibilidades_rst = (
            constantes.MODOS_SNR |
            constantes.MODOS_RST_COMPLETO |
            constantes.MODOS_RS
        )
        patron_rst = r"((?:R[5S]T|R[5S])?[ :\-]?\s?[1-5ISZ][1-9ISZ]{1,2})"

        patron_rst = r"(" + "|".join(modo_a_regex(modo) for modo in todas_posibilidades_rst) + r")"

         

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

         









