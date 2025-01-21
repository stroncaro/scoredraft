from typing import Tuple

from . import State

class DrawState(State):
    "User is drawing. Depending on following input, result could be a point or a line."
    _xy: Tuple[int, int]

    def on_enter(self, event, data=None):
        self._xy = self._get_canvas_xy(event)

    def on_rmb_drag(self, event):
        from .drawline import DrawLineState
        xy = self._get_canvas_xy(event)
        self._sdc.start_line(*self._xy, *xy)
        return self.transition_to(DrawLineState, event)

    def on_rmb_release(self, event):
        from .idle import IdleState
        xy = self._get_canvas_xy(event)
        self._sdc.draw_point(*xy)
        return self.transition_to(IdleState, event)
