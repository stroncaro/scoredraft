"""
Default SDCanvas styles for Tk graphical elements.
"""

from typing import Any, Dict

OVAL: Dict[str, Any] = {
    'fill': 'gray',
    'outline': 'gray',
}

LINE: Dict[str, Any] = {
    'width': '3',
    'fill': 'gray',
    'joinstyle': 'round',
    'capstyle': 'round',
}

RECT: Dict[str, Any] = {
    'width': '2',
    'outline': 'green',
}

SUBCANVAS: Dict[str, Any] = {
    'highlightbackground': 'green', 
    'highlightcolor': 'green', 
    'highlightthickness': '2',
}
