from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

SEMILLA = b'\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0a\x0b\x0c\x0d\x0e\x0f\x10'


def descifrar_archivo(archivo_cifrado, archivo_salida, contraseña):
    tamano_bloque = AES.block_size
    
    # Leer el archivo cifrado
    with open(archivo_cifrado, 'rb') as f:
        iv = f.read(tamano_bloque)  # Leer el IV al inicio
        datos_cifrados = f.read()  # Leer los datos cifrados

    # Transformación de contraseña a clave
    contraseña_bytes = contraseña.encode()

    # Rellenar o truncar la contraseña a 16 bytes
    if len(contraseña_bytes) < 16:
        contraseña_bytes += b'\x00' * (16 - len(contraseña_bytes))  # Rellenar con 0s
    else:
        contraseña_bytes = contraseña_bytes[:16]  # Tomar los primeros 16 bytes

    # Mezclar la contraseña con SEMILLA usando XOR
    clave = bytes(a ^ b for a, b in zip(contraseña_bytes, SEMILLA))  # XOR para mezclar

    # Crear el descifrador y descifrar los datos
    descifrador = AES.new(clave, AES.MODE_CBC, iv)
    datos_descifrados = unpad(descifrador.decrypt(datos_cifrados), tamano_bloque)

    print(datos_descifrados)