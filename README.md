# Parsers

Saves every HTML table from a web page, an HTML file or stdin as one CSV per table, using `pandas.read_html`.

```sh
git clone https://github.com/TanGentleman/Parsers && cd Parsers
uv sync --locked
uv run parsers tests/fixtures/page.html -o fruit
```

Needs [uv](https://docs.astral.sh/uv/) 0.13 or newer; uv installs Python 3.11+ if needed. Details: [IMPLEMENTATION.md](IMPLEMENTATION.md), [ROADMAP.md](ROADMAP.md).
