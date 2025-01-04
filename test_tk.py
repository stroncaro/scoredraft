from typing import Tuple, List, Optional

from tkinter import Tk, Canvas

class SketchPad(Canvas):
    def __init__(self, parent, **kwargs) -> None:
        super().__init__(parent, **kwargs)

        self._is_drawing: bool = False
        self._current_coords: Tuple[int, int] = (0, 0)
        self._current_line: int = 0
        self._lines: List[int] = []

        self._line_style = {
            'width': 3,
            'fill': 'gray',
            'joinstyle': 'round',
            'capstyle': 'round',
            # 'smooth': 'bezier', # do not use, laggy
        }

        self.bind('<ButtonPress-1>', self._init_line)
        self.bind('<B1-Motion>', self._draw_line)
        self.bind('<ButtonRelease-1>', self._end_line)
        parent.bind('z', self._undo)

    def _init_line(self, event):
        self._current_coords = (event.x, event.y)

    def _draw_line(self, event):
        if self._is_drawing:
            self.coords(self._current_line, *self.coords(self._current_line), event.x, event.y)
        else:
            line_id = self.create_line(*self._current_coords, event.x, event.y, **self._line_style)
            self._current_line = line_id
            self._is_drawing = True
        self._current_coords = (event.x, event.y)

    def _end_line(self, _):
        self._lines.append(self._current_line)
        self._is_drawing = False

    def _undo(self, _):
        print("undo")
        if len(self._lines) > 0:
            self.delete(self._lines.pop())


# Mouse
# canvas.bind('<ButtonPress-1>', print)
# canvas.bind('<B1-Motion>', print)
# canvas.bind('<ButtonPress-3>', print)
# canvas.bind('<B3-Motion>', print)
# canvas.bind('<MouseWheel>', print)

# Keys
# canvas.bind('<KeyPress-z>', print)
# canvas.bind('<KeyPress-x>', print)

# Resize (also triggers on canvas creation)
# canvas.bind('<Configure>', print)


if __name__ == "__main__":

    root = Tk()
    root.title('Paint')
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)

    sp = SketchPad(root, width=800, height=600)
    sp.grid(column=0, row=0)

    root.mainloop()
