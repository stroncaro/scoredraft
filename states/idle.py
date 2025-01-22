from . import State

class IdleState(State):
    "Waiting for input."
    def on_rmb_press(self, event):
        if self._ctrl_pressed(event):
            from .drawsubcanvas import DrawSubcanvasState as Next
        else:
            from .draw import DrawState as Next
        return self.transition_to(Next, event)

    def on_lmb_press(self, event):
        from .scroll import ScrollState
        return self.transition_to(ScrollState, event)

    def on_key(self, event):
        match event.keysym:
            case 'z':
                self._sdc.remove_last_item()
            case 'l':
                self._sdc.load('test.svg')
            case 's':
                self._sdc.save('test.svg')
        return self
