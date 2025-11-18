# main.py
"""Main application entry point"""

from auth_windows import LoginWindow


def main():
    """Start the application"""
    app = LoginWindow()
    app.run()


if __name__ == "__main__":
    main()