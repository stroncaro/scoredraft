from enum import Enum
from typing import Tuple, List

from tkinter import HORIZONTAL, VERTICAL, Tk, Canvas
from tkinter import ttk

class SketchPad(Canvas):
    STATE = Enum('STATE', ['IDLE', 'DRAW', 'LINE', 'SCROLL'])
    ITEM_STYLE = {
        'width': 3,
        'fill': 'gray',
        'joinstyle': 'round',
        'capstyle': 'round',
    }

    def __init__(self, parent, **kwargs) -> None:
        super().__init__(parent, **kwargs)

        self._state: SketchPad.STATE = SketchPad.STATE.IDLE
        self._curr_xy: Tuple[int, int] = (0, 0)
        self._curr_item: int = 0
        self._items: List[int] = []

        # needed for drag scrolling to work
        self.configure(xscrollincrement=1, yscrollincrement=1)

        self.bind('<ButtonPress-1>', self._draw_init)
        self.bind('<B1-Motion>', self._draw_drag)
        self.bind('<ButtonRelease-1>', self._draw_end)

        self.bind('<ButtonPress-3>', self._scroll_init)
        self.bind('<B3-Motion>', self._scroll_drag)
        self.bind('<ButtonRelease-3>', self._scroll_end)

        self.bind('z', self._undo)
        self.focus_set()



    def _draw_init(self, event):
        if self._state != SketchPad.STATE.IDLE:
            return
        self._state = SketchPad.STATE.DRAW
        self._curr_xy = self._translate_xy(event)

    def _draw_drag(self, event):
        xy = self._translate_xy(event)
        match self._state:
            case SketchPad.STATE.DRAW:
                line_id = self.create_line(*self._curr_xy, *xy, **SketchPad.ITEM_STYLE)
                self._curr_item = line_id
                self._state = SketchPad.STATE.LINE
            case SketchPad.STATE.LINE:
                self.coords(self._curr_item, *self.coords(self._curr_item), *xy)
            case _:
                return
        self._curr_xy = xy

    def _draw_end(self, event):
        match self._state:
            case SketchPad.STATE.DRAW:
                x, y, w = *self._translate_xy(event), SketchPad.ITEM_STYLE['width']
                x1, y1, x2, y2 = x - w, y - w, x + w, y + w
                point_id = self.create_oval(x1, y1, x2, y2, fill=SketchPad.ITEM_STYLE['fill'])
                self._items.append(point_id)
            case SketchPad.STATE.LINE:
                self._items.append(self._curr_item)
            case _:
                return
        self._state = SketchPad.STATE.IDLE

    def _scroll_init(self, event):
        if self._state != SketchPad.STATE.IDLE:
            return
        self._state = SketchPad.STATE.SCROLL
        self._curr_xy = event.x, event.y
        # TODO: find way to use grabbing hand cursor
        self.config(cursor="hand1")

    def _scroll_drag(self, event):
        if self._state != SketchPad.STATE.SCROLL:
            return
        xy = event.x, event.y
        self.xview('scroll', self._curr_xy[0] - xy[0], 'unit')
        self.yview('scroll', self._curr_xy[1] - xy[1], 'unit')
        self._curr_xy = xy

    def _scroll_end(self, _):
        if self._state != SketchPad.STATE.SCROLL:
            return
        self._state = SketchPad.STATE.IDLE
        self.config(cursor="")


    def _translate_xy(self, event):
        return (self.canvasx(event.x), self.canvasy(event.y))

    def _undo(self, _):
        try:
            self.delete(self._items.pop())
        except IndexError:
            pass


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
