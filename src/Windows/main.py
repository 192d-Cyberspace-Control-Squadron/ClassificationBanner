"""
Classification Banner - Main Entry Point
"""

import sys
from ClassificationBanner.banner import ClassificationBanner


def main():
    """Main entry point"""
    banner = ClassificationBanner()

    if banner.settings.enabled:
        banner.run()
    else:
        print("Classification banner is disabled in registry (Enabled=0)")
        sys.exit(0)


if __name__ == "__main__":
    main()
