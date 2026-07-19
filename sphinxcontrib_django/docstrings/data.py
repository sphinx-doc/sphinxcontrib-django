from __future__ import annotations

import io
import sys

from pprintpp import pprint as pp


def improve_data_docstring(data: object, lines: list[str]) -> None:
    """
    Improve the documentation of data by pretty-printing into in the docstring.

    :param data: The documented object
    :param lines: The lines of docstring lines
    """
    if isinstance(data, (list, tuple, dict, set)):
        # Redirect stdout to StringIO to catch print
        old_stdout = sys.stdout
        new_stdout = io.StringIO()
        sys.stdout = new_stdout

        # Pretty print iterable
        pp(data)
        output = new_stdout.getvalue()

        # Append pretty printed lines
        lines.append(".. code-block:: JavaScript")
        lines.append("")
        lines.append("    " + output)

        # Reset stdout
        sys.stdout = old_stdout
