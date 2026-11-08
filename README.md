# Parsers

Save every HTML table on a web page, or in an HTML file, as a CSV. Parsing is
`pandas.read_html` with lxml.

## Quick start

Needs [uv](https://docs.astral.sh/uv/) 0.13 or newer; uv installs Python 3.11+ if needed.

```bash
git clone https://github.com/TanGentleman/Parsers && cd Parsers
uv sync --locked
uv run parsers tests/fixtures/page.html -o fruit
cat fruit/table_1.csv
```

```console
fruit/table_1.csv
fruit/table_2.csv
Fruit,Price
Apple,1.2
Pear,0.95
```

To put `parsers` on your PATH: `uv tool install .` from the clone, or
`uv tool install git+https://github.com/TanGentleman/Parsers`.

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

A live page, keeping only the `wikitable` tables:

```bash
parsers https://en.wikipedia.org/wiki/List_of_largest_cities -o cities \
  --xpath '//table[contains(@class,"wikitable")]'
```

## Output

- colspan and rowspan are filled in; a multi-row header becomes extra header rows.
- Number-like cells are written as numbers: `1.20` becomes `1.2`, `1,234` becomes `1234`.
- Text such as `NA` is kept, not turned into an empty cell.
- A table nested inside a selected table is not written twice.
- UTF-8 input is read as UTF-8; otherwise the page's declared charset is used.

## Boundaries

- The only network request is a GET of a URL `SOURCE` (User-Agent
  `parsers/0.1`, 30 s timeout). Files and stdin are read locally.
- No credentials, no JavaScript: tables a page builds in the browser are not seen.

## Development

```bash
uv sync --locked
uv run ruff check
uv run ruff format --check
uv run pytest          # offline: tests/fixtures, URLs served from 127.0.0.1
```

CI (`.github/workflows/ci.yml`) runs these commands on Python 3.11 and 3.15.
`uv.lock` pins exact versions; the floors in `pyproject.toml` are the versions it was
last tested with.
