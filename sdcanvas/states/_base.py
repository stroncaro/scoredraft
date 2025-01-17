from __future__ import annotations
from typing import TYPE_CHECKING
from typing import Any, Optional, Tuple, Type

from abc import ABC
import tkinter as tk

if TYPE_CHECKING:
    from sdcanvas import SDCanvas

class SDCanvasState(ABC):
    "Base state machine class for SDCanvas input handling."
    _sdc: SDCanvas

    def __init__(self, canvas: SDCanvas, data: Optional[Any]=None) -> None:
        self._sdc = canvas
        self._data = data
        self.on_enter()

    def on_enter(self):
        "Invoked after entering state."

    def on_exit(self):
        "Invoked before exiting state."

    def on_rmb_press(self, event: tk.Event[SDCanvas]) -> SDCanvasState:
        "Override to handle right mouse button presses."
        return self

    def on_rmb_drag(self, event: tk.Event[SDCanvas]) -> SDCanvasState:
        "Override to handle right mouse button dragging."
        return self

    def on_rmb_release(self, event: tk.Event[SDCanvas]) -> SDCanvasState:
        "Override to handle right mouse button releases."
        return self

    def on_lmb_press(self, event: tk.Event[SDCanvas]) -> SDCanvasState:
        "Override to handle left mouse button presses."
        return self

    def on_lmb_drag(self, event: tk.Event[SDCanvas]) -> SDCanvasState:
        "Override to handle left mouse button dragging."
        return self

    def on_lmb_release(self, event: tk.Event[SDCanvas]) -> SDCanvasState:
        "Override to handle left mouse button releases."
        return self

    def on_key(self, event: tk.Event[SDCanvas]) -> SDCanvasState:
        "Override to handle key presses."
        return self

    def transition_to(self, cls: Type[SDCanvasState], data: Optional[Any]=None) -> SDCanvasState:
        "Return a new state, passing data if given."
        self.on_exit()
        return cls(self._sdc, data)

    def _get_xy_from_event(self, event: tk.Event[SDCanvas]) -> Tuple[int, int]:
        "Extract the x, y pair from the event and return it as absolute canvas coordinates."
        return (int(self._sdc.canvasx(event.x)), int(self._sdc.canvasy(event.y)))
