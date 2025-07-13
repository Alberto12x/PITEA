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
            

        
       
       
        json_string = json.dumps(self.__dic_campos, indent=4, ensure_ascii=False)
        bytes_json = json_string.encode('utf-8')
        with open(constantes._RUTA_QSL_DATOS_ESTRUCTURADOS, "wb") as f:
            f.write(bytes_json)


    def __estructura_pitea(self,campos_separados) :
        print(campos_separados)
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


