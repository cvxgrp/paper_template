# paper_template

A starter template for writing academic papers in LaTeX, with a reproducible
build and automated PDF compilation on every push.

## Layout

```
.
├── paper/
│   ├── main.tex        # the paper
│   ├── refs/
│   │   └── references.bib  # bibliography
│   └── figures/        # figures (PDF/PNG/...)
├── Makefile            # build / clean targets
└── .github/workflows/  # CI that builds the PDF
```

## Building

You need a LaTeX distribution (e.g. TeX Live or MacTeX) with `pdflatex` and
`bibtex`.

```bash
make          # show the available targets
make compile  # build paper/main.pdf
make clean    # remove build artifacts (keeps the PDF)
```

## Continuous integration

Two GitHub Actions workflows run automatically:

- **build.yml** — compiles the PDF on every push and pull request, uploads it
  as a workflow artifact, attaches it to tagged releases, and (on pushes to
  `main`) publishes it to the `pdf` branch.
- **arxiv.yml** — on pushes to `main`, assembles a self-contained arXiv
  submission tarball (source `.tex`, `references.bib`, pre-built `.bbl`, and
  figure PDFs), verifies it compiles standalone, and publishes it to the
  `arxiv` branch.

## License

[MIT](LICENSE)
