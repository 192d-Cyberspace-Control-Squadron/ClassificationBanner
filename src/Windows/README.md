# Classification Banner - Modular Structure

## File Organization

```
modular/
├── __init__.py                 # Package initialization
├── main.py                     # Entry point
├── constants.py                # All constants and configuration
├── settings.py                 # Settings management
├── registry_manager.py         # Windows Registry operations
├── system_info.py              # System information gathering
├── monitor_manager.py          # Monitor detection
├── appbar.py                   # Windows AppBar management
├── banner_window.py            # Window creation and UI
└── banner.py                   # Main application logic
```

## Module Responsibilities

### constants.py
- AppBar constants (ABM_*, ABE_*)
- Default values for all settings
- Color schemes
- Registry paths
- UI layout constants

### settings.py
- `BannerSettings` class
- Manages all configuration settings
- Change detection
- Settings storage and comparison

### registry_manager.py
- `RegistryManager` class
- Reads from Windows Registry
- Handles HKLM and HKCU
- Applies color schemes

### system_info.py
- `SystemInfoGatherer` class
- Gathers hostname, IP, username, etc.
- Builds display text
- Handles errors gracefully

### monitor_manager.py
- `MonitorManager` class
- Detects all monitors
- Provides fallback for errors

### appbar.py
- Windows AppBar API structures (RECT, APPBARDATA)
- `register_appbar_for_window()`
- `remove_appbar_for_window()`

### banner_window.py
- `BannerWindow` class
- Creates and manages single window
- Builds UI panels (left, center, right)
- Handles window lifecycle

### banner.py
- `ClassificationBanner` class
- Main application logic
- Coordinates all modules
- Registry monitoring
- Window management

### main.py
- Entry point
- Creates ClassificationBanner instance
- Starts application

## Usage

### Run the Application
```python
python main.py
```

### Import as Module
```python
from banner import ClassificationBanner

app = ClassificationBanner()
app.run()
```

### Access Components
```python
from settings import BannerSettings
from registry_manager import RegistryManager

settings = BannerSettings()
registry = RegistryManager()
registry_data = registry.load_settings()
settings.update_from_registry(registry_data)
```

## Building Executable

### PyInstaller
```cmd
pyinstaller --onefile --noconsole ^
    --name ClassificationBanner ^
    --add-data "constants.py;." ^
    main.py
```

### With Spec File
Create `ClassificationBanner.spec`:
```python
# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=['screeninfo'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='ClassificationBanner',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
```

Then build:
```cmd
pyinstaller ClassificationBanner.spec
```

## Testing

### Run Tests
```cmd
pytest tests/ -v
```

### Test Individual Modules
```cmd
pytest tests/test_settings.py -v
pytest tests/test_registry_manager.py -v
pytest tests/test_system_info.py -v
```

## Advantages of Modular Structure

### Maintainability
- Each module has single responsibility
- Easier to locate and fix bugs
- Clear separation of concerns

### Testability
- Each module can be tested independently
- Easier to mock dependencies
- Better test coverage

### Reusability
- Modules can be used independently
- Easy to extract for other projects
- Clear interfaces

### Readability
- Smaller files are easier to understand
- Clear module names indicate purpose
- Less scrolling through code

### Extensibility
- Easy to add new features
- Can add new modules without affecting existing ones
- Clear extension points

## Migration from Monolithic

If migrating from single `main.py`:

1. All constants → `constants.py`
2. Settings class → `settings.py`
3. Registry functions → `registry_manager.py`
4. System info gathering → `system_info.py`
5. Monitor detection → `monitor_manager.py`
6. AppBar structures/functions → `appbar.py`
7. Window creation → `banner_window.py`
8. Main class → `banner.py`
9. Entry point → `main.py`

## Dependencies

Same as monolithic version:
```
screeninfo==0.8.1
```

## Module Dependencies

```
main.py
  └── banner.py
      ├── settings.py
      │   └── constants.py
      ├── registry_manager.py
      │   └── constants.py
      ├── system_info.py
      ├── monitor_manager.py
      └── banner_window.py
          ├── appbar.py
          │   └── constants.py
          ├── settings.py
          └── constants.py
```

## Version

- **Version:** 1.3.0
- **Structure:** Modular
- **Python:** 3.8+
- **Platform:** Windows 10/11
