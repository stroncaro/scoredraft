"""
Draw methods for the SDCanvas class.
"""
from typing import List

import tkinter as tk

from sdcanvas import STYLES
from sdcanvas.mixins import AreaMixin

class DrawMixin(AreaMixin, tk.Canvas):
    """Collection of draw methods for the SDCanvas class."""

    items: List[int] = []

    _active_line_id: int | None = None

    def draw_point(self, cx: float, cy: float, cr: float=2) -> None:
        """Draw a point following style guidelines."""

        x1, y1, x2, y2 = cx - cr, cy - cr, cx + cr, cy + cr
        oval_id = self.create_oval(x1, y1, x2, y2, **STYLES.OVAL)
        self.update_active_area_from_item(oval_id)
        self.items.append(oval_id)

    def draw_line(self, x1: float, y1: float, x2: float, y2: float, *args: float) -> None:
        """Create a line with all given points, following style guidelines."""
        line_id = self.create_line(x1, y1, x2, y2, *args, **STYLES.LINE)
        self.update_active_area_from_item(line_id)
        self.items.append(line_id)

    def start_line(self, x1: float, y1: float, x2: float, y2: float) -> None:
        """Initialize line segment, following style guidelines."""

        if self._active_line_id is not None:
            return

        self._active_line_id = self.create_line(x1, y1, x2, y2, **STYLES.LINE)

    def extend_line(self, *coords: float) -> None:
        """Add a segment to current line."""

        if self._active_line_id is None:
            return

        line_id = self._active_line_id
        self.coords(line_id, *self.coords(line_id), *coords)

    def end_line(self) -> None:
        """Finish drawing line, adding it to canvas items"""
        if self._active_line_id is None:
            return

        self.update_active_area_from_item(self._active_line_id)
        self.items.append(self._active_line_id)
        self._active_line_id = None

    def remove_last_item(self):
        """Remove the last created item from the canvas."""
        try:
            self.delete(self.items.pop())
        except IndexError:
            pass
