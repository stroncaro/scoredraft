"""
Save and load the contents of the SDCanvas to an svg file.
"""
from typing import Any, List, Literal, Tuple

import base64
from itertools import chain
from xml.etree import ElementTree

from svg import (
    Circle, Defs, Element, Image, Length, Pattern,
    Polyline, PreserveAspectRatio, Rect, Style, SVG
)

from sdcanvas import STYLES
from sdcanvas.mixins import BGMixin, DrawMixin, AreaMixin

# TODO: save in git friendly svg file

SVG_STYLE = "".join(f"""
    polyline {{
        stroke: {STYLES.LINE['fill']};
        stroke-width: {STYLES.LINE['width']};
        fill: none;
    }}

    circle {{
        fill: {STYLES.OVAL['fill']};
    }}
""".split())

class SVGMixin(BGMixin, DrawMixin, AreaMixin):
    """Handle saving and loading to svg files"""

    def save(self, file: str) -> None:
        x, y, w, h = self._get_xywh()

        def_element = Defs(elements=[Style(text=SVG_STYLE)])
        elements: List[Element] = [def_element]
        self._save_bg(def_element, elements)

        # TODO: save item order?
        items = self.items
        ovals = (self._save_oval(i, x, y) for i in items if self._get_item_type(i) == 'oval')
        lines = (self._save_line(i, x, y) for i in items if self._get_item_type(i) == 'line')
        elements += list(chain(ovals, lines))

        svg = SVG(width=w, height=h, elements=elements)

        with open(file, 'w', encoding='utf-8') as f:
            f.write(str(svg))

    def load(self, file: str) -> None:
        svg = ElementTree.parse(file).getroot()
        ns = {"svg": "http://www.w3.org/2000/svg"}
        for oval in svg.findall('.//svg:circle', ns):
            self._load_oval(oval)
        for line in svg.findall('.//svg:polyline', ns):
            self._load_line(line)

    def _get_xywh(self) -> Tuple[float, float, float, float]:
        # unpack
        # TODO: add properties to AreaMixin
        x = self.active_area[0]
        y = self.active_area[1]
        w = self.active_area[2] - x
        h = self.active_area[3] - y

        # adjust offset for bg_size
        bg_x, bg_y = self.tile_size
        if bg_x > 0:
            x = (x // bg_x) * -bg_x
        if bg_y > 0:
            y = (y // bg_y) * -bg_y

        return x, y, w, h

    def _save_bg(self, defs: Defs, elems: List[Element]) -> None:
        if not self.has_background:
            return

        img_b64 = self._img_to_base64(self.background_tile) # type: ignore
        img = Image(
            id='tile', href=img_b64, x=0, y=0, width=self.tile_w, height=self.tile_h,
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
        item_type = self.type(item_id)
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
        coords = self.coords(item_id)
        r = (coords[2] - coords[0]) / 2
        cx = (coords[0] + coords[2]) / 2 + x_offset
        cy = (coords[1] + coords[3]) / 2 + y_offset
        return Circle(cx=cx, cy=cy, r=r)

    def _save_line(self, item_id: int, x_offset: float, y_offset: float) -> Polyline:
        points: List[Any] = list(
            v + (x_offset, y_offset)[i % 2]
            for i, v in enumerate(self.coords(item_id))
        )
        return Polyline(points=points)

    def _load_oval(self, e: ElementTree.Element) -> None:
        cx, cy = (float(e.attrib[k]) for k in ('cx', 'cy'))
        self.draw_point(cx, cy)

    def _load_line(self, e: ElementTree.Element) -> None:
        points = (float(p) for p in e.attrib['points'].split())
        self.draw_line(*points)
