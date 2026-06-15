"""Entry point for Universal PDF Converter."""
import sys
import os

# Ensure the project root is on the path regardless of where the script is launched from
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from gui.app import Application


def main():
    app = Application()
    app.run()


if __name__ == "__main__":
    main()
