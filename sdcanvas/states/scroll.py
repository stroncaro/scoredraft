from __future__ import annotations
from typing import TYPE_CHECKING

from sdcanvas.states import State

if TYPE_CHECKING:
    import tkinter as tk
    from sdcanvas.sdcanvas import SDCanvas

class ScrollState(State):
    _data: tk.Event[SDCanvas]

    def on_enter(self):
        self._sdc.config(cursor="hand1")

    def on_exit(self):
        self._sdc.config(cursor="")

    def on_lmb_drag(self, event):
        x1, y1 = self._data.x, self._data.y
        x2, y2 = event.x, event.y
        x_units = x1 - x2
        y_units = y1 - y2
        if x_units != 0:
            self._sdc.xview('scroll', str(x_units), 'units')
        if y_units != 0:
            self._sdc.yview('scroll', str(y_units), 'units')
        self._data = event
        return self

    def on_lmb_release(self, event):
        from sdcanvas.states.idle import IdleState
        return self.transition_to(IdleState)
