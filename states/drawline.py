from . import State

class DrawLineState(State):
    "User is drawing a line."
    def on_rmb_drag(self, event):
        xy = self._get_canvas_xy(event)
        self._sdc.extend_line(*xy)
        return self

    def on_rmb_release(self, event):
        from .idle import IdleState
        self._sdc.end_line()
        return self.transition_to(IdleState, event)
