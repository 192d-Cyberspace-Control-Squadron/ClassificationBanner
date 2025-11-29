"""
Settings management for Classification Banner
"""

from typing import Dict, Any
from .constants import (
    DEFAULT_CLASSIFICATION,
    DEFAULT_BG_COLOR,
    DEFAULT_FG_COLOR,
    DEFAULT_BANNER_HEIGHT,
    DEFAULT_FONT_SIZE,
    DEFAULT_FONT_FAMILY,
    DEFAULT_ENABLED,
    DEFAULT_FPCON,
    DEFAULT_CPCON,
    DEFAULT_CHECK_INTERVAL,
    DEFAULT_CAVEATS,
    DEFAULT_DISSEMINATION_CONTROLS,
)


class BannerSettings:
    """Manages banner configuration settings"""

    def __init__(self):
        # Display settings
        self.classification: str = DEFAULT_CLASSIFICATION
        self.bg_color: str = DEFAULT_BG_COLOR
        self.fg_color: str = DEFAULT_FG_COLOR
        self.banner_height: int = DEFAULT_BANNER_HEIGHT
        self.font_size: int = DEFAULT_FONT_SIZE
        self.font_family: str = DEFAULT_FONT_FAMILY
        self.enabled: int = DEFAULT_ENABLED
        self.caveats: str = DEFAULT_CAVEATS
        self.dissemenation_controls: str = DEFAULT_DISSEMINATION_CONTROLS

        # Threat levels
        self.fpcon: str = DEFAULT_FPCON
        self.cpcon: str = DEFAULT_CPCON

        # System info flags
        self.show_hostname: bool = False
        self.show_username: bool = False
        self.show_windows_version: bool = False
        self.show_ip_address: bool = False
        self.show_group_id: bool = False

        # Group ID value
        self.group_id: str = ""

        # Monitoring
        self.check_interval: int = DEFAULT_CHECK_INTERVAL

        # Storage for change detection
        self.previous_settings: Dict[str,str|bool|int] = {}

    def update_from_registry(self, registry_settings: Dict[str, Any]) -> None:
        """Update settings from registry values"""
        # String values
        if registry_settings.get("Classification") is not None:
            self.classification = registry_settings["Classification"]

        if registry_settings.get("BackgroundColor") is not None:
            self.bg_color = registry_settings["BackgroundColor"]

        if registry_settings.get("TextColor") is not None:
            self.fg_color = registry_settings["TextColor"]

        if registry_settings.get("FPCON") is not None:
            self.fpcon = registry_settings["FPCON"]

        if registry_settings.get("CPCON") is not None:
            self.cpcon = str(registry_settings["CPCON"])

        if registry_settings.get("GroupID") is not None:
            self.group_id = registry_settings["GroupID"]
        
        if registry_settings.get("Caveats") is not None:
            self.group_id = registry_settings["Caveats"]

        if registry_settings.get("DisseminationControls") is not None:
            self.group_id = registry_settings["DisseminationControls"]

        # Integer values
        if registry_settings.get("Enabled") is not None:
            self.enabled = registry_settings["Enabled"]

        # Boolean values
        if registry_settings.get("ShowHostname") is not None:
            self.show_hostname = registry_settings["ShowHostname"]

        if registry_settings.get("ShowUsername") is not None:
            self.show_username = registry_settings["ShowUsername"]

        if registry_settings.get("ShowWindowsVersion") is not None:
            self.show_windows_version = registry_settings["ShowWindowsVersion"]

        if registry_settings.get("ShowIPAddress") is not None:
            self.show_ip_address = registry_settings["ShowIPAddress"]

        if registry_settings.get("ShowGroupID") is not None:
            self.show_group_id = registry_settings["ShowGroupID"]

    def store_current_state(self) -> None:
        """Store current settings for change detection"""
        self.previous_settings: Dict[str,str|bool|int] = {
            "classification": self.classification,
            "bg_color": self.bg_color,
            "fg_color": self.fg_color,
            "enabled": self.enabled,
            "fpcon": self.fpcon,
            "cpcon": self.cpcon,
            "caveats": self.caveats,
            "dissemination_controls": self.dissemenation_controls,
            "show_hostname": self.show_hostname,
            "show_username": self.show_username,
            "show_windows_version": self.show_windows_version,
            "show_ip_address": self.show_ip_address,
            "show_group_id": self.show_group_id,
            "group_id": self.group_id,
        }

    def has_changed(self) -> bool:
        """Check if settings have changed since last store"""
        current: Dict[str,str|bool|int] = {
            "classification": self.classification,
            "bg_color": self.bg_color,
            "fg_color": self.fg_color,
            "caveats": self.caveats,
            "dissemination_controls": self.dissemenation_controls,
            "enabled": self.enabled,
            "fpcon": self.fpcon,
            "cpcon": self.cpcon,
            "show_hostname": self.show_hostname,
            "show_username": self.show_username,
            "show_windows_version": self.show_windows_version,
            "show_ip_address": self.show_ip_address,
            "show_group_id": self.show_group_id,
            "group_id": self.group_id,
        }

        return current != self.previous_settings

    def needs_system_info(self) -> bool:
        """Check if any system info should be displayed"""
        return any(
            [
                self.show_hostname,
                self.show_username,
                self.show_windows_version,
                self.show_ip_address,
                self.show_group_id,
            ]
        )

    def get_show_flags(self) -> Dict[str, bool]:
        """Get dictionary of system info display flags"""
        return {
            "show_hostname": self.show_hostname,
            "show_username": self.show_username,
            "show_windows_version": self.show_windows_version,
            "show_ip_address": self.show_ip_address,
            "show_group_id": self.show_group_id,
        }
