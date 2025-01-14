"""
Draw methods for the SDCanvas class.
"""

from typing import List

from sdcanvas import STYLES
from ._uses import UseArea, UseCanvas

class DrawMixin(UseArea, UseCanvas):
    """Collection of draw methods for the SDCanvas class."""

    items: List[int] = []

    _active_line_id: int | None = None

    def draw_point(self, cx: float, cy: float, cr: float=2) -> None:
        """Draw a point following style guidelines."""

        x1, y1, x2, y2 = cx - cr, cy - cr, cx + cr, cy + cr
        oval_id = self._canvas.create_oval(x1, y1, x2, y2, **STYLES.OVAL)
        self._area.update_active_area_from_item(oval_id)
        self.items.append(oval_id)

    def start_line(self, x1: float, y1: float, x2: float, y2: float) -> None:
        """Initialize line segment, following style guidelines."""

        if self._active_line_id is not None:
            return

        self._active_line_id = self._canvas.create_line(x1, y1, x2, y2, **STYLES.LINE)

    def extend_line(self, *coords: float) -> None:
        """Add a segment to current line."""

        if self._active_line_id is None:
            return

        line_id = self._active_line_id
        self._canvas.coords(line_id, *self._canvas.coords(line_id), *coords)

    def end_line(self) -> None:
        """Finish drawing line, adding it to canvas items"""
        if self._active_line_id is None:
            return

        self._area.update_active_area_from_item(self._active_line_id)
        self.items.append(self._active_line_id)
        self._active_line_id = None

    def remove_last_item(self):
        """Remove the last created item from the canvas."""
        try:
            self._canvas.delete(self.items.pop())
        except IndexError:
            pass
