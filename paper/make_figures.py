# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "matplotlib==3.11.0",
#     "numpy==2.4.6",
#     "typer==0.26.7",
# ]
# ///
"""Figures for the paper.

One self-contained, seeded entry point that builds the paper's figures. A small
Typer CLI selects which figure to build; with no argument it asks interactively.

    uv run paper/make_figures.py            # ask which figure, or all
    uv run paper/make_figures.py all        # every figure
    uv run paper/make_figures.py sine       # just one figure

Each figure is written as a PDF into ``paper/figures/`` (resolved relative to
this script, so the working directory does not matter). Add a new figure by
writing a ``figure_*`` function and registering it in ``Target`` / ``_run_target``.
"""

from __future__ import annotations

import enum
from pathlib import Path
from typing import Annotated

import matplotlib.pyplot as plt
import numpy as np
import typer

# Output directory: alongside this script, so artifacts land in paper/figures/
# regardless of the working directory the command is run from.
DEFAULT_OUT_DIR = Path(__file__).resolve().parent / "figures"

# Seed for the data-driven figures, so re-runs reproduce the committed PDFs.
SEED = 42


def figure_sine(out_dir: Path) -> Path:
    """A damped sine wave -- a minimal analytic example figure."""
    x = np.linspace(0.0, 4.0 * np.pi, 400)
    y = np.exp(-0.2 * x) * np.sin(2.0 * x)

    fig, ax = plt.subplots(figsize=(6.0, 3.6))
    ax.plot(x, y, lw=1.6)
    ax.axhline(0.0, color="0.6", lw=0.6)
    ax.set_xlabel("$x$")
    ax.set_ylabel(r"$e^{-x/5}\sin 2x$")
    ax.set_title("A damped sine wave")
    fig.tight_layout()

    out = out_dir / "sine.pdf"
    fig.savefig(out)
    plt.close(fig)
    print(f"wrote {out}")
    return out


def figure_scatter(out_dir: Path) -> Path:
    """A seeded scatter with a least-squares fit -- a minimal data example."""
    rng = np.random.default_rng(SEED)
    x = rng.uniform(0.0, 10.0, size=60)
    y = 0.7 * x + 1.5 + rng.normal(scale=1.2, size=x.size)
    slope, intercept = np.polyfit(x, y, deg=1)

    grid = np.linspace(x.min(), x.max(), 100)
    fig, ax = plt.subplots(figsize=(6.0, 3.6))
    ax.scatter(x, y, s=18, alpha=0.7, label="data")
    ax.plot(grid, slope * grid + intercept, color="C3", lw=1.8,
            label=rf"fit: $y = {slope:.2f}x + {intercept:.2f}$")
    ax.set_xlabel("$x$")
    ax.set_ylabel("$y$")
    ax.set_title("Least-squares fit")
    ax.legend(fontsize=8, loc="best")
    fig.tight_layout()

    out = out_dir / "scatter.pdf"
    fig.savefig(out)
    plt.close(fig)
    print(f"wrote {out}")
    return out


# --------------------------------------------------------------------------------------
# Typer CLI
# --------------------------------------------------------------------------------------
class Target(enum.StrEnum):
    """A buildable figure, or a group of them."""

    sine = "sine"
    scatter = "scatter"
    all = "all"


_DESCRIPTIONS: dict[Target, str] = {
    Target.sine: "a damped sine wave            -> sine.pdf",
    Target.scatter: "scatter with a fitted line    -> scatter.pdf",
    Target.all: "every figure",
}


def _choose_target() -> Target:
    """Interactively ask which figure to build when none was given on the CLI."""
    options = list(Target)
    typer.echo("Which figure to generate?\n")
    for i, t in enumerate(options, 1):
        typer.echo(f"  {i:>2}. {t.value:<10} {_DESCRIPTIONS[t]}")
    typer.echo("")
    while True:
        raw = typer.prompt("Enter a number or name").strip()
        if raw.isdigit() and 1 <= int(raw) <= len(options):
            return options[int(raw) - 1]
        try:
            return Target(raw)
        except ValueError:
            typer.echo(f"  '{raw}' is not a valid choice; try again.")


def _run_target(target: Target, out_dir: Path) -> None:
    """Build the requested figure(s)."""
    out_dir.mkdir(parents=True, exist_ok=True)
    if target in (Target.all, Target.sine):
        figure_sine(out_dir)
    if target in (Target.all, Target.scatter):
        figure_scatter(out_dir)


app = typer.Typer(add_completion=False, help=__doc__)


@app.command()
def main(
    target: Annotated[
        Target | None,
        typer.Argument(help="Which figure to build. Omit to choose interactively."),
    ] = None,
    out_dir: Annotated[
        Path,
        typer.Option(help="Directory to write figures into."),
    ] = DEFAULT_OUT_DIR,
) -> None:
    """Build a paper figure (or all of them)."""
    if target is None:
        target = _choose_target()
    _run_target(target, out_dir)


if __name__ == "__main__":
    app()
