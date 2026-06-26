PAPER   := main
SRC_DIR := paper
PDF     := $(SRC_DIR)/$(PAPER).pdf

.PHONY: all clean watch

all: $(PDF)

$(PDF): $(SRC_DIR)/$(PAPER).tex $(SRC_DIR)/references.bib
	latexmk -pdf -cd -interaction=nonstopmode -halt-on-error $(SRC_DIR)/$(PAPER).tex

watch:
	latexmk -pdf -pvc -cd -interaction=nonstopmode $(SRC_DIR)/$(PAPER).tex

clean:
	latexmk -cd -C $(SRC_DIR)/$(PAPER).tex
	rm -f $(SRC_DIR)/*.bbl $(SRC_DIR)/*.run.xml
