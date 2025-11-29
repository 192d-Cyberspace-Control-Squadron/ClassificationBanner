# Migration Guide: Monolithic to Modular Structure

## Overview

This guide helps you migrate from the single-file `main.py` to the modular structure.

## File Mapping

### Old (Monolithic) → New (Modular)

| Original Code | New Location | Module |
|--------------|--------------|---------|
| `ABM_NEW`, `ABM_REMOVE`, etc. | `constants.py` | Constants |
| `ABE_TOP`, `ABE_LEFT`, etc. | `constants.py` | Constants |
| `RECT` class | `appbar.py` | AppBar |
| `APPBARDATA` class | `appbar.py` | AppBar |
| `register_appbar_for_window()` | `appbar.py` | AppBar |
| `remove_appbar_for_window()` | `appbar.py` | AppBar |
| `ClassificationBanner.__init__()` | `banner.py` | Main app |
| Registry reading logic | `registry_manager.py` | Registry |
| System info gathering | `system_info.py` | System info |
| Monitor detection | `monitor_manager.py` | Monitors |
| Window creation | `banner_window.py` | Window |
| Settings management | `settings.py` | Settings |
| Default values | `constants.py` | Constants |
| Color schemes | `constants.py` | Constants |
| Main entry point | `main.py` | Entry point |

## Code Changes

### Import Statements

**Before (monolithic):**
```python
import tkinter as tk
from tkinter import font
import ctypes
import sys
import winreg
from screeninfo import get_monitors
import socket
import platform
import os
```

**After (modular):**
```python
# In main.py
from banner import ClassificationBanner

# In banner.py
from settings import BannerSettings
from registry_manager import RegistryManager
from system_info import SystemInfoGatherer
from monitor_manager import MonitorManager
from banner_window import BannerWindow

# In banner_window.py
import tkinter as tk
from tkinter import font
from appbar import register_appbar_for_window, remove_appbar_for_window
from constants import ABE_TOP, INNER_PADX, INNER_PADY
```

### Creating an Instance

**Before:**
```python
banner = ClassificationBanner()
banner.run()
```

**After (same):**
```python
banner = ClassificationBanner()
banner.run()
```

### Accessing Settings

**Before:**
```python
banner = ClassificationBanner()
print(banner.classification)
print(banner.bg_color)
```

**After:**
```python
banner = ClassificationBanner()
print(banner.settings.classification)
print(banner.settings.bg_color)
```

### Loading Registry Settings

**Before (in __init__):**
```python
self.load_registry_settings()
```

**After:**
```python
self._load_settings()  # Uses RegistryManager internally
```

### Gathering System Info

**Before:**
```python
self.gather_system_info()
```

**After:**
```python
self._gather_system_info()  # Uses SystemInfoGatherer internally
```

### Creating Windows

**Before:**
```python
self.create_banners()
```

**After:**
```python
self._create_banners()  # Uses BannerWindow class internally
```

## Running the Application

### Development

**Before:**
```cmd
python main.py
```

**After (same):**
```cmd
cd modular
python main.py
```

### Building

**Before:**
```cmd
pyinstaller --onefile --noconsole --name ClassificationBanner main.py
```

**After:**
```cmd
cd modular
pyinstaller ClassificationBanner.spec
```

Or:
```cmd
cd modular
pyinstaller --onefile --noconsole --name ClassificationBanner main.py
```

## Testing

### Before (monolithic)
```cmd
pytest test_main.py -v
```

### After (modular)
Each module can be tested independently:
```cmd
pytest tests/test_settings.py -v
pytest tests/test_registry_manager.py -v
pytest tests/test_system_info.py -v
pytest tests/test_banner.py -v
```

Or test all:
```cmd
pytest tests/ -v
```

## Key Differences

### 1. Settings Access

**Monolithic:**
```python
banner.classification = "SECRET"
banner.bg_color = "#FF0000"
```

**Modular:**
```python
banner.settings.classification = "SECRET"
banner.settings.bg_color = "#FF0000"
```

### 2. Private Methods

All internal methods are now prefixed with `_`:

**Monolithic:**
```python
self.load_registry_settings()
self.gather_system_info()
self.create_banners()
```

**Modular:**
```python
self._load_settings()
self._gather_system_info()
self._create_banners()
```

### 3. Module Dependencies

**Monolithic:** Everything in one file

**Modular:** Clear dependency chain
```
main.py
  └── banner.py
      ├── settings.py
      ├── registry_manager.py
      ├── system_info.py
      ├── monitor_manager.py
      └── banner_window.py
          └── appbar.py
```

## Advantages of Modular Structure

### 1. Easier Testing
Each module can be tested independently with focused tests.

### 2. Better Organization
Related code is grouped together in dedicated files.

### 3. Easier Maintenance
Bugs are easier to locate and fix in smaller, focused files.

### 4. Reusability
Individual modules can be reused in other projects.

### 5. Clear Separation
Each module has a single, well-defined responsibility.

## Common Migration Issues

### Issue 1: Import Errors

**Problem:**
```
ModuleNotFoundError: No module named 'constants'
```

**Solution:**
Ensure you're running from the modular directory:
```cmd
cd modular
python main.py
```

### Issue 2: Relative Imports

**Problem:**
```
ImportError: attempted relative import with no known parent package
```

**Solution:**
Use absolute imports in all modules:
```python
from constants import DEFAULT_CLASSIFICATION  # Good
from .constants import DEFAULT_CLASSIFICATION  # Avoid
```

### Issue 3: Circular Dependencies

**Problem:**
```
ImportError: cannot import name 'X' from partially initialized module
```

**Solution:**
The modular structure is designed to avoid circular dependencies. Follow the dependency hierarchy in README.md.

### Issue 4: PyInstaller Not Finding Modules

**Problem:**
Built .exe doesn't work, modules not found.

**Solution:**
Use the provided spec file which lists all hiddenimports:
```cmd
pyinstaller ClassificationBanner.spec
```

## Backward Compatibility

The modular version maintains the same external interface:

```python
# Both versions work the same way
from banner import ClassificationBanner

app = ClassificationBanner()
if app.settings.enabled:  # Note: .settings in modular
    app.run()
```

## Migration Checklist

- [ ] Copy all modular files to new directory
- [ ] Install dependencies (`pip install screeninfo`)
- [ ] Test basic functionality (`python main.py`)
- [ ] Test registry loading
- [ ] Test system info gathering
- [ ] Test multi-monitor support
- [ ] Test registry monitoring
- [ ] Build executable (`pyinstaller ClassificationBanner.spec`)
- [ ] Test built executable
- [ ] Update deployment scripts if needed
- [ ] Update documentation references

## Rollback Plan

If needed, you can always return to the monolithic version:

1. Keep the original `main.py` as `main_monolithic.py`
2. Test modular version thoroughly before deployment
3. If issues arise, rename files back:
   ```cmd
   mv main.py main_modular.py
   mv main_monolithic.py main.py
   ```

## Next Steps

After migration:

1. **Update Tests:** Create tests for each module
2. **Update Documentation:** Reference new module structure
3. **Update Build Scripts:** Use new spec file
4. **Update Deployment:** Ensure all modules are included
5. **Code Review:** Review each module for improvements

## Support

For issues during migration:
1. Check README.md for module responsibilities
2. Review module dependencies diagram
3. Compare with original main.py
4. Test each module independently
