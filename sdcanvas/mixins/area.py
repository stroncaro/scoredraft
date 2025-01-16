"""
Active area tracking for the SDCanvas class.
"""
from typing import List, Optional, Tuple

from itertools import chain, islice
import tkinter as tk

class AreaMixin(tk.Canvas):
    """Keeps track of and updates active area (area where there are elements)"""

    active_area: List[float] = [float('inf'), float('inf'), float('-inf'), float('-inf')]

    @property
    def active_area_position(self) -> Tuple[float, float]:
        """Coordinates of the upper left point of the active area of the canvas as an x, y pair."""
        return self.active_area[0], self.active_area[1]

    @property
    def active_area_x(self) -> float:
        """Upper left x coordinate of the canvas active area."""
        return self.active_area[0]

    @property
    def active_area_y(self) -> float:
        """Upper left y coordinate of the canvas active area."""
        return self.active_area[1]

    @property
    def active_area_size(self) -> Tuple[float, float]:
        """Size tuple of the active area."""
        return self.active_area_w, self.active_area_h

    @property
    def active_area_w(self) -> float:
        """Width of the active area."""
        return self.active_area[2] - self.active_area[0]

    @property
    def active_area_h(self) -> float:
        """Heigth of the active area."""
        return self.active_area[3] - self.active_area[1]

    def reset_active_area(self):
        """Reset the active area to empty."""
        self.active_area = [float('inf'), float('inf'), float('-inf'), float('-inf')]

    def update_active_area(self, *coords: float):
        """Grow active area to hold given x, y pairs, if necessary."""
        for x in islice(coords, 0, None, 2):
            self.active_area[0] = min(x, self.active_area[0])
            self.active_area[2] = max(x, self.active_area[2])
        for y in islice(coords, 1, None, 2):
            self.active_area[1] = min(y, self.active_area[1])
            self.active_area[3] = max(y, self.active_area[3])
        self._update_scrollregion()

    def update_active_area_from_item(self, item_id: int):
        """Grow active area to hold item, if necessary."""
        coords = self.coords(item_id)
        self.update_active_area(*coords)

    def update_active_area_from_all_items(self, items: List[int]):
        """Grow active area to hold all items in the canvas."""
        coords = chain(*(self.coords(item) for item in items))
        self.reset_active_area()
        self.update_active_area(*coords)

    def _update_scrollregion(self, area: Optional[List[float]]=None):
        sr = self.cget('scrollregion')
        if not sr:
            return

        area = area or self.active_area
        new = tuple(n for n in area)
        old = tuple(float(n) for n in sr.split())

        new_sr = min(old[0], new[0]), min(old[1], new[1]), max(old[2], new[2]), max(old[3], new[3])
        self.config(scrollregion=new_sr)
