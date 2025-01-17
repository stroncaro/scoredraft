from __future__ import annotations

import tkinter as tk

from sdcanvas.mixins import AreaMixin, BGMixin, DrawMixin, SVGMixin, ViewMixin
from sdcanvas.states.idle import IdleState

class SDCanvas(SVGMixin, BGMixin, ViewMixin, DrawMixin, AreaMixin, tk.Canvas):

    def __init__(self, parent, **kwargs) -> None:
        super().__init__(parent, **kwargs)

        self.configure(
            # needed for drag scrolling to work
            xscrollincrement=1, yscrollincrement=1,
            # allow going out of scrollregion
            confine=False,
        )

        self.set_background_tile('backgrounds/paper5_1.png')

        self.state = IdleState(self)
        self.bind('<ButtonPress-1>', self.on_rmb_press)
        self.bind('<B1-Motion>', self.on_rmb_drag)
        self.bind('<ButtonRelease-1>', self.on_rmb_release)
        self.bind('<ButtonPress-3>', self.on_lmb_press)
        self.bind('<B3-Motion>', self.on_lmb_drag)
        self.bind('<ButtonRelease-3>', self.on_lmb_release)
        self.bind('<Key>', self.on_key)

        self.focus_set()

    def on_rmb_press(self, event):
        self.state = self.state.on_rmb_press(event)

    def on_rmb_drag(self, event):
        self.state = self.state.on_rmb_drag(event)

    def on_rmb_release(self, event):
        self.state = self.state.on_rmb_release(event)

    def on_lmb_press(self, event):
        self.state = self.state.on_lmb_press(event)

    def on_lmb_drag(self, event):
        self.state = self.state.on_lmb_drag(event)

    def on_lmb_release(self, event):
        self.state = self.state.on_lmb_release(event)

    def on_key(self, event):
        self.state = self.state.on_key(event)
