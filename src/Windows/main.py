"""
Classification Banner - Main Entry Point
"""
import sys
import classification_banner as cb


def main():
    """Main entry point"""
    print(cb.__version__)
    banner = cb.banner.ClassificationBanner()
    
    if banner.settings.enabled:
        banner.run()
    else:
        print("Classification banner is disabled in registry (Enabled=0)")
        sys.exit(0)
    

if __name__ == "__main__":
    main()
