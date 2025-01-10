from tkinter import Canvas
from typing import Iterable

import svg

class SDCanvasSvgHandler:
    _canvas: Canvas

    def __init__(self, canvas: Canvas):
        self._canvas = canvas

    def save(self, dest: str, item_ids: Iterable[int]) -> None:
        # create new svg
        # add all items
        # add background
        # write to file
        raise NotImplementedError()

    def load(self, source: str) -> List[int]:
        # load svg
        # get items from svg
        # add items to canvas
        # return item ids
        raise NotImplementedError()
