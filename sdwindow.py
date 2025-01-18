from tkinter import Tk, HORIZONTAL, VERTICAL
from tkinter import ttk

from sdcanvas import SDCanvas

# TODO: find how to run many concurrent windows in a nonblocking manner.

class SDWindow(Tk):
    """Main ScoreDraft window"""
    def __init__(self) -> None:
        super().__init__()
        self.title('ScoreDraft')
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        fr = ttk.Frame(self, width=800, height=600)
        fr.grid(column=0, row=0, sticky='nwse')
        fr.grid_columnconfigure(0, weight=1)
        fr.grid_rowconfigure(0, weight=1)

        sp = SDCanvas(fr, scrollregion=(0, 0, 400, 400))
        sx = ttk.Scrollbar(fr, orient=HORIZONTAL, command=sp.xview)
        sy = ttk.Scrollbar(fr, orient=VERTICAL, command=sp.yview)
        sp.configure(xscrollcommand=sx.set, yscrollcommand=sy.set)

        sp.grid(column=0, row=0, sticky='nwse')
        sx.grid(column=0, row=1, sticky='we')
        sy.grid(column=1, row=0, sticky='ns')

        subc = SDCanvas(sp, highlightbackground='green', highlightcolor='green', highlightthickness=2)
        subc.create_line(25, 25, 75, 75, fill='red', width=3)
        sp.create_window(0, 0, anchor='nw', width=100, height=100, window=subc)

if __name__ == "__main__":
    sd = SDWindow()
    sd.mainloop()
