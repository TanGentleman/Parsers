"""Turn the HTML tables on a web page or in a file into CSV files."""

from parsers.cli import main, read_source, read_tables, write_csvs

__all__ = ["main", "read_source", "read_tables", "write_csvs"]
