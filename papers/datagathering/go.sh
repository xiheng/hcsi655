#!/bin/sh

pdflatex doc
pdflatex doc
bibtex doc
pdflatex doc
skim doc.pdf