# Parsers: implementation

## Requirements

- [uv](https://docs.astral.sh/uv/) 0.13 or newer; uv installs Python 3.11+ if needed.
- Dependencies are `lxml` and `pandas`. `uv.lock` pins exact versions; the floors in `pyproject.toml`
  are the versions it was last tested with.
- Network only when `SOURCE` is a URL.

## Usage

```
parsers SOURCE [-o DIR] [--xpath XPATH] [--prefix NAME]
python -m parsers SOURCE ...
```

| Argument | Meaning |
| --- | --- |
| `SOURCE` | An `http://` or `https://` URL, a path to an HTML file, or `-` for stdin. |
| `-o DIR` | Output folder, created if missing. Default: current folder. |
| `--xpath XPATH` | Only tables the XPath matches, or tables inside the elements it matches. |
| `--prefix NAME` | File names are `NAME_1.csv`, `NAME_2.csv`, ... Default: `table`. |

Each written path is printed on stdout; errors go to stderr.

| Exit code | Meaning |
| --- | --- |
| 0 | CSVs written |
| 1 | No tables found (nothing written) |
| 2 | Source unreadable (missing file, HTTP error, no connection) or bad XPath |

The README example writes `fruit/table_1.csv` and `fruit/table_2.csv`; the first is:

```console
Fruit,Price
Apple,1.2
Pear,0.95
```

A live page, keeping only the `wikitable` tables:

```bash
uv run parsers https://en.wikipedia.org/wiki/List_of_largest_cities -o cities \
  --xpath '//table[contains(@class,"wikitable")]'
```

To put `parsers` on your PATH: `uv tool install .` from the clone, or
`uv tool install git+https://github.com/TanGentleman/Parsers`.

## How it works

Everything is in `src/parsers/cli.py`; `src/parsers/__main__.py` makes `python -m parsers` call the same
`run()`.

- `read_source` returns the bytes of a URL (`fetch_url`: one GET, User-Agent `parsers/0.1`, 30 s timeout),
  a file, or stdin.
- `read_tables` parses the bytes with lxml (UTF-8 input is read as UTF-8; otherwise the page's declared
  charset is used), selects every `<table>` or those at or under `--xpath`, drops tables nested inside
  another selected table so none is written twice, and hands the rest to `pd.read_html(..., flavor="lxml",
  keep_default_na=False)`.
- `write_csvs` writes `PREFIX_N.csv` files with `DataFrame.to_csv(index=False)`.

What pandas does to the output:

- colspan and rowspan are filled in; a multi-row header becomes extra header rows.
- Number-like cells are written as numbers: `1.20` becomes `1.2`, `1,234` becomes `1234`.
- Text such as `NA` is kept, not turned into an empty cell.

## Tests

```bash
uv sync --locked
uv run ruff check
uv run ruff format --check
uv run pytest
```

CI (`.github/workflows/ci.yml`) runs these on Python 3.11 and 3.15. `pytest` is offline: it reads
`tests/fixtures` and serves URL sources from 127.0.0.1.

## Limits

- No credentials and no JavaScript: tables a page builds in the browser are not seen.
- Cell text is not kept verbatim where pandas reads it as a number (see above).
