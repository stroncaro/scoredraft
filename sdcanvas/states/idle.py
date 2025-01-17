from sdcanvas.states import State

class IdleState(State):
    def on_rmb_press(self, event):
        from sdcanvas.states.draw import DrawState
        return self.transition_to(DrawState, event)

    def on_lmb_press(self, event):
        from sdcanvas.states.scroll import ScrollState
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
