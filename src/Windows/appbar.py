"""
Windows AppBar management for Classification Banner
"""

import ctypes
from ctypes import wintypes
from .constants import ABM_NEW, ABM_REMOVE, ABM_SETPOS, ABE_TOP


class RECT(ctypes.Structure):
    _fields_ = [
        ("left", wintypes.LONG),
        ("top", wintypes.LONG),
        ("right", wintypes.LONG),
        ("bottom", wintypes.LONG),
    ]


class APPBARDATA(ctypes.Structure):
    _fields_ = [
        ("cbSize", wintypes.DWORD),
        ("hWnd", wintypes.HWND),
        ("uCallbackMessage", wintypes.UINT),
        ("uEdge", wintypes.UINT),
        ("rc", RECT),
        ("lParam", wintypes.LPARAM),
    ]


_shell32 = ctypes.windll.shell32
_user32 = ctypes.windll.user32


def register_appbar_for_window(hwnd, x, y, width, height, edge=ABE_TOP) -> APPBARDATA:
    """Register/position a window as an AppBar so maximized windows avoid it."""
    abd = APPBARDATA()
    abd.cbSize = ctypes.sizeof(APPBARDATA)
    abd.hWnd = hwnd
    abd.uCallbackMessage = 0
    abd.uEdge = edge

    abd.rc.left = x
    abd.rc.top = y
    abd.rc.right = x + width
    abd.rc.bottom = y + height

    _shell32.SHAppBarMessage(ABM_NEW, ctypes.byref(abd))
    _shell32.SHAppBarMessage(ABM_SETPOS, ctypes.byref(abd))

    _user32.MoveWindow(
        hwnd,
        abd.rc.left,
        abd.rc.top,
        abd.rc.right - abd.rc.left,
        abd.rc.bottom - abd.rc.top,
        True,
    )

    return abd


def remove_appbar_for_window(hwnd) -> None:
    """Unregister the AppBar."""
    abd = APPBARDATA()
    abd.cbSize = ctypes.sizeof(APPBARDATA)
    abd.hWnd = hwnd
    _shell32.SHAppBarMessage(ABM_REMOVE, ctypes.byref(abd))
