import tkinter as tk
from tkinter import font
import ctypes
import sys
import winreg
from screeninfo import get_monitors
import socket
import platform
import subprocess
import os

# ------------------ AppBar (Win32) definitions ------------------
# See https://learn.microsoft.com/en-us/windows/win32/api/shellapi/ns-shellapi-appbardata

from ctypes import wintypes

# https://learn.microsoft.com/en-us/windows/win32/shell/abm-new
ABM_NEW = 0x00000000
# https://learn.microsoft.com/en-us/windows/win32/shell/abm-remove
ABM_REMOVE = 0x00000001
# https://learn.microsoft.com/en-us/windows/win32/shell/abm-querypos
ABM_QUERYPOS = 0x00000002
# https://learn.microsoft.com/en-us/windows/win32/shell/abm-setpos
ABM_SETPOS = 0x00000003

ABE_LEFT = 0
ABE_TOP = 1
ABE_RIGHT = 2
ABE_BOTTOM = 3


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
    abd.uCallbackMessage = 0  # we’re not handling callbacks in Tk
    abd.uEdge = edge

    abd.rc.left = x
    abd.rc.top = y
    abd.rc.right = x + width
    abd.rc.bottom = y + height

    # Tell the shell we’re a new appbar
    _shell32.SHAppBarMessage(ABM_NEW, ctypes.byref(abd))

    # Let the shell adjust our rectangle based on other appbars/taskbar
    _shell32.SHAppBarMessage(ABM_SETPOS, ctypes.byref(abd))

    # Move the window to the final rectangle
    _user32.MoveWindow(
        hwnd,
        abd.rc.left,
        abd.rc.top,
        abd.rc.right - abd.rc.left,
        abd.rc.bottom - abd.rc.top,
        True,
    )

    return abd  # Keep if you want to later ABM_REMOVE


def remove_appbar_for_window(hwnd) -> None:
    """Unregister the AppBar (optional but cleaner)."""
    abd = APPBARDATA()
    abd.cbSize = ctypes.sizeof(APPBARDATA)
    abd.hWnd = hwnd
    _shell32.SHAppBarMessage(ABM_REMOVE, ctypes.byref(abd))


class ClassificationBanner:
    def __init__(self):
        """
        Create a classification banner that reads settings from Windows Registry.

        Registry location: HKEY_LOCAL_MACHINE\\SOFTWARE\\ClassificationBanner
        or: HKEY_CURRENT_USER\\SOFTWARE\\ClassificationBanner

        Registry values:
            - Classification (REG_SZ): Text to display
            - BackgroundColor (REG_SZ): Background color in hex format (#RRGGBB)
            - TextColor (REG_SZ): Text color in hex format (#RRGGBB)
            - BannerHeight (REG_DWORD): Height of banner in pixels (default: 30)
            - FontSize (REG_DWORD): Font size (default: 12)
            - FontFamily (REG_SZ): Font family name (default: Arial)
            - Enabled (REG_DWORD): 1 to show banner, 0 to hide (default: 1)
            - FPCON (REG_SZ): Force Protection Condition (Alpha, Bravo, Charlie, Delta)
            - CYBERCON (REG_SZ): Cyber Condition (1, 2, 3, 4, 5)
        """
        # Default values
        self.classification: str = "UNCONFIGURED"
        self.bg_color: str = "#FFFFFF"
        self.fg_color: str = "#000000"
        self.banner_height: int = 47
        self.font_size: int = 12
        self.font_family: str = "Arial"
        self.enabled: int = 1
        self.fpcon: str = "Alpha"
        self.cybercon: str = "1"

        # System information
        self.hostname: str = ""
        self.username: str = ""
        self.windows_version: str = ""
        self.ip_address: str = ""
        self.group_id: str = ""

        # Flags to control what's displayed
        self.show_hostname: bool = False
        self.show_username: bool = False
        self.show_windows_version: bool = False
        self.show_ip_address: bool = False
        self.show_serial_number: bool = False
        self.show_group_id: bool = False

        # Common classification colors (fallback)
        self.color_schemes: dict[str, dict[str, str]] = {
            r"UNCONFIGURED": {"bg": "#FFFFFF", "fg": "#000000"},
            r"UNCLASSIFIED": {"bg": "#00FF00", "fg": "#000000"},
            r"CUI": {"bg": "#502B85", "fg": "#FFFFFF"},
            r"CONFIDENTIAL": {"bg": "#0000FF", "fg": "#FFFFFF"},
            r"SECRET": {"bg": "#FF0000", "fg": "#000000"},
            r"TOP SECRET": {"bg": "#FF8C00", "fg": "#000000"},
            r"TOP SECRET//HCS-P/SI/TK//NOFORN": {"bg": "#FFFF00", "fg": "#000000"},
        }

        self.windows = []

        # Load settings from registry
        self.load_registry_settings()

        # Gather system information if any display flags are enabled
        if any(
            [
                self.show_hostname,
                self.show_username,
                self.show_windows_version,
                self.show_ip_address,
                self.show_group_id,
            ]
        ):
            self.gather_system_info()

        # Only create banners if enabled
        if self.enabled:
            self.create_banners()

    def gather_system_info(self) -> None:
        """Gather system information for display"""
        try:
            # Hostname
            if self.show_hostname:
                self.hostname = socket.gethostname()

            # Domain\Username
            if self.show_username:
                try:
                    username = os.environ.get("USERNAME", "")
                    if username:
                        self.username = rf"{username}"
                except:
                    self.username = ""

            # Windows Version
            if self.show_windows_version:
                try:
                    version = platform.version()
                    release = platform.release()
                    self.windows_version = f"Windows {release} ({version})"
                except:
                    self.windows_version = ""

            # IP Address (primary/first non-loopback)
            if self.show_ip_address:
                try:
                    # Get the IP address by connecting to an external address
                    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                    s.settimeout(0.1)
                    try:
                        # Doesn't actually connect, just determines route
                        s.connect(("10.254.254.254", 1))
                        self.ip_address = s.getsockname()[0]
                    except:
                        self.ip_address = socket.gethostbyname(socket.gethostname())
                    finally:
                        s.close()
                except:
                    self.ip_address = ""

            # Group ID (from registry or environment)
            if self.show_group_id:
                try:
                    # Try to read from registry first (custom value)
                    for hkey, subkey in [
                        (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\ClassificationBanner"),
                        (winreg.HKEY_CURRENT_USER, r"SOFTWARE\ClassificationBanner"),
                    ]:
                        try:
                            key = winreg.OpenKey(hkey, subkey, 0, winreg.KEY_READ)
                            value, _ = winreg.QueryValueEx(key, "GroupID")
                            if value:
                                self.group_id = value
                            winreg.CloseKey(key)
                            break
                        except FileNotFoundError:
                            continue
                except:
                    self.group_id = ""

        except Exception as e:
            print(f"Error gathering system information: {e}")

    def load_registry_settings(self):
        """Load configuration from Windows Registry"""
        # Try HKEY_LOCAL_MACHINE first (system-wide), then HKEY_CURRENT_USER (user-specific)
        registry_paths = [
            (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\ClassificationBanner"),
            (winreg.HKEY_CURRENT_USER, r"SOFTWARE\ClassificationBanner"),
        ]

        for hkey, subkey in registry_paths:
            try:
                key = winreg.OpenKey(hkey, subkey, 0, winreg.KEY_READ)

                # Read Classification
                try:
                    value, _ = winreg.QueryValueEx(key, "Classification")
                    if value:
                        self.classification = value
                except FileNotFoundError:
                    pass

                # Read Enabled flag
                try:
                    value, _ = winreg.QueryValueEx(key, "Enabled")
                    self.enabled = int(value)
                except FileNotFoundError:
                    pass

                # If we found a classification, check if it matches a predefined scheme
                if self.classification.upper() in self.color_schemes:
                    scheme = self.color_schemes[self.classification.upper()]
                    self.bg_color = scheme["bg"]
                    self.fg_color = scheme["fg"]

                # Read custom colors (these override predefined schemes)
                try:
                    value, _ = winreg.QueryValueEx(key, "BackgroundColor")
                    if value and value.startswith("#"):
                        self.bg_color = value
                except FileNotFoundError:
                    pass

                try:
                    value, _ = winreg.QueryValueEx(key, "TextColor")
                    if value and value.startswith("#"):
                        self.fg_color = value
                except FileNotFoundError:
                    pass

                # Read BannerHeight
                try:
                    value, _ = winreg.QueryValueEx(key, "BannerHeight")
                    self.banner_height = int(value)
                except FileNotFoundError:
                    pass

                # Read FontSize
                try:
                    value, _ = winreg.QueryValueEx(key, "FontSize")
                    self.font_size = int(value)
                except FileNotFoundError:
                    pass

                # Read FontFamily
                try:
                    value, _ = winreg.QueryValueEx(key, "FontFamily")
                    if value:
                        self.font_family = value
                except FileNotFoundError:
                    pass

                # Read FPCON
                try:
                    value, _ = winreg.QueryValueEx(key, "FPCON")
                    if value:
                        self.fpcon = value.upper()
                except FileNotFoundError:
                    pass

                # Read CYBERCON
                try:
                    value, _ = winreg.QueryValueEx(key, "CYBERCON")
                    if value:
                        self.cybercon = str(value)
                except FileNotFoundError:
                    pass

                # Read system information display flags
                try:
                    value, _ = winreg.QueryValueEx(key, "ShowHostname")
                    self.show_hostname = bool(int(value))
                except FileNotFoundError:
                    pass

                try:
                    value, _ = winreg.QueryValueEx(key, "ShowUsername")
                    self.show_username = bool(int(value))
                except FileNotFoundError:
                    pass

                try:
                    value, _ = winreg.QueryValueEx(key, "ShowWindowsVersion")
                    self.show_windows_version = bool(int(value))
                except FileNotFoundError:
                    pass

                try:
                    value, _ = winreg.QueryValueEx(key, "ShowIPAddress")
                    self.show_ip_address = bool(int(value))
                except FileNotFoundError:
                    pass

                try:
                    value, _ = winreg.QueryValueEx(key, "ShowGroupID")
                    self.show_group_id = bool(int(value))
                except FileNotFoundError:
                    pass

                winreg.CloseKey(key)

                # If we successfully read from this registry location, don't try the next one
                break

            except FileNotFoundError:
                # Registry key doesn't exist, continue to next location
                continue
            except Exception as e:
                print(f"Error reading registry at {hkey}\\{subkey}: {e}")
                continue

    def create_banners(self):
        """Create banner windows for each monitor"""
        try:
            monitors = get_monitors()
        except Exception as e:
            print(f"Error detecting monitors: {e}")
            # Fallback to single monitor
            monitors = [
                type("obj", (object,), {"x": 0, "y": 0, "width": 1920, "height": 1080})
            ]

        for monitor in monitors:
            self.create_banner_for_monitor(monitor)

    def create_banner_for_monitor(self, monitor):
        """Create a banner window for a specific monitor"""
        window = tk.Tk()

        # Position at top of monitor
        window.geometry(f"{monitor.width}x{self.banner_height}+{monitor.x}+{monitor.y}")

        # Remove window decorations
        window.overrideredirect(True)

        # Set background color
        window.configure(bg=self.bg_color)

        # Always on top
        window.attributes("-topmost", True)

        # --- AppBar registration so maximized windows stop at bottom of banner ---
        window.update_idletasks()  # ensure window has a real HWND
        hwnd = window.winfo_id()
        # On Tk on Windows, winfo_id() is already the HWND; if paranoid:
        # hwnd = _user32.GetParent(window.winfo_id()) or window.winfo_id()

        # Register this window as a TOP AppBar for this monitor
        register_appbar_for_window(
            hwnd,
            monitor.x,
            monitor.y,
            monitor.width,
            self.banner_height,
            edge=ABE_TOP,
        )

        # Create main frame to hold left, center, and right content
        main_frame = tk.Frame(window, bg=self.bg_color)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Configure 3-column grid so center stays centered
        main_frame.grid_rowconfigure(0, weight=1)
        main_frame.grid_columnconfigure(0, weight=0)  # left - no expand
        main_frame.grid_columnconfigure(1, weight=1)  # center - expands
        main_frame.grid_columnconfigure(2, weight=0)  # right - no expand

        # Margins inside the banner (adjust these as you like)
        inner_padx = 10
        inner_pady = 0
        # Create label font
        label_font = font.Font(
            family=self.font_family, size=self.font_size, weight="bold"
        )

        # Build system info text for left side
        sys_info_parts = []
        if self.show_hostname and self.hostname:
            sys_info_parts.append(self.hostname)
        if self.show_username and self.username:
            sys_info_parts.append(self.username)
        if self.show_windows_version and self.windows_version:
            sys_info_parts.append(self.windows_version)
        if self.show_ip_address and self.ip_address:
            sys_info_parts.append(self.ip_address)
        if self.show_group_id and self.group_id:
            sys_info_parts.append(f"Group: {self.group_id}")

        # Left side: System information (if any)
        if sys_info_parts:
            left_frame = tk.Frame(main_frame, bg=self.bg_color)
            left_frame.grid(
                row=0,
                column=0,
                sticky="nsw",
                padx=(inner_padx, inner_padx),
                pady=inner_pady,
            )

            sys_info_text = " | ".join(sys_info_parts)

            sys_info_label = tk.Label(
                left_frame,
                text=sys_info_text,
                bg=self.bg_color,
                fg=self.fg_color,
                font=label_font,
                anchor="w",
            )
            sys_info_label.pack(fill=tk.BOTH, expand=True)

        # Center: Classification text
        center_frame = tk.Frame(main_frame, bg=self.bg_color)
        center_frame.grid(
            row=0,
            column=1,
            sticky="nsew",
            padx=inner_padx,
            pady=inner_pady,
        )

        classification_label = tk.Label(
            center_frame,
            text=f"{self.classification}",
            bg=self.bg_color,
            fg=self.fg_color,
            font=label_font,
            anchor="center",
        )
        classification_label.pack(expand=True, fill=tk.BOTH)

        # Right side: FPCON and CYBERCON (if set)
        if self.fpcon or self.cybercon:
            right_frame = tk.Frame(main_frame, bg=self.bg_color)
            right_frame.grid(
                row=0,
                column=2,
                sticky="nse",
                padx=(inner_padx, inner_padx),
                pady=inner_pady,
            )

            # Build the right-side text
            right_text_parts = []
            if self.fpcon:
                right_text_parts.append(f"FPCON: {self.fpcon}")
            if self.cybercon:
                right_text_parts.append(f"CYBERCON: {self.cybercon}")

            right_text = " | ".join(right_text_parts)

            right_label = tk.Label(
                right_frame,
                text=right_text,
                bg=self.bg_color,
                fg=self.fg_color,
                font=label_font,
                anchor="e",
            )
            right_label.pack(side=tk.RIGHT, expand=True, fill=tk.BOTH)

        # Keep window on top every 100ms
        def keep_on_top():
            window.attributes("-topmost", True)
            window.lift()
            window.after(100, keep_on_top)

        keep_on_top()

        # Optional: clean up appbar on close (if you allow closing)
        def on_close():
            try:
                remove_appbar_for_window(hwnd)
            except Exception:
                pass
            window.destroy()

        window.protocol("WM_DELETE_WINDOW", on_close)

        self.windows.append(window)

    def run(self):
        """Start the banner application"""
        if self.windows:
            # Run the first window's mainloop (all windows will stay open)
            self.windows[0].mainloop()


def main():
    """Main function to run the classification banner"""
    banner = ClassificationBanner()

    if banner.enabled:
        banner.run()
    else:
        print("Classification banner is disabled in registry (Enabled=0)")
        sys.exit(0)


if __name__ == "__main__":
    main()
