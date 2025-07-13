# TFG-PITEA

## Licencia

Este proyecto está licenciado bajo los términos de la [GNU GPL v3](LICENSE), © 2025 Alberto Martín Oruña y Rodrigo Gallego Marín.

## 📦 Instalación

Consulta la [Guía de instalación](./docs/INSTALL.md).

## 🚀 Uso

Consulta la [Guía de uso](./docs/USAGE.md).

## USOS DE IBERRADIO(AQUI POR COMODIDAD HASTA PROXIMO RELEASE)

## Data Sources and License

This project uses data from the GeoNames geographical database in the file [localidades.txt](pitea/localidades.txt).

- 🔗 Source: [GeoNames.org](https://www.geonames.org)
- 📄 License: [Creative Commons Attribution 4.0](https://creativecommons.org/licenses/by/4.0/)

The data may contain inaccuracies or be incomplete. Use at your own risk.

### GENERAR-TARJETA

No son datos validos por ahora, porque no se que son validos

```bash
./script_ejecucion.py generar-tarjeta -qra EA5CO -qth Namibia_JG87 -fecha 2025/06/08 -hora 17:43 -freq 28 -modo 10m -rst a
```

### Intercambio-qsl

```bash
./script_ejecucion.py intercambio-qsl --input ./archivos_prueba/iberradio/transmision.png
```
