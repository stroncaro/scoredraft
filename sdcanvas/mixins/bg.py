from typing import Optional
import tkinter as tk

import PIL.Image
from PIL import UnidentifiedImageError
from PIL.Image import Image as PILImage
from PIL.ImageTk import PhotoImage as PILPhotoImage
from PIL.ImageFile import ImageFile as PILImageFile

from sdcanvas.mixins.view import ViewMixin

class BGMixin(ViewMixin, tk.Canvas):
    """Adds a tiling background to an infinite canvas. Requires hooking the provided methods."""
    TAG = 'background'

    _configure_bind_id: str | None = None
    _tile: Optional[PILImageFile] = None
    _bg_img: Optional[PILImage] = None
    _bg_photoimg: Optional[PILPhotoImage] = None

    @property
    def has_background(self):
        """Return True if the background is active."""
        return self._tile is not None

    @property
    def background_tile(self) -> str | None:
        """Returns the filename of the img used as background tile, or None if not set."""
        return str(self._tile.filename) if self._tile is not None else None

    def set_background_tile(self, file: str):
        """Add a background to the canvas from a tiling image."""

        # Attempt to load image
        try:
            tile = PIL.Image.open(file)
        except (FileNotFoundError, OSError, UnidentifiedImageError, ValueError):
            print("Loading background image failed. Ignoring.")
            return

        # Clear existing background
        self.clear_background()

        # Create new background
        self._tile = tile
        self._configure_bind_id = self.bind('<Configure>', self._on_configure, add=True)
        self.create_image(*self.view_position, image=None, anchor='nw', tags=self.TAG)
        self._resize_background(self.view_w, self.view_h)

    def clear_background(self) -> None:
        """Remove the background from the canvas."""
        if self._configure_bind_id is not None:
            self.unbind('<Configure>', self._configure_bind_id)
            self._configure_bind_id = None

        self._tile = None
        self._bg_img = None
        self._bg_photoimg = None
        self.delete(self.TAG)

    def xview(self, *args):
        """Update background to be into view"""
        out = super().xview(*args)
        if len(args) >= 2:
            self._scroll_background()
        return out

    def yview(self, *args):
        """Update background to be into view"""
        out = super().yview(*args)
        if len(args) >= 2:
            self._scroll_background()
        return out

    def _on_configure(self, event):
        """Hook for canvas configure event. Updates background to fill window"""
        self._resize_background(event.width, event.height)

    @property
    def tile_w(self) -> int:
        """Width of the tile image used for the background if it exists, 0 otherwise."""
        return self._tile.size[0] if self._tile is not None else 0

    @property
    def tile_h(self) -> int:
        """Height of the tile image used for the background if it exists, 0 otherwise."""
        return self._tile.size[1] if self._tile is not None else 0

    @property
    def background_w(self) -> int:
        """Width of the background image if it exists, 0 otherwise."""
        return self._bg_img.size[0] if self._bg_img is not None else 0

    @property
    def background_h(self) -> int:
        """Height of the background image if it exists, 0 otherwise."""
        return self._bg_img.size[1] if self._bg_img is not None else 0

    def _resize_background(self, w, h) -> None:
        if self._tile is None:
            return

        if w <= self.background_w and h <= self.background_h:
            return

        # Adjust w and h to be multiples of tile size
        w = w - w % self.tile_w + 2 * self.tile_w
        h = h - h % self.tile_h + 2 * self.tile_h

        # Create img and copy already existing background
        bg = PIL.Image.new('RGB', (w, h))
        if self._bg_img is not None:
            bg.paste(self._bg_img)

        # Fill missing tiles
        for x in range(self.background_w, w, self.tile_w):
            for y in range(0, self.background_h, self.tile_h):
                bg.paste(self._tile, (x, y))
        for x in range(0, w, self.tile_w):
            for y in range(self.background_h, h, self.tile_h):
                bg.paste(self._tile, (x, y))

        # Update background
        self._bg_img = bg
        self._bg_photoimg = PILPhotoImage(self._bg_img)
        self.itemconfig(self.TAG, image=self._bg_photoimg)

    def _scroll_background(self) -> None:
        if self._tile is None:
            return

        bg_x, bg_y = self.coords(self.TAG)
        bg_x = self.view_x // self.tile_w * self.tile_w
        bg_y = self.view_y // self.tile_h * self.tile_h
        self.coords(self.TAG, bg_x, bg_y)
