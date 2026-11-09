import functools
import http.server
import io
import socket
import subprocess
import sys
import threading
from pathlib import Path

import pytest

from parsers import main, read_source, read_tables
from parsers.cli import USER_AGENT, fetch_url

FIXTURES = Path(__file__).parent / "fixtures"


def fixture(name: str) -> str:
    return str(FIXTURES / name)


def test_file_to_one_csv_per_table(tmp_path, capsys):
    assert main([fixture("page.html"), "-o", str(tmp_path)]) == 0
    assert capsys.readouterr().out.split() == [str(tmp_path / "table_1.csv"), str(tmp_path / "table_2.csv")]
    assert (tmp_path / "table_1.csv").read_text() == "Fruit,Price\nApple,1.2\nPear,0.95\n"
    assert (tmp_path / "table_2.csv").read_text() == "Fruit,Crates\nApple,12\nPear,7\n"


def test_colspan_and_rowspan_are_filled(tmp_path):
    assert main([fixture("spans.html"), "-o", str(tmp_path)]) == 0
    assert (tmp_path / "table_1.csv").read_text() == (
        "0,1,2,3,4\n1,1,1,4,5\n1,2,3,4,5\n1,2,3,4,5\n1,2,2,2,5\n1,2,3,3,3\n"
    )


def test_two_header_rows_and_utf8(tmp_path):
    assert main([fixture("scores.html"), "-o", str(tmp_path), "--prefix", "scores"]) == 0
    assert (tmp_path / "scores_1.csv").read_text(encoding="utf-8") == (
        "Name,Scores,Scores,Scores\nName,Math 😀😂🔥🌟,Science,English\nJohn,90,85,92\nJane,95,88,90\n"
    )


def test_declared_charset_is_used():
    [table] = read_tables(Path(fixture("cp1252.html")).read_bytes())
    assert table.iloc[0, 0] == "Café – Renée"


def test_na_text_is_kept():
    [table] = read_tables(b"<table><tr><th>a</th><th>b</th></tr><tr><td>NA</td><td></td></tr></table>")
    assert table.to_csv(index=False) == "a,b\nNA,\n"


@pytest.mark.parametrize("xpath", ['//div[@id="prices"]', '//div[@id="prices"]/table'])
def test_xpath_selects_tables_at_or_under_it(tmp_path, xpath):
    assert main([fixture("page.html"), "-o", str(tmp_path), "--xpath", xpath]) == 0
    assert sorted(p.name for p in tmp_path.iterdir()) == ["table_1.csv"]
    assert (tmp_path / "table_1.csv").read_text().startswith("Fruit,Price\n")


def test_nested_tables_are_not_duplicated():
    html = b"<table><tr><td><table><tr><td>inner</td></tr></table></td></tr></table>"
    assert len(read_tables(html)) == 2
    assert len(read_tables(html, "//table")) == 2


@pytest.mark.parametrize(
    "args", [[fixture("no_tables.html")], [fixture("page.html"), "--xpath", '//div[@id="missing"]']]
)
def test_no_tables_exits_1(tmp_path, capsys, args):
    assert main([*args, "-o", str(tmp_path)]) == 1
    assert "no tables found" in capsys.readouterr().err
    assert list(tmp_path.iterdir()) == []


def test_missing_file_exits_2(capsys):
    assert main([fixture("nope.html")]) == 2
    assert "cannot read" in capsys.readouterr().err


def test_bad_xpath_exits_2(capsys):
    assert main([fixture("page.html"), "--xpath", "//["]) == 2
    assert "bad XPath" in capsys.readouterr().err


def test_empty_input_has_no_tables():
    assert read_tables(b"") == []


def test_url_uses_fetch(tmp_path):
    seen = []

    def fake_fetch(url):
        seen.append(url)
        return Path(fixture("page.html")).read_bytes()

    assert main(["https://example.test/fruit", "-o", str(tmp_path)], fetch=fake_fetch) == 0
    assert seen == ["https://example.test/fruit"]
    assert len(list(tmp_path.iterdir())) == 2


def test_stdin(monkeypatch):
    monkeypatch.setattr(sys, "stdin", io.TextIOWrapper(io.BytesIO(b"<table><tr><td>1</td></tr></table>")))
    assert read_source("-") == b"<table><tr><td>1</td></tr></table>"


@pytest.fixture
def server():
    """Serve tests/fixtures on 127.0.0.1 and record each request's User-Agent."""
    agents = []

    class Handler(http.server.SimpleHTTPRequestHandler):
        def do_GET(self):
            agents.append(self.headers["User-Agent"])
            super().do_GET()

        def log_message(self, *args):
            pass

    httpd = http.server.ThreadingHTTPServer(
        ("127.0.0.1", 0), functools.partial(Handler, directory=str(FIXTURES))
    )
    httpd.agents = agents
    threading.Thread(target=httpd.serve_forever, daemon=True).start()
    yield httpd
    httpd.shutdown()
    httpd.server_close()


def test_fetch_url_against_local_server(server):
    html = fetch_url(f"http://127.0.0.1:{server.server_port}/page.html")
    assert html == Path(fixture("page.html")).read_bytes()
    assert server.agents == [USER_AGENT]


def test_url_to_csvs_over_http(server, tmp_path, capsys):
    assert main([f"http://127.0.0.1:{server.server_port}/page.html", "-o", str(tmp_path)]) == 0
    assert capsys.readouterr().out.split() == [str(tmp_path / "table_1.csv"), str(tmp_path / "table_2.csv")]


def unused_port() -> int:
    with socket.socket() as sock:
        sock.bind(("127.0.0.1", 0))
        return sock.getsockname()[1]


@pytest.mark.parametrize(
    "url",
    [
        pytest.param("http://127.0.0.1:{port}/missing.html", id="http-404"),
        pytest.param("http://127.0.0.1:{closed}/page.html", id="connection-refused"),
    ],
)
def test_unreadable_url_exits_2(server, tmp_path, capsys, url):
    url = url.format(port=server.server_port, closed=unused_port())
    assert main([url, "-o", str(tmp_path)]) == 2
    assert f"cannot read {url}" in capsys.readouterr().err
    assert list(tmp_path.iterdir()) == []


def test_console_script(tmp_path):
    script = Path(sys.executable).with_name("parsers")
    result = subprocess.run(
        [str(script), fixture("page.html"), "-o", str(tmp_path)], capture_output=True, text=True, check=False
    )
    assert result.returncode == 0, result.stderr
    assert len(result.stdout.split()) == 2


def test_python_dash_m(tmp_path):
    result = subprocess.run(
        [sys.executable, "-m", "parsers", fixture("spans.html"), "-o", str(tmp_path)],
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, result.stderr
    assert (tmp_path / "table_1.csv").exists()
