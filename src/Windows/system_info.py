"""
System information gathering for Classification Banner
"""

import socket
import platform
import os
from typing import Dict, Optional, List


class SystemInfoGatherer:
    """Gathers system information for display"""
    
    def __init__(self):
        self.info: Dict[str,str] = {}
    
    def gather_all(self, show_flags: Dict[str, bool], group_id: Optional[str] = None) -> Dict[str, str]:
        """Gather all requested system information"""
        info: Dict[str,str] = {}
        
        if show_flags.get("show_hostname", False):
            info["hostname"] = self._get_hostname()
        
        if show_flags.get("show_username", False):
            info["username"] = self._get_username()
        
        if show_flags.get("show_windows_version", False):
            info["windows_version"] = self._get_windows_version()
        
        if show_flags.get("show_ip_address", False):
            info["ip_address"] = self._get_ip_address()
        
        if show_flags.get("show_group_id", False) and group_id:
            info["group_id"] = group_id
        
        return info
    
    def _get_hostname(self) -> str:
        """Get computer hostname"""
        try:
            return socket.gethostname()
        except:
            return ""
    
    def _get_username(self) -> str:
        """Get current username"""
        try:
            username = os.environ.get("USERNAME", "")
            if username:
                return username
        except:
            pass
        return ""
    
    def _get_windows_version(self) -> str:
        """Get Windows version"""
        try:
            version = platform.version()
            release = platform.release()
            return f"Windows {release} ({version})"
        except:
            return ""
    
    def _get_ip_address(self) -> str:
        """Get primary IP address"""
        try:
            s: socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.settimeout(0.1)
            try:
                s.connect(("10.254.254.254", 1))
                ip: str = s.getsockname()[0]
            except:
                ip: str = socket.gethostbyname(socket.gethostname())
            finally:
                s.close()
            return ip
        except:
            return ""
    
    def build_display_text(self, info: Dict[str, str]) -> str:
        """Build formatted display text from system info"""
        parts: List[str] = []
        
        if "hostname" in info and info["hostname"]:
            parts.append(info["hostname"])
        
        if "username" in info and info["username"]:
            parts.append(info["username"])
        
        if "windows_version" in info and info["windows_version"]:
            parts.append(info["windows_version"])
        
        if "ip_address" in info and info["ip_address"]:
            parts.append(info["ip_address"])
        
        if "group_id" in info and info["group_id"]:
            parts.append(f"Group: {info['group_id']}")
        
        return " | ".join(parts)
