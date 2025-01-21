from __future__ import annotations
from typing import Any, List

from tkinter import Tk, HORIZONTAL, VERTICAL
from tkinter import ttk

from sdcanvas import SDCanvas
from states import State, init_state_machine

# TODO: find how to run many concurrent windows in a nonblocking manner.

class SDWindow(Tk):
    """Main ScoreDraft window"""

    _canvas: SDCanvas
    _state: State
    _bypass_click_widgets: List[Any]

    def __init__(self) -> None:
        super().__init__()
        self.title('ScoreDraft')
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        fr = ttk.Frame(self, width=800, height=600)
        fr.grid(column=0, row=0, sticky='nwse')
        fr.grid_columnconfigure(0, weight=1)
        fr.grid_rowconfigure(0, weight=1)

        canvas = SDCanvas(fr, scrollregion=(0, 0, 400, 400))
        sx = ttk.Scrollbar(fr, orient=HORIZONTAL, command=canvas.xview)
        sy = ttk.Scrollbar(fr, orient=VERTICAL, command=canvas.yview)
        canvas.configure(xscrollcommand=sx.set, yscrollcommand=sy.set)

        self._bypass_click_widgets = [sx, sy]

        canvas.grid(column=0, row=0, sticky='nwse')
        sx.grid(column=0, row=1, sticky='we')
        sy.grid(column=1, row=0, sticky='ns')

        canvas.create_subcanvas(0, 0, 100, 100)
        canvas.create_subcanvas(20, 20, 50, 50)

        self._state = init_state_machine(canvas)
        self.bind('<ButtonPress-1>', self._on_rmb_press)
        self.bind('<B1-Motion>', self._on_rmb_drag)
        self.bind('<ButtonRelease-1>', self._on_rmb_release)
        self.bind('<ButtonPress-3>', self._on_lmb_press)
        self.bind('<B3-Motion>', self._on_lmb_drag)
        self.bind('<ButtonRelease-3>', self._on_lmb_release)
        self.bind('<Key>', self._on_key)
        self.focus_set()

        self._canvas = canvas

    def _on_rmb_press(self, event):
        if event.widget in self._bypass_click_widgets:
            return
        self._state = self._state.on_rmb_press(event)

    def _on_rmb_drag(self, event):
        self._state = self._state.on_rmb_drag(event)

    def _on_rmb_release(self, event):
        self._state = self._state.on_rmb_release(event)

    def _on_lmb_press(self, event):
        if event.widget in self._bypass_click_widgets:
            return
        self._state = self._state.on_lmb_press(event)

    def _on_lmb_drag(self, event):
        self._state = self._state.on_lmb_drag(event)

    def _on_lmb_release(self, event):
        self._state = self._state.on_lmb_release(event)

    def _on_key(self, event):
        self._state = self._state.on_key(event)

if __name__ == "__main__":
    sd = SDWindow()
    sd.mainloop()
