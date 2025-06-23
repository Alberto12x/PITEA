#!/bin/bash -f

# ───────────── CONFIGURACIÓN GENERAL ─────────────

IFILE="fondos_tarjetas/qsl2.jpg"            # Imagen base negra (1024x768)
SIZE="320x256"              # Tamaño final para SSTV
FONT="Bitstream-Charter-Regular"
COLOR="yellow"
POINTSIZE=90                # LETRA GRANDE para máxima legibilidad
MY_QRA="EA4IAX"
OFILE="sstv_qsl.jpg"

# Coordenadas línea por línea (espaciado amplio)
L1="50,120"
L2="50,210"
L3="50,300"
L4="50,390"
L5="50,480"
L6="50,570"
L7="50,660"
L8="50,750"

function usage {
  echo "Uso: $(basename $0) qra qth date utc freq mode rst"
  exit 1
}

if [ $# -ne 7 ]; then
  usage
fi

qra="$1"
qth="$2"
fecha="$3"
qtr="$4"
freq="$5"
mode="$6"
rst="$7"

if [ ! -f "$IFILE" ]; then
  echo "❌ Imagen base '$IFILE' no encontrada."
  exit 1
fi

cp "$IFILE" "$OFILE"

# Insertar texto
convert -font "$FONT" -pointsize "$POINTSIZE" -fill "$COLOR" \
    -draw "text $L1 \"To: $qra\"" \
    -draw "text $L2 \"Date: $fecha\"" \
    -draw "text $L3 \"Time: $qtr UTC\"" \
    -draw "text $L4 \"Freq: $freq\"" \
    -draw "text $L5 \"Mode: $mode\"" \
    -draw "text $L6 \"RST: $rst\"" \
    -draw "text $L7 \"From: $MY_QRA\"" \
    -draw "text $L8 \"QTH: $qth\"" \
    "$OFILE" "$OFILE"

# Redimensionar para SSTV
convert -resize "$SIZE" "$OFILE" "$OFILE"

# Metadatos (opcional)
# exiv2 -M"set Exif.Image.Artist $MY_QRA" "$OFILE"
# exiv2 -M"set Exif.Image.DateTime $fecha $qtr" "$OFILE"
# exiv2 -M"set Exif.Photo.UserComment $MY_QRA QSL to $qra, $freq, $mode, $rst" "$OFILE"

echo "✅ Imagen SSTV QSL generada como: $OFILE"
