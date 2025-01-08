from tkinter import Canvas
from typing import Literal, Optional, Tuple

from PIL import Image, ImageTk

class SDCanvasTileBackgroundHandler:
    """Adds a tiling background to an infinite canvas. Requires hooking the provided methods."""
    TAG = 'background'

    _canvas: Canvas
    _tile: Image.Image
    _bg: Image.Image
    _imgtk: ImageTk.PhotoImage
    _view_pos: Tuple[int, int]

    def __init__(self, canvas: Canvas, tile: Image.Image, initial_position: Tuple[int, int]=(0, 0)):
        self._canvas = canvas
        self._tile = tile
        self._view_pos = initial_position
        self._bg = self._tile
        self._imgtk = ImageTk.PhotoImage(self._tile)
        self._canvas.create_image(*self._view_pos, image=self._imgtk, anchor='nw', tags=self.TAG)
        self._resize_background(self._view_w, self._view_h)

    def on_xview(self, *args):
        """Hook for canvas xview method. Updates background to be into view"""
        if len(args) >= 2:
            self._scroll_background('x', *args)

    def on_yview(self, *args):
        """Hook for canvas yview method. Updates background to be into view"""
        if len(args) >= 2:
            self._scroll_background('y', *args)

    def on_configure(self, event):
        """Hook for canvas configure event. Updates background to fill window"""
        self._resize_background(event.width, event.height)

    @property
    def _tile_w(self) -> int:
        return self._tile.size[0]

    @property
    def _tile_h(self) -> int:
        return self._tile.size[1]

    @property
    def _bg_w(self) -> int:
        return self._bg.size[0]

    @property
    def _bg_h(self) -> int:
        return self._bg.size[1]

    @property
    def _view_w(self) -> int:
        return self._canvas.winfo_width()

    @property
    def _view_h(self) -> int:
        return self._canvas.winfo_height()

    @property
    def _view_x(self) -> int:
        return self._view_pos[0]

    @_view_x.setter
    def _view_x(self, val: int):
        self._view_pos = val, self._view_pos[1]

    @property
    def _view_y(self) -> int:
        return self._view_pos[1]

    @_view_y.setter
    def _view_y(self, val: int):
        self._view_pos = self._view_pos[0], val

    @property
    def _scrollregion_bounds_x(self) -> Tuple[int, int]:
        sr = self._canvas.cget('scrollregion').split()
        return int(sr[0]), int(sr[2])

    @property
    def _scrollregion_bounds_y(self) -> Tuple[int, int]:
        sr = self._canvas.cget('scrollregion').split()
        return int(sr[1]), int(sr[3])

    def _resize_background(self, w, h) -> None:
        if w <= self._bg_w and h <= self._bg_h:
            return

        # Adjust w and h to be multiples of tile size
        w = w - w % self._tile_w + 2 * self._tile_w
        h = h - h % self._tile_h + 2 * self._tile_h

        # Create img and copy already existing background
        new_bg = Image.new('RGB', (w, h))
        new_bg.paste(self._bg)

        # Fill missing tiles
        for x in range(self._bg_w, w, self._tile_w):
            for y in range(0, self._bg_h, self._tile_h):
                new_bg.paste(self._tile, (x, y))
        for x in range(0, w, self._tile_w):
            for y in range(self._bg_h, h, self._tile_h):
                new_bg.paste(self._tile, (x, y))

        # Update background
        self._bg = new_bg
        self._imgtk = ImageTk.PhotoImage(self._bg)
        self._canvas.itemconfig(self.TAG, image=self._imgtk)

    def _scroll_background(
        self,
        axis: Literal['x'] | Literal['y'],
        method: Literal['scroll'] | Literal['moveto'],
        number: str,
        what: Optional[Literal['units'] | Literal['pages']]=None,
    ):
        n = float(number)
        pos = self._view_x if axis == 'x' else self._view_y

        # Calculate new position
        if method == 'scroll':
            # Ignore mypy error, what is guaranteed to be 'units' or 'pages' if method is 'scroll'
            pos += int(n * self._get_scroll_unit(axis, what)) # type: ignore
        else:
            v1, v2 = self._scrollregion_bounds_x if axis == 'x' else self._scrollregion_bounds_y
            pos = int((v2 - v1) * n) + v1

        # Update axis position and background
        bg_x, bg_y = self._canvas.coords(self.TAG)
        if axis == 'x':
            self._view_x = pos
            bg_x = pos // self._tile.size[0] * self._tile.size[0]
        else:
            self._view_y = pos
            bg_y = pos // self._tile.size[1] * self._tile.size[1]
        self._canvas.coords(self.TAG, bg_x, bg_y)

    def _get_scroll_unit(
        self,
        axis: Literal['x'] | Literal['y'],
        what: Literal['units'] | Literal['pages']
    ) -> float:
        size = self._view_w if axis == 'x' else self._view_h
        if what == 'pages':
            return size * 9 / 10

        inc = self._canvas.cget(axis + 'scrollincrement')
        if inc == "" or int(inc) <= 0:
            return size / 10

        return int(inc)
