"""
Constants and configuration values for Classification Banner
"""

# AppBar message types
ABM_NEW = 0x00000000
ABM_REMOVE = 0x00000001
ABM_QUERYPOS = 0x00000002
ABM_SETPOS = 0x00000003

# AppBar edge positions
ABE_LEFT = 0
ABE_TOP = 1
ABE_RIGHT = 2
ABE_BOTTOM = 3

# Default banner settings
DEFAULT_CLASSIFICATION = "UNCONFIGURED"
DEFAULT_BG_COLOR = "#FFFFFF"
DEFAULT_FG_COLOR = "#000000"
DEFAULT_BANNER_HEIGHT = 35
DEFAULT_FONT_SIZE = 12
DEFAULT_FONT_FAMILY = "Arial"
DEFAULT_ENABLED = 1
DEFAULT_FPCON = "Alpha"
DEFAULT_CPCON = "1"
DEFAULT_CHECK_INTERVAL = 60000  # 1 minute in milliseconds

# Registry paths
REGISTRY_PATHS = [
    ("HKEY_LOCAL_MACHINE", r"SOFTWARE\ClassificationBanner"),
    ("HKEY_CURRENT_USER", r"SOFTWARE\ClassificationBanner"),
]

# Classification color schemes
COLOR_SCHEMES = {
    "UNCONFIGURED": {"bg": "#FFFFFF", "fg": "#000000"},
    "UNCLASSIFIED": {"bg": "#00FF00", "fg": "#000000"},
    "CUI": {"bg": "#502B85", "fg": "#FFFFFF"},
    "CONFIDENTIAL": {"bg": "#0000FF", "fg": "#FFFFFF"},
    "SECRET": {"bg": "#FF0000", "fg": "#000000"},
    "TOP SECRET": {"bg": "#FF8C00", "fg": "#000000"},
    "TOP SECRET//HCS-P/SI/TK//NOFORN": {"bg": "#FFFF00", "fg": "#000000"},
}

# UI layout settings
INNER_PADX = 10
INNER_PADY = 0

# Keep on top interval (milliseconds)
KEEP_ON_TOP_INTERVAL = 100
