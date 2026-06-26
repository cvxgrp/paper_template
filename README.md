# paper_template

A starter template for writing academic papers in LaTeX, with a reproducible
build and automated PDF compilation on every push.

## Layout

```
.
├── paper/
│   ├── main.tex        # the paper
│   └── references.bib  # bibliography
├── figures/            # figures (PDF/PNG/...)
├── Makefile            # build / clean targets
└── .github/workflows/  # CI that builds the PDF
```

## Building

You need a LaTeX distribution (e.g. TeX Live or MacTeX) with `latexmk`.

```bash
make        # build paper/main.pdf
make clean  # remove build artifacts
```

The PDF is also built automatically by GitHub Actions on every push and is
available as a workflow artifact (and attached to tagged releases).

## License

[MIT](LICENSE)
