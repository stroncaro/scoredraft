from __future__ import annotations
from typing import List, Tuple

from dataclasses import dataclass
import tkinter as tk

from sdcanvas import STYLES
from sdcanvas.mixins import AreaMixin, BGMixin, DrawMixin, SVGMixin, ViewMixin

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

    _subcanvases: List[SubCanvasRegister]
    _master_offset_x: float
    _master_offset_y: float
    _boundary_w: float
    _boundary_h: float

    def __init__(self, parent, master_x: float = 0, master_y: float = 0, **kwargs) -> None:
        super().__init__(parent, **kwargs)

        self._subcanvases = []

        # TODO: rework rmb scrolling so that these are not needed
        self.configure(xscrollincrement=1, yscrollincrement=1)

        self._master_offset_x = master_x
        self._master_offset_y = master_y

        self._boundary_w = kwargs.get('width', -1)
        self._boundary_h = kwargs.get('height', -1)
        if self._boundary_w == -1 and self._boundary_h == -1:
            self.configure(confine=False)

        self.set_background_tile('backgrounds/paper5_1.png')

    @property
    def master_offset_x(self) -> float:
        "X location of this canvas on the master canvas."
        return self._master_offset_x

    @property
    def master_offset_y(self) -> float:
        "Y location of this canvas on the master canvas."
        return self._master_offset_y

    @property
    def boundary_w(self) -> float:
        "Usable width of this canvas, -1 if infinite."
        return self._boundary_w

    @property
    def boundary_h(self) -> float:
        "Usable height of this canvas, -1 if infinite."
        return self._boundary_h

    def create_subcanvas(self, master_x: float, master_y: float, w: float, h: float) -> None:
        "Initialize a SDCanvas child on the canvas."
        _, px, py, parent = self._get_sc_chain(master_x, master_y)[-1]

        subcanvas = SDCanvas(parent, master_x, master_y, width=w, height=h, **STYLES.SUBCANVAS)
        subcanvas_id = parent.create_window(px, py, width=w, height=h, window=subcanvas, anchor='nw')
        parent._subcanvases.append(SubCanvasRegister(subcanvas, subcanvas_id, px, py, px+w, py+h))

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
