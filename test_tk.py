from enum import Enum
from typing import Tuple, List, Optional

from tkinter import HORIZONTAL, VERTICAL, Tk, Canvas, N, W, S, E
from tkinter import ttk

class SketchPad(Canvas):

    State = Enum('State', ['IDLE', 'DRAW', 'LINE', 'SCROLL'])

    def __init__(self, parent, **kwargs) -> None:
        super().__init__(parent, **kwargs)

        self._state: SketchPad.State = SketchPad.State.IDLE

        self._current_coords: Tuple[int, int] = (0, 0)
        self._current_line: int = 0
        self._lines: List[int] = []

        self._line_style = {
            'width': 3,
            'fill': 'gray',
            'joinstyle': 'round',
            'capstyle': 'round',
        }

        # needed for drag scrolling to work
        self.configure(xscrollincrement=1, yscrollincrement=1)

        self.bind('<ButtonPress-1>', self._draw_init)
        self.bind('<B1-Motion>', self._draw_drag)
        self.bind('<ButtonRelease-1>', self._draw_end)

        self.bind('<ButtonPress-3>', self._scroll_init)
        self.bind('<B3-Motion>', self._scroll_drag)
        self.bind('<ButtonRelease-3>', self._scroll_end)

        parent.bind('z', self._undo)

    def _draw_init(self, event):
        if self._state != SketchPad.State.IDLE:
            return
        self._state = SketchPad.State.DRAW
        self._current_coords = self._translate_xy(event)

    def _draw_drag(self, event):
        xy = self._translate_xy(event)
        match self._state:
            case SketchPad.State.DRAW:
                line_id = self.create_line(*self._current_coords, *xy, **self._line_style)
                self._current_line = line_id
                self._state = SketchPad.State.LINE
            case SketchPad.State.LINE:
                self.coords(self._current_line, *self.coords(self._current_line), *xy)
            case _:
                return
        self._current_coords = xy

    def _draw_end(self, _):
        match self._state:
            case SketchPad.State.DRAW:
                pass
            case SketchPad.State.LINE:
                self._lines.append(self._current_line)
            case _:
                return
        self._state = SketchPad.State.IDLE

    def _scroll_init(self, event):
        if self._state != SketchPad.State.IDLE:
            return
        self._state = SketchPad.State.SCROLL
        self._current_coords = event.x, event.y
        # TODO: find way to use grabbing hand cursor
        self.config(cursor="hand1")

    def _scroll_drag(self, event):
        if self._state != SketchPad.State.SCROLL:
            return
        xy = event.x, event.y
        self.xview('scroll', self._current_coords[0] - xy[0], 'unit')
        self.yview('scroll', self._current_coords[1] - xy[1], 'unit')
        self._current_coords = xy

    def _scroll_end(self, _):
        if self._state != SketchPad.State.SCROLL:
            return
        self._state = SketchPad.State.IDLE
        self.config(cursor="")


    def _translate_xy(self, event):
        return (self.canvasx(event.x), self.canvasy(event.y))

    def _undo(self, _):
        try:
            self.delete(self._lines.pop())
        except IndexError:
            pass

# Mouse
# canvas.bind('<ButtonPress-1>', print)
# canvas.bind('<B1-Motion>', print)
# canvas.bind('<ButtonPress-3>', print)
# canvas.bind('<B3-Motion>', print)
# canvas.bind('<MouseWheel>', print)

# Keys
# canvas.bind('<KeyPress-z>', print)
# canvas.bind('<KeyPress-x>', print)

# Resize (also triggers on canvas creation)
# canvas.bind('<Configure>', print)


if __name__ == "__main__":

    root = Tk()
    root.title('Paint')
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)

    fr = ttk.Frame(root, width=800, height=600)
    fr.grid(column=0, row=0, sticky='nwse')
    fr.grid_columnconfigure(0, weight=1)
    fr.grid_rowconfigure(0, weight=1)

    sp = SketchPad(fr, scrollregion=(0, 0, 1000, 1000), background='black')
    sx = ttk.Scrollbar(fr, orient=HORIZONTAL, command=sp.xview)
    sy = ttk.Scrollbar(fr, orient=VERTICAL, command=sp.yview)
    sp.configure(xscrollcommand=sx.set, yscrollcommand=sy.set)

    sp.grid(column=0, row=0, sticky='nwse')
    sx.grid(column=0, row=1, sticky='we')
    sy.grid(column=1, row=0, sticky='ns')

    root.mainloop()
