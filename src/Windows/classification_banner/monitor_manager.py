"""
Monitor detection and management
"""

from typing import Any
from screeninfo import get_monitors


class MonitorManager:
    """Manages monitor detection"""

    @staticmethod
    def get_all_monitors() -> Any:
        """Get all connected monitors"""
        try:
            return get_monitors()
        except SystemError as e:
            print(f"Error detecting monitors: {e}")
            # Fallback to single monitor
            return [MonitorManager._create_fallback_monitor()]

    @staticmethod
    def _create_fallback_monitor():
        """Create a fallback monitor object"""
        return type("Monitor", (), {"x": 0, "y": 0, "width": 1920, "height": 1080})()
