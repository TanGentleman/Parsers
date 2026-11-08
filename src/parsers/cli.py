import argparse
import io
import sys
import urllib.request
from collections.abc import Callable
from pathlib import Path

import lxml.etree
import lxml.html
import pandas as pd

USER_AGENT = "parsers/0.1 (+https://github.com/TanGentleman/Parsers)"


def fetch_url(url: str, timeout: float = 30) -> bytes:
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(request, timeout=timeout) as response:
        return response.read()


def read_source(source: str, fetch: Callable[[str], bytes] = fetch_url) -> bytes:
    """Return the HTML bytes of a URL, a file path, or "-" for stdin."""
    if source.startswith(("http://", "https://")):
        return fetch(source)
    if source == "-":
        return sys.stdin.buffer.read()
    return Path(source).read_bytes()


def html_parser(html: bytes) -> lxml.html.HTMLParser:
    """Read UTF-8 as UTF-8; otherwise let lxml use the page's declared charset."""
    try:
        html.decode("utf-8")
    except UnicodeDecodeError:
        return lxml.html.HTMLParser()
    return lxml.html.HTMLParser(encoding="utf-8")


def read_tables(html: bytes, xpath: str | None = None) -> list[pd.DataFrame]:
    """Parse every table in the HTML, or only those at or under an XPath."""
    if not html.strip():
        return []
    tree = lxml.html.document_fromstring(html, parser=html_parser(html))
    if xpath:
        tables = []
        for element in tree.xpath(xpath):
            if isinstance(element, lxml.html.HtmlElement):
                tables += [element] if element.tag == "table" else element.findall(".//table")
    else:
        tables = tree.findall(".//table")
    selected = set(tables)
    tables = [t for t in tables if not any(a in selected for a in t.iterancestors())]
    if not tables:
        return []
    markup = "".join(lxml.html.tostring(table, encoding="unicode") for table in tables)
    try:
        return pd.read_html(io.StringIO(markup), flavor="lxml", keep_default_na=False)
    except ValueError as error:
        if "No tables found" in str(error):
            return []
        raise


def write_csvs(tables: list[pd.DataFrame], outdir: Path, prefix: str = "table") -> list[Path]:
    outdir.mkdir(parents=True, exist_ok=True)
    paths = []
    for number, table in enumerate(tables, start=1):
        path = outdir / f"{prefix}_{number}.csv"
        table.to_csv(path, index=False)
        paths.append(path)
    return paths


def main(argv: list[str] | None = None, fetch: Callable[[str], bytes] = fetch_url) -> int:
    parser = argparse.ArgumentParser(
        prog="parsers", description="Save every HTML table at a URL or in a file as a CSV."
    )
    parser.add_argument("source", help="URL, path to an HTML file, or - for stdin")
    parser.add_argument("-o", "--outdir", type=Path, default=Path("."), help="output folder (default: .)")
    parser.add_argument("--xpath", help="only tables at or under this XPath")
    parser.add_argument("--prefix", default="table", help="CSV file name prefix (default: table)")
    args = parser.parse_args(argv)

    try:
        html = read_source(args.source, fetch)
    except (OSError, ValueError) as error:
        print(f"parsers: cannot read {args.source}: {error}", file=sys.stderr)
        return 2
    try:
        tables = read_tables(html, args.xpath)
    except lxml.etree.XPathError as error:
        print(f"parsers: bad XPath {args.xpath!r}: {error}", file=sys.stderr)
        return 2
    if not tables:
        print("parsers: no tables found", file=sys.stderr)
        return 1
    for path in write_csvs(tables, args.outdir, args.prefix):
        print(path)
    return 0


def run() -> None:
    sys.exit(main())
