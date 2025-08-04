"""HTML table extraction utilities.

This module provides a lightweight HTML table extractor that does not rely on
external dependencies. It parses the HTML structure and returns table data as
lists of rows and cells.
"""

from __future__ import annotations

from html.parser import HTMLParser
from typing import List


class _TableHTMLParser(HTMLParser):
    """Parse HTML tables into Python data structures.

    The parser builds a list of tables where each table is a list of rows and
    each row is a list of cell values (strings). It ignores any nested tables
    and non-text content inside cells.
    """

    def __init__(self) -> None:
        super().__init__()
        self.tables: List[List[List[str]]] = []
        self._current_table: List[List[str]] | None = None
        self._current_row: List[str] | None = None
        self._current_cell: List[str] | None = None

    # -- Handlers ---------------------------------------------------------
    def handle_starttag(self, tag: str, attrs) -> None:  # noqa: ANN001 - attrs
        if tag == "table":
            self._current_table = []
        elif tag == "tr" and self._current_table is not None:
            self._current_row = []
        elif tag in {"td", "th"} and self._current_row is not None:
            self._current_cell = []

    def handle_endtag(self, tag: str) -> None:
        if tag == "table":
            if self._current_table is not None:
                self.tables.append(self._current_table)
            self._current_table = None
        elif tag == "tr":
            if self._current_table is not None and self._current_row is not None:
                self._current_table.append(self._current_row)
            self._current_row = None
        elif tag in {"td", "th"}:
            if self._current_row is not None and self._current_cell is not None:
                cell_text = "".join(self._current_cell).strip()
                self._current_row.append(cell_text)
            self._current_cell = None

    def handle_data(self, data: str) -> None:
        if self._current_cell is not None:
            self._current_cell.append(data)


def extract_tables_from_html(html: str) -> List[List[List[str]]]:
    """Extract tables from an HTML document.

    Parameters
    ----------
    html:
        The HTML content to parse.

    Returns
    -------
    list of tables
        A list where each element represents a table. Each table is a list of
        rows, and each row is a list of cell strings.
    """

    parser = _TableHTMLParser()
    parser.feed(html)
    return parser.tables
