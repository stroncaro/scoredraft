import base64
from decimal import Decimal
from itertools import chain
from tkinter import Canvas
from typing import Literal, List, Optional, Tuple

from svg import (
    Circle, Defs, Element, Image, Length, Pattern, Polyline, PreserveAspectRatio, Rect, Style, SVG
)

class SDCanvasSvgHandler:
    STYLE = "".join("""
        polyline {
            stroke: gray;
            stroke-width: 3;
            fill: none;
        }

        circle {
            fill: gray;
        }
    """.split())

    _canvas: Canvas

    def __init__(self, canvas: Canvas):
        self._canvas = canvas

    def save(
        self,
        item_ids: List[int],
        bounds: Tuple[float, float, float, float],
        bg_file: Optional[str]=None,
    ) -> None:
        x = bounds[0]
        y = bounds[1]
        w = bounds[2] - x
        h = bounds[3] - y

        def_element = Defs(elements=[Style(text=self.STYLE)])
        elements: List[Element] = [def_element]

        if bg_file is not None:
            self._add_bg(bg_file, def_element, elements)

        ovals = (self._make_oval(i, -x, -y) for i in item_ids if self._get_item_type(i) == 'oval')
        lines = (self._make_line(i, -x, -y) for i in item_ids if self._get_item_type(i) == 'line')
        elements += list(chain(ovals, lines))

        svg = SVG(width=w, height=h, elements=elements)

        with open('test.svg', 'w', encoding='utf-8') as f:
            f.write(str(svg))

    def _add_bg(self, bg_file: str, defs: Defs, elems: List[Element]) -> None:
        img_b64 = self._img_to_base64(bg_file)
        img = Image(
            id='tile', href=img_b64, x=0, y=0, width=64, height=64,
            preserveAspectRatio=PreserveAspectRatio('none')
        )
        pattern = Pattern(
            id='background', width=64, height=64,
            elements=[img], patternUnits='userSpaceOnUse'
        )
        if defs.elements is not None:
            defs.elements += [pattern]
        else:
            defs.elements = [pattern]
        bg_rect = Rect(width=Length(100, '%'), height=Length(100, '%'), fill='url(#background)')
        elems += [bg_rect]

    def _get_item_type(self, item_id: int) -> Literal['oval'] | Literal['line']:
        item_type = self._canvas.type(item_id)
        match item_type:
            case 'oval' | 'line':
                return item_type
            case _:
                raise TypeError(f'Invalid item type: {item_type}')

    def _img_to_base64(self, img_path: str) -> str:
        with open(img_path, "rb") as f:
            img = base64.b64encode(f.read()).decode("utf-8")
        return f"data:image/png;base64,{img}"

    def _make_oval(self, item_id: int, x_offset: float, y_offset: float) -> Circle:
        coords = self._canvas.coords(item_id)
        r = coords[2] - coords[0]
        cx = (coords[0] + coords[2]) / 2 + x_offset
        cy = (coords[1] + coords[3]) / 2 + y_offset
        return Circle(cx=cx, cy=cy, r=r)

    def _make_line(self, item_id: int, x_offset: float, y_offset: float) -> Polyline:
        points: List[Decimal | float | int] = list(
            v - (x_offset, y_offset)[i % 2]
            for i, v in enumerate(self._canvas.coords(item_id))
        )
        return Polyline(points=points)

    def load(self, source: str) -> List[int]:
        # load svg
        # get items from svg
        # add items to canvas
        # return item ids
        raise NotImplementedError()
