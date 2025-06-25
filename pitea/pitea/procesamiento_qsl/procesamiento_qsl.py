import json
from constantes import constantes
import re
class Procesamiento_datos_qsl:
    
    def procesamiento_datos_qsl(self, datos_decodificados):
        self.__procesamiento_estructura(datos_decodificados)

        
    
    def __procesamiento_estructura(self,datos_decodificados):
        campos_separados= datos_decodificados.decode().split(" ")
        self.__dic_campos = {}
        self.__dic_campos["QRA_RECEPTOR"] = campos_separados[0].split(":")[1].strip()
        self.__dic_campos["DATE"] = campos_separados[1].split(":")[1].strip()
        self.__dic_campos["FREQ"] = campos_separados[3].split(":")[1].strip()
        self.__dic_campos["MODE"] = campos_separados[4].split(":")[1].strip()
        self.__dic_campos["RST"] = campos_separados[5].split(":")[1].strip()
        self.__dic_campos["QRA_EMISOR"] = campos_separados[6].split(":")[1].strip()
        self.__dic_campos["QTH"] = campos_separados[7].split(":")[1].strip()

        raw = campos_separados[2]  # "Time:17:43UTC"

        # Extraer las partes numéricas
        partes = raw.split(":")[1:]  # ['17', '43UTC']

        # Limpiar la segunda parte, quedándonos solo con dígitos
        minutos = re.findall(r'\d+', partes[1])[0]  # '43'

        # Formar el resultado
        hora_formateada = f"{partes[0]}:{minutos}"

        self.__dic_campos["TIME"] = hora_formateada

        json_string = json.dumps(self.__dic_campos, indent=4, ensure_ascii=False)
        bytes_json = json_string.encode('utf-8')
        with open(constantes._RUTA_QSL_DATOS_ESTRUCTURADOS, "wb") as f:
            f.write(bytes_json)

