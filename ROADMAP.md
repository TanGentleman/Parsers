# Parsers roadmap

## What it is for

Point it at a web page or a saved HTML file and get every `<table>` as a CSV.
For people who want a spreadsheet out of a Wikipedia or stats page without writing pandas code.

## Status (upstream main 525afd5, checked with Python 3.12, pandas 3.1.1, lxml 6.1.3)

- Nothing ran on current pandas: `parse1.main` and `parse2.main` raised `FileNotFoundError`, because
  `pd.read_html` now treats a literal HTML string as a path. Fixed on Parsers-1 (StringIO).
- `parse2` and `cli_parse.py` failed on a fresh clone: `outputs/` is gitignored and never created. Fixed on Parsers-1.
- `tests.py` is a list of live URLs and XPaths, not tests. `test12` opened `nasty,html`. Fixed on Parsers-1.
- `Parsnip` (`parsers.py`) only lists `<table>` tags; `save_to_csv` and `text_to_tree` are empty stubs.
- No dependency list, no tests, no CI. `logfile.log` was committed run output (untracked on Parsers-1).
- Both parsers are thin wrappers over `pandas.read_html`. On the five fixtures in `html_strings/` with a
  table, `parse2` output equals `pd.read_html(html)[0].to_csv(index=False)` byte for byte; `parse1` matches
  on four and differs on `nasty.html` only by whitespace that BeautifulSoup `prettify()` adds to cells.

## Signal vs noise

Signal: "URL or file in, one CSV per table out", plus an optional XPath to pick tables. pandas does the parsing;
the useful part is a small, tested command around it.

Noise: two parallel parsers that call the same pandas function, the timing race in `parse.py`, the `Parsnip`
stubs, the live-URL `tests.py`, `logfile.log`, and fixtures no test reads.

## Stack

- Parsers-1: import upstream, this roadmap, fixes so `parse1`/`parse2` run on current pandas.
- Parsers-2: `parsers` CLI (`src/parsers/cli.py`, about 100 lines), pyproject + `uv.lock`, 17 offline tests
  (`uv run pytest`, also passing on Python 3.11).
- Parsers-3: README with install command and a fixture example, GitHub Actions CI (ruff + pytest, Python 3.11 and 3.14,
  both run locally; workflow checked with actionlint).
- Parsers-4: remove the legacy scripts and `html_strings/` (10 of 16 files); add `python -m parsers`. 18 tests.

## Applying a branch upstream

Base for every branch is the import commit `1d0d633be4f8` (Parsers-1's first commit).

```bash
git clone https://github.com/TanGentleman/kranti-sandbox && git -C kranti-sandbox fetch origin Parsers-N
git clone https://github.com/TanGentleman/Parsers && cd Parsers
git -C ../kranti-sandbox format-patch --relative=Parsers --stdout 1d0d633be4f8..origin/Parsers-N > stack.patch
git am stack.patch
uv sync && uv run pytest   # from Parsers-2 on
```

## Needs Tan

- Numbers: pandas turns number-like cells into numbers, so `1.20` is written as `1.2` and `1,234` as `1234`.
  Keeping the raw cell text would mean replacing `read_html` with our own cell walk. Kept pandas for now.
- Name: `parsers` is taken on PyPI ("Collection of reusable parsing utilities"). Pick another name before publishing.

- Confirm cutting `parse1.py`, `parse2.py`, `parse.py`, `parsers.py` (`Parsnip`), `cli_parse.py` and `tests.py` (Parsers-4).
