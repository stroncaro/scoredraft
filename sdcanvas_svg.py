import base64
from decimal import Decimal
from itertools import chain
from tkinter import Canvas
from typing import Literal, List, Optional, Tuple
from xml.etree import ElementTree

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

        ovals = (self._save_oval(i, -x, -y) for i in item_ids if self._get_item_type(i) == 'oval')
        lines = (self._save_line(i, -x, -y) for i in item_ids if self._get_item_type(i) == 'line')
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

    def _save_oval(self, item_id: int, x_offset: float, y_offset: float) -> Circle:
        coords = self._canvas.coords(item_id)
        r = coords[2] - coords[0] - 1
        cx = (coords[0] + coords[2]) / 2 + x_offset
        cy = (coords[1] + coords[3]) / 2 + y_offset
        return Circle(cx=cx, cy=cy, r=r)

    def _save_line(self, item_id: int, x_offset: float, y_offset: float) -> Polyline:
        points: List[Decimal | float | int] = list(
            v - (x_offset, y_offset)[i % 2]
            for i, v in enumerate(self._canvas.coords(item_id))
        )
        return Polyline(points=points)

    def load(self, source: str='test.svg') -> List[int]:
        svg = ElementTree.parse(source).getroot()
        ns = {"svg": "http://www.w3.org/2000/svg"}
        ovals = (self._load_oval(e) for e in svg.findall('.//svg:circle', ns))
        lines = (self._load_line(e) for e in svg.findall('.//svg:polyline', ns))
        item_ids = list(chain(ovals, lines))
        return item_ids

    def _load_oval(self, e: ElementTree.Element) -> int:
        cx, cy, r = (float(e.attrib[k]) for k in ('cx', 'cy', 'r'))
        x1, y1, x2, y2 = cx - r, cy - r, cx + r, cy + r
        return self._canvas.create_oval(x1, y1, x2, y2)

    def _load_line(self, e: ElementTree.Element) -> int:
        points = (float(p) for p in e.attrib['points'].split())
        return self._canvas.create_line(*points)
