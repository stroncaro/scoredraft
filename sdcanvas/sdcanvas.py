from __future__ import annotations
from typing import List, Tuple

from dataclasses import dataclass
import tkinter as tk

from sdcanvas import STYLES
from sdcanvas.mixins import AreaMixin, BGMixin, DrawMixin, SVGMixin, ViewMixin
from sdcanvas.states import State, init_state_machine

@dataclass
class SubCanvasRegister:
    """Class for keeping track of a subcanvas on a canvas."""
    instance: SDCanvas
    id: int
    x1: float
    y1: float
    x2: float
    y2: float


class SDCanvas(SVGMixin, BGMixin, ViewMixin, DrawMixin, AreaMixin, tk.Canvas):
    "ScoreDraft canvas: Tk Canvas with custom functionality."

    _state: State
    _subcanvases: List[SubCanvasRegister]

    def __init__(self, parent, **kwargs) -> None:
        super().__init__(parent, **kwargs)

        self.configure(
            # needed for drag scrolling to work
            xscrollincrement=1, yscrollincrement=1,
            # allow going out of scrollregion
            confine=False,
        )

        self._subcanvases = []

        self.set_background_tile('backgrounds/paper5_1.png')

        self._state = init_state_machine(self)
        self.bind('<ButtonPress-1>', self._on_rmb_press)
        self.bind('<B1-Motion>', self._on_rmb_drag)
        self.bind('<ButtonRelease-1>', self._on_rmb_release)
        self.bind('<ButtonPress-3>', self._on_lmb_press)
        self.bind('<B3-Motion>', self._on_lmb_drag)
        self.bind('<ButtonRelease-3>', self._on_lmb_release)
        self.bind('<Key>', self._on_key)

        self.focus_set()

    def create_subcanvas(self, x: float, y: float, w: float, h: float) -> None:
        "Initialize a SDCanvas child on the canvas."
        _, x, y, parent = self._get_sc_chain(x, y)[-1]

        subcanvas = SDCanvas(parent, **STYLES.SUBCANVAS)
        subcanvas_id = parent.create_window(x, y, width=w, height=h, window=subcanvas, anchor='nw')
        parent._subcanvases.append(SubCanvasRegister(subcanvas, subcanvas_id, x, y, x+w, y+h))

    def canvas_instance_on_xy(self, x: float, y: float) -> SDCanvas:
        "Get the active subcanvas on coordinates x, y."
        return self._get_sc_chain(x, y)[-1][3]

    def delete_subcanvas_on_xy(self, x: float, y: float) -> None:
        "Delete a subcanvas on coordinates x, y."
        chain = self._get_sc_chain(x, y)
        if len(chain) > 1:
            parent = chain[-2][3]
            child_id = chain[-1][0]
            parent.delete(child_id)

    def _get_sc_chain(self, x: float, y: float, self_id: int = -1) -> List[Tuple[int, float, float, SDCanvas]]:
        """
        Get canvas instances, from outer to inner, that are on coordinates x,y, with their item ids.
        Id of -1 is the parent of the chain.
        """
        chain: List[Tuple[int, float, float, SDCanvas]] = [(self_id, x, y, self)]
        for sc in self._subcanvases:
            if sc.x1 <= x <= sc.x2 and sc.y1 <= y <= sc.y2:
                sub_chain = sc.instance._get_sc_chain(x - sc.x1, y - sc.y1, sc.id)
                chain = chain + sub_chain
                break
        return chain


    def _on_rmb_press(self, event):
        self._state = self._state.on_rmb_press(event)

    def _on_rmb_drag(self, event):
        self._state = self._state.on_rmb_drag(event)

    def _on_rmb_release(self, event):
        self._state = self._state.on_rmb_release(event)

    def _on_lmb_press(self, event):
        self._state = self._state.on_lmb_press(event)

    def _on_lmb_drag(self, event):
        self._state = self._state.on_lmb_drag(event)

    def _on_lmb_release(self, event):
        self._state = self._state.on_lmb_release(event)

    def _on_key(self, event):
        self._state = self._state.on_key(event)
