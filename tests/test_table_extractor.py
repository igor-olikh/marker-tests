"""Tests for the HTML table extractor."""

from table_extractor import extract_tables_from_html


def test_extract_single_table() -> None:
    html = (
        "<table><tr><th>A</th><th>B</th></tr>"
        "<tr><td>1</td><td>2</td></tr>"
        "<tr><td>3</td><td>4</td></tr></table>"
    )
    assert extract_tables_from_html(html) == [[["A", "B"], ["1", "2"], ["3", "4"]]]


def test_extract_multiple_tables() -> None:
    html = (
        "<table><tr><td>a</td></tr></table>"
        "<p>text between</p>"
        "<table><tr><td>b</td></tr></table>"
    )
    assert extract_tables_from_html(html) == [[["a"]], [["b"]]]
