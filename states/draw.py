from __future__ import annotations
from typing import Tuple, TYPE_CHECKING

from . import State

if TYPE_CHECKING:
    from sdcanvas import SDCanvas

class DrawState(State):
    "User is drawing. Depending on following input, result could be a point or a line."
    _xy: Tuple[float, float]
    _target: SDCanvas

    def on_enter(self, event, data=None):
        self._xy = self._get_target_xy(event, initialize_target=True)
        self._sdc.draw_point(*self._xy, temporary=True)

    def on_rmb_drag(self, event):
        self._sdc.remove_temporary_item()
        xy = self._get_target_xy(event)
        self._target.start_line(*self._xy, *xy)

        from .drawline import DrawLineState
        return self.transition_to(DrawLineState, event, data=self._target)

    def on_rmb_release(self, event):
        self._sdc.add_temporary_item()

        from .idle import IdleState
        return self.transition_to(IdleState, event)

    def _get_target_xy(self, event, *, initialize_target=False) -> Tuple[float, float]:
        abs_x, abs_y = self._get_master_canvas_xy(event)

        if initialize_target:
            self._target = self._sdc.canvas_instance_on_xy(abs_x, abs_y)

        return abs_x - self._target.master_offset_x, abs_y - self._target.master_offset_y
