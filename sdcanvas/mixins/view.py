from typing import cast, Literal, Optional, Tuple, TypeVar

import tkinter as tk

ScrollAxis = TypeVar("ScrollAxis", Literal['x'], Literal['y'])
ScrollMethod = TypeVar("ScrollMethod", Literal['scroll'], Literal['moveto'])
ScrollUnit = TypeVar("ScrollUnit", Literal['units'], Literal['pages'])

class ViewMixin(tk.Canvas):
    """Track viewport position on the canvas."""
    _view_position: Tuple[float, float] = 0, 0

    @property
    def view_position(self) -> Tuple[float, float]:
        """Coordinates of the upper left point of the canvas view as an x, y pair."""
        return self._view_position

    @property
    def view_x(self) -> float:
        """Upper left x coordinate of the canvas view."""
        return self._view_position[0]

    @property
    def view_y(self) -> float:
        """Upper left y coordinate of the canvas view."""
        return self._view_position[1]

    def _set_view_x(self, val: float):
        self._view_position = val, self.view_y

    def _set_view_y(self, val: float):
        self._view_position = self.view_x, val

    @property
    def view_w(self) -> int:
        """Width of the canvas."""
        return self.winfo_width()

    @property
    def view_h(self) -> int:
        """Height of the canvas."""
        return self.winfo_height()

    @property
    def scrollregion_bounds_x(self) -> Tuple[float, float]:
        """Left and right bounds of the canvas scrollregion."""
        sr = self.cget('scrollregion').split()
        return float(sr[0]), float(sr[2])

    @property
    def scrollregion_bounds_y(self) -> Tuple[float, float]:
        """Top and bottom bounds of the canvas scrollregion."""
        sr = self.cget('scrollregion').split()
        return float(sr[1]), float(sr[3])

    def xview(self, *args):
        out = super().xview(*args)
        if len(args) >= 2:
            self._update_view_position('x', *args)
        return out

    def yview(self, *args):
        out = super().yview(*args)
        if len(args) >= 2:
            self._update_view_position('y', *args)
        return out

    def _update_view_position(
        self,
        axis: ScrollAxis,
        method: ScrollMethod,
        number: str,
        what: Optional[ScrollUnit]=None,
    ):
        n = float(number)
        pos = self.view_x if axis == 'x' else self.view_y

        # Calculate new position
        if method == 'scroll':
            # `what` is guaranteed to be 'units' or 'pages' if method is 'scroll'
            what = cast(ScrollUnit, what)
            pos += int(n * self._get_scroll_unit(axis, what))
        else:
            v1, v2 = self.scrollregion_bounds_x if axis == 'x' else self.scrollregion_bounds_y
            pos = int((v2 - v1) * n + v1)

        # Update axis position
        (self._set_view_x if axis == 'x' else self._set_view_y)(pos)

    def _get_scroll_unit(self, axis: ScrollAxis, what: ScrollUnit) -> float:
        size = self.view_w if axis == 'x' else self.view_h
        if what == 'pages':
            return size * 9 / 10

        inc = self.cget(axis + 'scrollincrement')
        if inc == "" or int(inc) <= 0:
            return size / 10

        return float(inc)
