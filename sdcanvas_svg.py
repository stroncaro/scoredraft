from decimal import Decimal
from itertools import chain
from tkinter import Canvas
from typing import Literal, List, Tuple

from svg import Circle, Element, SVG, Polyline

class SDCanvasSvgHandler:
    _canvas: Canvas

    def __init__(self, canvas: Canvas):
        self._canvas = canvas

    def save(
        self,
        item_ids: List[int],
        bounds: Tuple[float, float, float, float]
    ) -> None:
        x = bounds[0]
        y = bounds[1]
        w = bounds[2] - x
        h = bounds[3] - y

        ovals = (self._make_oval(id, -x, -y) for id in item_ids if self._get_item_type(id) == 'oval')
        lines = (self._make_line(id, -x, -y) for id in item_ids if self._get_item_type(id) == 'line')
        elements: List[Element] = list(chain(ovals, lines))
        svg = SVG(width=w, height=h, elements=elements)

        # add background
        # write to file
        raise NotImplementedError()

    def _get_item_type(self, item_id: int) -> Literal['oval'] | Literal['line']:
        item_type = self._canvas.type(item_id)
        match item_type:
            case 'oval' | 'line':
                return item_type
            case _:
                raise TypeError(f'Invalid item type: {item_type}')

    def _make_oval(self, item_id: int, x_offset: float, y_offset: float) -> Circle:
        """
        ITEM 2:
          item_type='oval'
          item_coords=[116.0, 95.0, 120.0, 99.0]
          Width / Fill: 1.0 / gray
        """

        coords = self._canvas.coords(item_id)
        r = coords[2] - coords[0]
        cx = (coords[0] + coords[2]) / 2 + x_offset
        cy = (coords[1] + coords[3]) / 2 + y_offset

        line_width = self._canvas.itemcget(item_id, 'width')
        color = self._canvas.itemcget(item_id, 'fill')

        return Circle(cx=cx, cy=cy, r=r)

    def _make_line(self, item_id: int, x_offset: float, y_offset: float) -> Polyline:
        """
        ITEM 3:
          item_type='line'
          item_coords=[264.0, 72.0, 255.0, 81.0, 246.0, 90.0, 240.0, 98.0, 235.0, 104.0, 231.0, 109.0, 227.0, 113.0, 224.0, 118.0, 219.0, 123.0, 213.0, 130.0, 205.0, 140.0, 194.0, 154.0, 185.0, 167.0, 179.0, 176.0, 174.0, 184.0, 171.0, 188.0, 169.0, 191.0, 168.0, 193.0, 167.0, 194.0, 166.0, 195.0, 165.0, 195.0, 165.0, 196.0]
          Width / Fill: 3.0 / gray
        """

        points: List[Decimal | float | int] = list(
            v - (x_offset, y_offset)[i % 2]
            for i, v in enumerate(self._canvas.coords(item_id))
        )

        line_width = self._canvas.itemcget(item_id, 'width')
        color = self._canvas.itemcget(item_id, 'fill')

        return Polyline(points=points)

    def load(self, source: str) -> List[int]:
        # load svg
        # get items from svg
        # add items to canvas
        # return item ids
        raise NotImplementedError()
