"""
Main Classification Banner application
"""

import sys
from typing import List
from .settings import BannerSettings
from .registry_manager import RegistryManager
from .system_info import SystemInfoGatherer
from .monitor_manager import MonitorManager
from .banner_window import BannerWindow


class ClassificationBanner:
    """Main Classification Banner application"""

    def __init__(self):
        self.settings = BannerSettings()
        self.registry_manager = RegistryManager()
        self.system_info_gatherer = SystemInfoGatherer()
        self.windows: List[BannerWindow] = []
        self.system_info_text: str = ""

        # Load initial settings
        self._load_settings()
        self.settings.store_current_state()

        # Gather system info if needed
        if self.settings.needs_system_info():
            self._gather_system_info()

        # Generate Classification Text
        self.settings.get_classification_text()

        # Create banners if enabled
        if self.settings.enabled:
            self._create_banners()
            self._schedule_registry_check()

    def _load_settings(self):
        """Load settings from registry"""
        registry_settings = self.registry_manager.load_settings()
        self.settings.update_from_registry(registry_settings)

    def _gather_system_info(self):
        """Gather system information"""
        # Get group ID from registry if showing
        group_id = None
        if self.settings.show_group_id:
            group_id = self.registry_manager.read_group_id()

        # Gather info
        info = self.system_info_gatherer.gather_all(
            self.settings.get_show_flags(), group_id
        )

        # Build display text
        self.system_info_text = self.system_info_gatherer.build_display_text(info)

    def _create_banners(self):
        """Create banner windows for all monitors"""
        monitors = MonitorManager.get_all_monitors()

        for monitor in monitors:
            window = BannerWindow(monitor, self.settings, self.system_info_text)
            self.windows.append(window)

    def _recreate_banners(self):
        """Destroy and recreate all banners"""
        # Close existing windows
        self._close_all_windows()

        # Regather system info if needed
        if self.settings.needs_system_info():
            self._gather_system_info()

        # Regenerate Classification Text
        self.settings.get_classification_text()

        # Create new banners
        self._create_banners()

    def _close_all_windows(self):
        """Close all banner windows"""
        for window in self.windows:
            window.destroy()
        self.windows = []

    def _schedule_registry_check(self):
        """Schedule next registry check"""
        if self.windows:
            self.windows[0].get_window().after(
                self.settings.check_interval, self._check_registry_changes
            )

    def _check_registry_changes(self):
        """Check for registry changes and update if needed"""
        try:
            # Reload settings
            self._load_settings()

            # Check if changed
            if self.settings.has_changed():
                print("Registry settings changed - updating banner...")

                # If disabled, close everything
                if not self.settings.enabled:
                    print("Banner disabled - closing...")
                    self._close_all_windows()
                    sys.exit(0)

                # Recreate banners
                self._recreate_banners()

                # Update stored settings
                self.settings.store_current_state()

                print("Banner updated successfully")

            # Schedule next check
            self._schedule_registry_check()

        except SystemError as e:
            print(f"Error checking registry changes: {e}")
            # Continue checking even on error
            self._schedule_registry_check()

    def run(self):
        """Start the banner application"""
        if self.windows:
            self.windows[0].get_window().mainloop()
