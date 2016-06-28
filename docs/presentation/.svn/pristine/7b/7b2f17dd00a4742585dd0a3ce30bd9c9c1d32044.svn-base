all: pdf

presentacion: presentacion.dvi
	dvips -t a4 -t landscape -f presentacion.dvi > presentacion.ps

presentacion.dvi: presentacion.tex
	latex presentacion.tex

clean:
	rm -f presentacion.dvi presentacion.ps presentacion.aux presentacion.pdf

doblepagina: presentacion.dvi presentacion a4caras

a4caras:
	psnup -4 presentacion.ps presentacion2.ps

pdf:
	pdflatex presentacion.tex

version:
	tar -cvzf nuevaversion.tgz img/ *.tex makefile *.sty *.jpg *.eps
