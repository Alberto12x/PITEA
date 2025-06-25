#!/bin/bash 

function usage {
  echo "Uso: $(basename $0) qra qth date utc freq mode rst ifile size font color pointsize my_qra ofile l1 l2 l3 l4 l5 l6 l7 l8"
  exit 1
}

if [ $# -ne 22 ]; then
  usage
fi

qra="$1"
qth="$2"
fecha="$3"
qtr="$4"
freq="$5"
mode="$6"
rst="$7"
IFILE="$8"         # Imagen base negra (1024x768)
SIZE="$9"           # Tamaño final para SSTV
FONT="${10}"
COLOR="${11}"
POINTSIZE="${12}"               # LETRA GRANDE para máxima legibilidad
MY_QRA="${13}"
OFILE="${14}"
L1="${15}"
L2="${16}"
L3="${17}"
L4="${18}"
L5="${19}"
L6="${20}"
L7="${21}"
L8="${22}"

echo "$20"



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
