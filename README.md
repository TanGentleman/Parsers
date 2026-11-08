# Parsers

Save every HTML table on a web page, or in an HTML file, as a CSV.

```bash
uv tool install git+https://github.com/TanGentleman/Parsers
```

## Example

```console
$ parsers tests/fixtures/page.html -o fruit
fruit/table_1.csv
fruit/table_2.csv
$ cat fruit/table_1.csv
Fruit,Price
Apple,1.2
Pear,0.95
```

A live page, keeping only the tables at or under an XPath:

```bash
parsers https://en.wikipedia.org/wiki/List_of_largest_cities -o cities --xpath '//table[contains(@class,"wikitable")]'
```

## Usage

```
parsers SOURCE [-o DIR] [--xpath XPATH] [--prefix NAME]
```

- `SOURCE`: an `http(s)://` URL, a path to an HTML file, or `-` for stdin.
- `-o DIR`: output folder, created if missing (default: current folder).
- `--xpath`: only tables matched by the XPath, or inside the elements it matches.
- `--prefix`: file names are `<prefix>_1.csv`, `<prefix>_2.csv`, ... (default: `table`).

Exit code 0 when CSVs were written, 1 when no tables were found, 2 when the source or XPath is bad.

Parsing is `pandas.read_html`: colspan and rowspan are filled in, multi-row headers become extra header
rows, and number-like cells are written as numbers (`1.20` becomes `1.2`).

## Development

```bash
uv sync
uv run pytest          # offline, uses tests/fixtures
uv run ruff check && uv run ruff format --check
```

The older `parse1.py`, `parse2.py`, `parse.py` and `parsers.py` scripts predate the CLI; see `ROADMAP.md`.
