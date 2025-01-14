from __future__ import annotations
from typing import TYPE_CHECKING, cast


if TYPE_CHECKING:
    from tkinter import Canvas
    from sdcanvas._area import AreaMixin


class UseCanvas:
    @property
    def _canvas(self):
        return cast("Canvas", self)

class UseArea:
    @property
    def _area(self):
        return cast("AreaMixin", self)
