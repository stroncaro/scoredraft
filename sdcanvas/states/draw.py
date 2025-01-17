from __future__ import annotations
from typing import Tuple

from sdcanvas.states import State

class DrawState(State):
    _data: Tuple[int, int]

    def on_rmb_drag(self, event):
        from sdcanvas.states.drawline import DrawLineState
        xy = self._get_xy_from_event(event)
        self._sdc.start_line(*self._data, *xy)
        return self.transition_to(DrawLineState)

    def on_rmb_release(self, event):
        from sdcanvas.states.idle import IdleState
        xy = self._get_xy_from_event(event)
        self._sdc.draw_point(*xy)
        return self.transition_to(IdleState)
