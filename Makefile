# Makefile for building the LaTeX document.

DOC      := main
SRCDIR   := paper
PDF      := $(SRCDIR)/$(DOC).pdf
TEX      := $(SRCDIR)/$(DOC).tex
BIB      := $(SRCDIR)/refs/references.bib
LATEX    := pdflatex
LATEXOPTS := -interaction=nonstopmode -halt-on-error

# Running `make` with no target prints the overview below.
.DEFAULT_GOAL := help

.PHONY: help compile clean

# Self-documenting help: lists every target with a `## description` comment.
help:  ## Show this overview of available commands
	@echo "Usage: make <target>"
	@echo ""
	@echo "Targets:"
	@grep -E '^[a-zA-Z_-]+:.*## ' $(MAKEFILE_LIST) \
		| sort \
		| awk -F':.*## ' '{ printf "  %-10s %s\n", $$1, $$2 }'

# Compile the document. The first pass writes the .aux citation list, BibTeX
# turns it into a formatted .bbl from refs/references.bib, and the final two
# passes fold the bibliography in and resolve all cross-references.
compile: $(PDF)  ## Build the LaTeX document (main.pdf)

$(PDF): $(TEX) $(BIB)
	cd $(SRCDIR) && $(LATEX) $(LATEXOPTS) $(DOC).tex
	cd $(SRCDIR) && bibtex $(DOC)
	cd $(SRCDIR) && $(LATEX) $(LATEXOPTS) $(DOC).tex
	cd $(SRCDIR) && $(LATEX) $(LATEXOPTS) $(DOC).tex
	$(MAKE) clean

# Remove LaTeX build artifacts (keeps the generated PDF).
clean:  ## Remove LaTeX build artifacts (keeps the generated PDF)
	cd $(SRCDIR) && rm -f $(DOC).aux $(DOC).log $(DOC).out $(DOC).toc \
		$(DOC).bbl $(DOC).blg $(DOC).nav $(DOC).snm $(DOC).vrb
