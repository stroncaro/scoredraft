from enum import Enum
from tkinter import Canvas
from typing import Tuple, List

from PIL import Image

from sdcanvas_svg import SDCanvasSvgHandler
from sdcanvas_tile_bg import SDCanvasTileBackgroundHandler

# TODO: refactor state handling and other components into encapsulated parts.
# Tkinter virtual events can help with decoupling, but a complete rework is needed
# Current implementation is fine for prototyping, but its important to deal with this debt
# before expanding the canvas functionality, otherwise the code will become unwieldly fast

class SDCanvas(Canvas):
    STATE = Enum('STATE', ['IDLE', 'DRAW', 'LINE', 'SCROLL'])
    ITEM_STYLE = {
        'width': 3,
        'fill': 'gray',
        'joinstyle': 'round',
        'capstyle': 'round',
    }

    def __init__(self, parent, **kwargs) -> None:
        super().__init__(parent, **kwargs)

        self._state: SDCanvas.STATE = SDCanvas.STATE.IDLE
        self._curr_xy: Tuple[int, int] = (0, 0)
        self._curr_item: int = 0
        self._items: List[int] = []

        self.configure(
            # needed for drag scrolling to work
            xscrollincrement=1, yscrollincrement=1,
            # allow going out of scrollregion
            confine=False,
        )

        if self.cget('scrollregion'):
            self._data_bounds = [float(s) for s in self.cget('scrollregion').split()]
        else:
            self._data_bounds = [float('inf'), float('inf'), float('-inf'), float('-inf')]

        tile = Image.open('backgrounds/paper5_1.png')
        self._tile_bg_handler = SDCanvasTileBackgroundHandler(self, tile)


        self._serializer = SDCanvasSvgHandler(self)

        self.bind('<ButtonPress-1>', self._draw_init)
        self.bind('<B1-Motion>', self._draw_drag)
        self.bind('<ButtonRelease-1>', self._draw_end)

        self.bind('<ButtonPress-3>', self._scroll_init)
        self.bind('<B3-Motion>', self._scroll_drag)
        self.bind('<ButtonRelease-3>', self._scroll_end)

        self.bind('<Configure>', self._tile_bg_handler.on_configure)

        self.bind('z', self._undo)
        self.bind('s', lambda _: self._serializer.save(self._items, self._data_bounds))
        self.focus_set()


    def xview(self, *args):
        self._tile_bg_handler.on_xview(*args)
        return super().xview(*args)

    def yview(self, *args):
        self._tile_bg_handler.on_yview(*args)
        return super().yview(*args)

    def _draw_init(self, event):
        if self._state != SDCanvas.STATE.IDLE:
            return
        self._state = SDCanvas.STATE.DRAW
        self._curr_xy = self._translate_xy(event)

    def _draw_drag(self, event):
        xy = self._translate_xy(event)
        match self._state:
            case SDCanvas.STATE.DRAW:
                line_id = self.create_line(*self._curr_xy, *xy, **SDCanvas.ITEM_STYLE)
                self._curr_item = line_id
                self._state = SDCanvas.STATE.LINE
                self._update_data_bounds(*self._curr_xy)
            case SDCanvas.STATE.LINE:
                self.coords(self._curr_item, *self.coords(self._curr_item), *xy)
            case _:
                return
        self._curr_xy = xy
        self._update_data_bounds(*self._curr_xy)

    def _draw_end(self, event):
        match self._state:
            case SDCanvas.STATE.DRAW:
                x, y, w = *self._translate_xy(event), SDCanvas.ITEM_STYLE['width'] - 1
                x1, y1, x2, y2 = x - w, y - w, x + w, y + w
                point_id = self.create_oval(
                    x1, y1, x2, y2,
                    fill=SDCanvas.ITEM_STYLE['fill'],
                    outline=SDCanvas.ITEM_STYLE['fill'],
                )
                self._items.append(point_id)
                self._update_data_bounds(x1, y1)
                self._update_data_bounds(x2, y2)
            case SDCanvas.STATE.LINE:
                self._items.append(self._curr_item)
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

    def _undo(self, _):
        try:
            self.delete(self._items.pop())
        except IndexError:
            pass

    def _update_data_bounds(self, x, y):
        updated = False
        if x < self._data_bounds[0]:
            self._data_bounds[0] = x
            updated = True
        if x > self._data_bounds[2]:
            self._data_bounds[2] = x
            updated = True
        if y < self._data_bounds[1]:
            self._data_bounds[1] = y
            updated = True
        if y > self._data_bounds[3]:
            self._data_bounds[3] = y
            updated = True
        if not updated:
            return

        new = tuple(n for n in self._data_bounds)
        if self.cget('scrollregion'):
            old = tuple(int(n) for n in self.cget('scrollregion').split())
            new = min(old[0], new[0]), min(old[1], new[1]), max(old[2], new[2]), max(old[3], new[3])

        self.config(scrollregion=new)
