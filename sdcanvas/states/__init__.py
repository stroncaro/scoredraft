from __future__ import annotations
from typing import TYPE_CHECKING

from ._base import SDCanvasState as State

if TYPE_CHECKING:
    from sdcanvas.sdcanvas import SDCanvas

def init_state_machine(sdc: SDCanvas) -> State:
    "Initialize SDCanvas state machine."
    from .idle import IdleState
    return IdleState(sdc, None) # type: ignore
