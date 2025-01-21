from __future__ import annotations
from typing import Tuple, TYPE_CHECKING

from . import State

if TYPE_CHECKING:
    from sdcanvas import SDCanvas

class DrawLineState(State):
    "User is drawing a line."

    _target: SDCanvas

    def on_enter(self, event, data: SDCanvas) -> None:
        self._target = data

    def on_rmb_drag(self, event):
        xy = self._get_target_xy(event)
        self._target.extend_line(*xy)
        return self

    def on_rmb_release(self, event):
        from .idle import IdleState
        self._target.end_line()
        return self.transition_to(IdleState, event)

    def _get_target_xy(self, event) -> Tuple[float, float]:
        abs_x, abs_y = self._get_master_canvas_xy(event)
        return abs_x - self._target.master_offset_x, abs_y - self._target.master_offset_y
