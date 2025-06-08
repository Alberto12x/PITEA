# Nombre del archivo principal (sin extensión .tex)
MAIN = TFGTeXiS

# Compilador LaTeX
LATEX = pdflatex
BIB = bibtex

# Opciones de compilación
LATEX_OPTS = -shell-escape -interaction=nonstopmode

# Archivos temporales a limpiar
CLEAN_EXT = aux bbl bcf blg log out run.xml toc lof lot fls fdb_latexmk

all: pdf

pdf:
	latexmk -pdf -shell-escape $(MAIN).tex

clean:
	latexmk -c

cleanall: clean
	rm -f $(MAIN).pdf