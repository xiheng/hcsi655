#!/bin/sh

pdflatex doc
pdflatex doc
bibtex doc
pdflatex doc
open doc.pdf
