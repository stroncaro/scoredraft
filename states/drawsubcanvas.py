from __future__ import annotations
from typing import Tuple, TYPE_CHECKING

from . import State

if TYPE_CHECKING:
    from sdcanvas.sdcanvas import SDCanvas

class DrawSubcanvasState(State):

    _target: SDCanvas
    _initial_xy: Tuple[float, float]

    def on_enter(self, event, data=None) -> None:
        xy = self._get_target_xy(event, initialize_target=True)
        self._target.start_rect(*xy)
        self._initial_xy = xy

    def on_rmb_drag(self, event) -> State:
        self._target.resize_rect(*self._get_coords(event))
        return self

    def on_rmb_release(self, event) -> State:
        self._target.remove_temporary_item()

        x1, y1, x2, y2 = self._get_coords(event)
        subc_abs_x = x1 + self._target.master_offset_x
        subc_abs_y = y1 + self._target.master_offset_y
        subc_width = x2 - x1
        subc_height = y2 - y1
        self._sdc.create_subcanvas(subc_abs_x, subc_abs_y, subc_width, subc_height)

        from .idle import IdleState
        return self.transition_to(IdleState, event)

    def _get_target_xy(self, event, *, initialize_target=False) -> Tuple[float, float]:
        abs_x, abs_y = self._get_master_canvas_xy(event)

        if initialize_target:
            self._target = self._sdc.canvas_instance_on_xy(abs_x, abs_y)

        return abs_x - self._target.master_offset_x, abs_y - self._target.master_offset_y

    def _get_coords(self, event) -> Tuple[float, float, float, float]:
        x2, y2 = self._get_target_xy(event)
        x1, y1 = self._initial_xy
        if x2 < x1:
            x1, x2 = x2, x1
        if y2 < y1:
            y1, y2 = y2, y1
        return x1, y1, x2, y2
