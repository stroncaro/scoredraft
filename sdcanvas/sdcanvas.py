from enum import Enum
from tkinter import Canvas
from typing import Tuple

from sdcanvas import STYLES
from sdcanvas.mixins import AreaMixin, BGMixin, DrawMixin, SVGMixin, ViewMixin

# TODO: refactor state handling and other components into encapsulated parts.
# Tkinter virtual events can help with decoupling, but a complete rework is needed
# Current implementation is fine for prototyping, but its important to deal with this debt
# before expanding the canvas functionality, otherwise the code will become unwieldly fast

class SDCanvas(AreaMixin, DrawMixin, BGMixin, ViewMixin, Canvas):
    STATE = Enum('STATE', ['IDLE', 'DRAW', 'LINE', 'SCROLL'])

    def __init__(self, parent, **kwargs) -> None:
        super().__init__(parent, **kwargs)

        self._state: SDCanvas.STATE = SDCanvas.STATE.IDLE
        self._curr_xy: Tuple[int, int] = (0, 0)

        self.configure(
            # needed for drag scrolling to work
            xscrollincrement=1, yscrollincrement=1,
            # allow going out of scrollregion
            confine=False,
        )

        bg_file = 'backgrounds/paper5_1.png'
        self.set_background_tile(bg_file)

        self._svg = SVGMixin(
            self, self.active_area, self.items,
            bg_file=bg_file, oval_style=STYLES.OVAL, line_style=STYLES.LINE
        )

        self.bind('<ButtonPress-1>', self._draw_init)
        self.bind('<B1-Motion>', self._draw_drag)
        self.bind('<ButtonRelease-1>', self._draw_end)

        self.bind('<ButtonPress-3>', self._scroll_init)
        self.bind('<B3-Motion>', self._scroll_drag)
        self.bind('<ButtonRelease-3>', self._scroll_end)

        self.bind('z', lambda _: self.remove_last_item())
        self.bind('s', lambda _: self._svg.save('test.svg'))
        self.bind('l', lambda _: self._svg.load('test.svg'))
        self.focus_set()

    def _draw_init(self, event):
        if self._state != SDCanvas.STATE.IDLE:
            return
        self._state = SDCanvas.STATE.DRAW
        self._curr_xy = self._translate_xy(event)

    def _draw_drag(self, event):
        xy = self._translate_xy(event)
        match self._state:
            case SDCanvas.STATE.DRAW:
                self.start_line(*self._curr_xy, *xy)
                self._state = SDCanvas.STATE.LINE
            case SDCanvas.STATE.LINE:
                self.extend_line(*xy)
            case _:
                return
        self._curr_xy = xy

    def _draw_end(self, event):
        match self._state:
            case SDCanvas.STATE.DRAW:
                self.draw_point(*self._translate_xy(event))
            case SDCanvas.STATE.LINE:
                self.end_line()
            case _:
                return
        self._state = SDCanvas.STATE.IDLE

    def _scroll_init(self, event):
        if self._state != SDCanvas.STATE.IDLE:
            return
        self._state = SDCanvas.STATE.SCROLL
        self._curr_xy = event.x, event.y
        # TODO: find way to use grabbing hand cursor
        self.config(cursor="hand1")

    def _scroll_drag(self, event):
        if self._state != SDCanvas.STATE.SCROLL:
            return
        xy = event.x, event.y
        x_units = self._curr_xy[0] - xy[0]
        if x_units != 0:
            self.xview('scroll', str(x_units), 'units')
        y_units = self._curr_xy[1] - xy[1]
        if y_units != 0:
            self.yview('scroll', str(y_units), 'units')
        self._curr_xy = xy

    def _scroll_end(self, _):
        if self._state != SDCanvas.STATE.SCROLL:
            return
        self._state = SDCanvas.STATE.IDLE
        self.config(cursor="")


    def _translate_xy(self, event):
        return (int(self.canvasx(event.x)), int(self.canvasy(event.y)))
