from typing import Tuple

from . import State

class ScrollState(State):
    "User is scrolling the view with the mouse."
    _xy: Tuple[int, int]

    def on_enter(self, event, data=None):
        self._xy = event.x, event.y
        self._sdc.config(cursor="hand1")

    def on_exit(self):
        self._sdc.config(cursor="")

    def on_lmb_drag(self, event):
        x1, y1 = self._xy
        x2, y2 = event.x, event.y
        x_units = x1 - x2
        y_units = y1 - y2
        if x_units != 0:
            self._sdc.xview('scroll', str(x_units), 'units')
        if y_units != 0:
            self._sdc.yview('scroll', str(y_units), 'units')
        self._xy = x2, y2
        return self

    def on_lmb_release(self, event):
        from .idle import IdleState
        return self.transition_to(IdleState, event)
