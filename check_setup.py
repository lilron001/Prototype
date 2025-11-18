# check_setup.py
"""Verify all required files and dependencies are present"""

import os
import sys


def check_files():
    """Check if all required files exist"""
    required_files = [
        'config.py',
        'database.py',
        'email_service.py',
        'verification_window.py',
        'auth_windows.py',
        'dashboard.py',
        'main.py'
    ]

    print("Checking required files...")
    all_present = True

    for file in required_files:
        if os.path.exists(file):
            print(f"✓ {file} - Found")
        else:
            print(f"✗ {file} - MISSING")
            all_present = False

    return all_present


def check_dependencies():
    """Check if all required packages are installed"""
    required_packages = {
        'tkinter': 'tkinter',
        'supabase': 'supabase',
        'hashlib': 'hashlib',
        'random': 'random',
        'smtplib': 'smtplib',
        'email': 'email'
    }

    print("\nChecking required packages...")
    all_installed = True

    for package, import_name in required_packages.items():
        try:
            __import__(import_name)
            print(f"✓ {package} - Installed")
        except ImportError:
            print(f"✗ {package} - NOT INSTALLED")
            all_installed = False
            if package == 'supabase':
                print(f"  Install with: pip install supabase")

    return all_installed


def main():
    """Run all checks"""
    print("=" * 50)
    print("Setup Verification Script")
    print("=" * 50 + "\n")

    files_ok = check_files()
    packages_ok = check_dependencies()

    print("\n" + "=" * 50)
    if files_ok and packages_ok:
        print("✓ All checks passed! You can run: python main.py")
    else:
        print("✗ Some issues found. Please fix them before running.")
    print("=" * 50)


if __name__ == "__main__":
    main()