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

    def __init__(self, canvas: SDCanvas, event: tk.Event, data: Optional[Any] = None) -> None:
        self._sdc = canvas
        self.on_enter(event, data)

    def on_enter(self, event: tk.Event, data: Optional[Any] = None) -> None:
        "Invoked after entering state. Override to add functionality."

    def on_exit(self) -> None:
        "Invoked before exiting state. Override to add functionality."

    def on_rmb_press(self, event: tk.Event) -> SDCanvasState:
        "Override to handle right mouse button presses."
        return self

    def on_rmb_drag(self, event: tk.Event) -> SDCanvasState:
        "Override to handle right mouse button dragging."
        return self

    def on_rmb_release(self, event: tk.Event) -> SDCanvasState:
        "Override to handle right mouse button releases."
        return self

    def on_lmb_press(self, event: tk.Event) -> SDCanvasState:
        "Override to handle left mouse button presses."
        return self

    def on_lmb_drag(self, event: tk.Event) -> SDCanvasState:
        "Override to handle left mouse button dragging."
        return self

    def on_lmb_release(self, event: tk.Event) -> SDCanvasState:
        "Override to handle left mouse button releases."
        return self

    def on_key(self, event: tk.Event) -> SDCanvasState:
        "Override to handle key presses."
        return self

    def transition_to(
        self,
        state: Type[SDCanvasState],
        event: tk.Event,
        data: Optional[Any] = None
    ) -> SDCanvasState:
        "Return a new state. Pass event that triggered the change, and extra data (if given)."
        self.on_exit()
        return state(self._sdc, event, data)

    def _get_canvas_xy(self, event: tk.Event) -> Tuple[int, int]:
        "Extract the x, y pair from the event and return it as absolute canvas coordinates."
        x = event.x_root - self._sdc.winfo_rootx()
        y = event.y_root - self._sdc.winfo_rooty()
        x = self._sdc.canvasx(x)
        y = self._sdc.canvasy(y)
        return (int(x), int(y))
