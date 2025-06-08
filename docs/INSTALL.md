# Guía de instalación 

En este documento se mostrará dónde descargar la aplicación y se
explicará su instalación en Linux.\
Se ha comprobado su funcionamiento en Debian, en la primera iso
descargable en:

``` bash
https://cdimage.debian.org/debian-cd/current/amd64/iso-cd/
```

Para descargar la aplicación es necesario clonar el repositorio de la
herramienta, <https://github.com/Alberto12x/PITEA.git>. Se puede hacer
de la siguiente manera:

``` bash
git clone https://github.com/Alberto12x/PITEA.git
```

o descargando el archivo `.zip` del repositorio de *GitHub*.\
Una vez clonado, es necesario entrar en el repositorio y ejecutar el
archivo `install.sh`, dándole permisos de ejecución si fuera necesario:

``` bash
cd TFG-PITEA-main
chmod +x install.sh
sudo ./install.sh
```

Una vez instalado, se llama a la herramienta por terminal escribiendo:

``` bash
pitea
```

> ⚠️ **Nota importante**  
> Si usas una *shell* con `AUTO_CD` activado como `zsh`, escribir `pitea` desde la raíz del proyecto puede ejecutar `cd pitea` en lugar de la herramienta.
