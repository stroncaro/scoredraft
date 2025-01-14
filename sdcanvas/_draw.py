"""
Draw methods for the SDCanvas class.
"""

from __future__ import annotations
from typing import TYPE_CHECKING, cast

from itertools import islice
from typing import List, Optional

from . import _styles as STYLES


if TYPE_CHECKING:
    from tkinter import Canvas


class DrawMixin:
    """Collection of draw methods for the SDCanvas class."""

    active_area: List[float] = [float('inf'), float('inf'), float('-inf'), float('-inf')]
    items: List[int] = []

    _active_line_id: int | None = None

    def draw_point(self, cx: float, cy: float, cr: float=2) -> None:
        """Draw a point following style guidelines."""

        canvas = cast("Canvas", self)
        x1, y1, x2, y2 = cx - cr, cy - cr, cx + cr, cy + cr
        oval_id = canvas.create_oval(x1, y1, x2, y2, **STYLES.OVAL)
        self._update_active_area(x1, y1, x2, y2)
        self.items.append(oval_id)

    def start_line(self, x1: float, y1: float, x2: float, y2: float) -> None:
        """Initialize line segment, following style guidelines."""

        if self._active_line_id is not None:
            return

        canvas = cast("Canvas", self)
        self._active_line_id = canvas.create_line(x1, y1, x2, y2, **STYLES.LINE)

    def extend_line(self, *coords: float) -> None:
        """Add a segment to current line."""

        if self._active_line_id is None:
            return

        line_id = self._active_line_id
        canvas = cast("Canvas", self)
        canvas.coords(line_id, *canvas.coords(line_id), *coords)

    def end_line(self) -> None:
        """Finish drawing line, adding it to canvas items"""
        if self._active_line_id is None:
            return

        canvas = cast("Canvas", self)
        self._update_active_area(*canvas.coords(self._active_line_id))
        self.items.append(self._active_line_id)
        self._active_line_id = None

    def remove_last_item(self):
        """Remove the last created item from the canvas."""
        canvas = cast("Canvas", self)
        try:
            canvas.delete(self.items.pop())
        except IndexError:
            pass

    def _update_active_area(self, *coords: float):
        for x in islice(coords, 0, None, 2):
            self.active_area[0] = min(x, self.active_area[0])
            self.active_area[2] = max(x, self.active_area[2])
        for y in islice(coords, 1, None, 2):
            self.active_area[1] = min(y, self.active_area[1])
            self.active_area[3] = min(y, self.active_area[3])
        self._update_scrollregion()

    def _update_scrollregion(self, area: Optional[List[float]]=None):
        canvas = cast("Canvas", self)
        sr = canvas.cget('scrollregion')
        if not sr:
            return

        area = area or self.active_area
        new = tuple(n for n in area)
        old = tuple(float(n) for n in sr.split())

        new_sr = min(old[0], new[0]), min(old[1], new[1]), max(old[2], new[2]), max(old[3], new[3])
        canvas.config(scrollregion=new_sr)
