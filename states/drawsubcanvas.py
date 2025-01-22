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
        xy = self._get_target_xy(event)
        self._target.resize_rect(*xy)
        return self

    def on_rmb_release(self, event) -> State:
        self._target.remove_temporary_item()
        from .idle import IdleState
        return self.transition_to(IdleState, event)

    def _get_target_xy(self, event, *, initialize_target=False) -> Tuple[float, float]:
        abs_x, abs_y = self._get_master_canvas_xy(event)

        if initialize_target:
            self._target = self._sdc.canvas_instance_on_xy(abs_x, abs_y)

        return abs_x - self._target.master_offset_x, abs_y - self._target.master_offset_y
