"""
Draw methods for the SDCanvas class.
"""

from __future__ import annotations
from typing import TYPE_CHECKING, cast

from . import _styles as STYLES


if TYPE_CHECKING:
    from tkinter import Canvas


class DrawMixin:
    """Collection of draw methods for the SDCanvas class."""

    def draw_point(self, cx: float, cy: float, cr: float=2) -> int:
        """Draw a point following style guidelines."""
        canvas = cast("Canvas", self)
        x1, y1, x2, y2 = cx - cr, cy - cr, cx + cr, cy + cr
        return canvas.create_oval(x1, y1, x2, y2, **STYLES.OVAL)

    def draw_line(self, x1: float, y1: float, x2: float, y2: float) -> int:
        """Draw a line following style guidelines."""
        canvas = cast("Canvas", self)
        return canvas.create_line(x1, y1, x2, y2, **STYLES.LINE)

    def extend_line(self, line_id: int, *coords: float) -> None:
        """Extend an already drawn line"""
        canvas = cast("Canvas", self)
        canvas.coords(line_id, *canvas.coords(line_id), *coords)
